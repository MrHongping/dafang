#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib3,random
from urlparse import urlparse
from socket import *
from threading import Thread
from time import sleep
import wx,sys

sys.path.append("..")

from utils import config
from utils.entity import SessionEntity

# Constants
SOCKTIMEOUT = 5
RESENDTIMEOUT = 300
VER = "\x05"
METHOD = "\x00"
SUCCESS = "\x00"
SOCKFAIL = "\x01"
NETWORKFAIL = "\x02"
HOSTFAIL = "\x04"
REFUSED = "\x05"
TTLEXPIRED = "\x06"
UNSUPPORTCMD = "\x07"
ADDRTYPEUNSPPORT = "\x08"
UNASSIGNED = "\x09"

BASICCHECKSTRING = "Georg says, 'All seems fine'"

class StatusLog:

    def __init__(self,callBack,sessionEntity):
        self.callBack=callBack
        self.sessionEntity=sessionEntity

    def info(self,message):
        print 'info:' + message
        self.sessionEntity.sessionStatus=config.SESSION_INFO_MESSAGE
        self.sessionEntity.sessionMessage=message
        wx.CallAfter(self.callBack,self.sessionEntity)

    def debug(self,message):
        print 'debug:'+message
        self.sessionEntity.sessionStatus=config.SESSION_DEBUG_MESSAGE
        self.sessionEntity.sessionMessage=message
        wx.CallAfter(self.callBack,self.sessionEntity)

    def error(self,message):
        print 'error:' + message
        self.sessionEntity.sessionStatus=config.SESSION_ERROR_MESSAGE
        self.sessionEntity.sessionMessage=message
        wx.CallAfter(self.callBack,self.sessionEntity)


class SocksCmdNotImplemented(Exception):
    pass


class SocksProtocolNotImplemented(Exception):
    pass


class RemoteConnectionFailed(Exception):
    pass


class session(Thread):
    def __init__(self, pSocket, connectString, callBack):

        Thread.__init__(self)

        self.pSocket = pSocket
        self.connectString = connectString
        o = urlparse(connectString)
        tunnelSeesion=SessionEntity(self.getSessionID(),sessionBelong=connectString)
        self.log=StatusLog(callBack,tunnelSeesion)
        try:
            self.httpPort = o.port
        except:
            if o.scheme == "https":
                self.httpPort = 443
            else:
                self.httpPort = 80
        self.httpScheme = o.scheme
        self.httpHost = o.netloc.split(":")[0]
        self.httpPath = o.path
        self.cookie = None
        if o.scheme == "http":
            self.httpScheme = urllib3.HTTPConnectionPool
        else:
            self.httpScheme = urllib3.HTTPSConnectionPool

    def getSessionID(self):
        seed = "1234567890abcdef"
        taskID = ''
        for i in range(32):
            taskID+=random.choice(seed)
        return taskID

    def parseSocks5(self, sock):
        self.log.debug("SocksVersion5 detected")
        nmethods, methods = (sock.recv(1), sock.recv(1))
        sock.sendall(VER + METHOD)
        ver = sock.recv(1)
        print ver
        if ver == "\x02":  # this is a hack for proxychains
            ver, cmd, rsv, atyp = (sock.recv(1), sock.recv(1), sock.recv(1), sock.recv(1))
        else:
            cmd, rsv, atyp = (sock.recv(1), sock.recv(1), sock.recv(1))
        target = None
        targetPort = None
        if atyp == "\x01":  # IPv4
            # Reading 6 bytes for the IP and Port
            target = sock.recv(4)
            targetPort = sock.recv(2)
            target = "." .join([str(ord(i)) for i in target])
        elif atyp == "\x03":  # Hostname
            targetLen = ord(sock.recv(1))  # hostname length (1 byte)
            target = sock.recv(targetLen)
            targetPort = sock.recv(2)
            target = "".join([unichr(ord(i)) for i in target])
        elif atyp == "\x04":  # IPv6
            target = sock.recv(16)
            targetPort = sock.recv(2)
            tmp_addr = []
            for i in xrange(len(target) / 2):
                tmp_addr.append(unichr(ord(target[2 * i]) * 256 + ord(target[2 * i + 1])))
            target = ":".join(tmp_addr)
        targetPort = ord(targetPort[0]) * 256 + ord(targetPort[1])
        if cmd == "\x02":  # BIND
            raise SocksCmdNotImplemented("Socks5 - BIND not implemented")
        elif cmd == "\x03":  # UDP
            raise SocksCmdNotImplemented("Socks5 - UDP not implemented")
        elif cmd == "\x01":  # CONNECT
            serverIp = target
            try:
                serverIp = gethostbyname(target)
            except:
                self.log.error("oeps")
            serverIp = "".join([chr(int(i)) for i in serverIp.split(".")])
            self.cookie = self.setupRemoteSession(target, targetPort)
            if self.cookie:
                sock.sendall(VER + SUCCESS + "\x00" + "\x01" + serverIp + chr(targetPort / 256) + chr(targetPort % 256))
                return True
            else:
                sock.sendall(VER + REFUSED + "\x00" + "\x01" + serverIp + chr(targetPort / 256) + chr(targetPort % 256))
                raise RemoteConnectionFailed("[%s:%d] Remote failed" % (target, targetPort))

        raise SocksCmdNotImplemented("Socks5 - Unknown CMD")

    def parseSocks4(self, sock):
        self.log.debug("SocksVersion4 detected")
        cmd = sock.recv(1)
        if cmd == "\x01":  # Connect
            targetPort = sock.recv(2)
            targetPort = ord(targetPort[0]) * 256 + ord(targetPort[1])
            target = sock.recv(4)
            sock.recv(1)
            target = ".".join([str(ord(i)) for i in target])
            serverIp = target
            try:
                serverIp = gethostbyname(target)
            except:
                self.log.error("oeps")
            serverIp = "".join([chr(int(i)) for i in serverIp.split(".")])
            self.cookie = self.setupRemoteSession(target, targetPort)
            if self.cookie:
                sock.sendall(chr(0) + chr(90) + serverIp + chr(targetPort / 256) + chr(targetPort % 256))
                return True
            else:
                sock.sendall("\x00" + "\x91" + serverIp + chr(targetPort / 256) + chr(targetPort % 256))
                raise RemoteConnectionFailed("Remote connection failed")
        else:
            raise SocksProtocolNotImplemented("Socks4 - Command [%d] Not implemented" % ord(cmd))

    def handleSocks(self, sock):
        # This is where we setup the socks connection
        ver = sock.recv(1)
        if ver == "\x05":
            return self.parseSocks5(sock)
        elif ver == "\x04":
            return self.parseSocks4(sock)

    def setupRemoteSession(self, target, port):
        headers = {"X-CMD": "CONNECT", "X-TARGET": target, "X-PORT": port}
        self.target = target
        self.port = port
        cookie = None
        conn = self.httpScheme(host=self.httpHost, port=self.httpPort)
        response = conn.urlopen('POST', self.connectString + "?cmd=connect&target=%s&port=%d" % (target, port), headers=headers, body="")
        if response.status == 200:
            status = response.getheader("x-status")
            if status == "OK":
                cookie = response.getheader("set-cookie")
                self.log.info("[%s:%d] HTTP [200]: cookie [%s]" % (self.target, self.port, cookie))
            else:
                if response.getheader("X-ERROR") is not None:
                    self.log.error(response.getheader("X-ERROR"))
        else:
            self.log.error("[%s:%d] HTTP [%d]: [%s]" % (self.target, self.port, response.status, response.getheader("X-ERROR")))
            self.log.error("[%s:%d] RemoteError: %s" % (self.target, self.port, response.data))
        conn.close()
        return cookie

    def closeRemoteSession(self):
        headers = {"X-CMD": "DISCONNECT", "Cookie": self.cookie}
        params = ""
        conn = self.httpScheme(host=self.httpHost, port=self.httpPort)
        response = conn.request("POST", self.httpPath + "?cmd=disconnect", params, headers)
        if response.status == 200:
            self.log.info("[%s:%d] Connection Terminated" % (self.target, self.port))
        conn.close()

    def reader(self):
        conn = urllib3.PoolManager()
        while True:
            try:
                if not self.pSocket:
                    break
                data = ""
                headers = {"X-CMD": "READ", "Cookie": self.cookie, "Connection": "Keep-Alive"}
                response = conn.urlopen('POST', self.connectString + "?cmd=read", headers=headers, body="")
                data = None
                if response.status == 200:
                    status = response.getheader("x-status")
                    if status == "OK":
                        if response.getheader("set-cookie") is not None:
                            cookie = response.getheader("set-cookie")
                        data = response.data
                        # Yes I know this is horrible, but its a quick fix to issues with tomcat 5.x bugs that have been reported, will find a propper fix laters
                        try:
                            if response.getheader("server").find("Apache-Coyote/1.1") > 0:
                                data = data[:len(data) - 1]
                        except:
                            pass
                        if data is None:
                            data = ""
                    else:
                        data = None
                        self.log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target, self.port, response.status, status, response.getheader("X-ERROR")))
                else:
                    self.log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target, self.port, response.status))
                if data is None:
                    # Remote socket closed
                    break
                if len(data) == 0:
                    sleep(0.1)
                    continue
                self.log.info("[%s:%d] <<<< [%d]" % (self.target, self.port, len(data)))
                self.pSocket.send(data)
            except Exception, ex:
                raise ex
        self.closeRemoteSession()
        self.log.debug("[%s:%d] Closing localsocket" % (self.target, self.port))
        try:
            self.pSocket.close()
        except:
            self.log.debug("[%s:%d] Localsocket already closed" % (self.target, self.port))

    def writer(self):
        conn = urllib3.PoolManager()
        while True:
            try:
                self.pSocket.settimeout(1)
                data = self.pSocket.recv(1024)
                if not data:
                    break
                headers = {"X-CMD": "FORWARD", "Cookie": self.cookie, "Content-Type": "application/octet-stream", "Connection": "Keep-Alive"}
                response = conn.urlopen('POST', self.connectString + "?cmd=forward", headers=headers, body=data)
                if response.status == 200:
                    status = response.getheader("x-status")
                    if status == "OK":
                        if response.getheader("set-cookie") is not None:
                            self.cookie = response.getheader("set-cookie")
                    else:
                        self.log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target, self.port, response.status, status, response.getheader("x-error")))
                        break
                else:
                    self.log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target, self.port, response.status))
                    break
                self.log.info("[%s:%d] >>>> [%d]" % (self.target, self.port, len(data)))
            except timeout:
                continue
            except Exception, ex:
                raise ex
                break
        self.closeRemoteSession()
        self.log.debug("Closing localsocket")
        try:
            self.pSocket.close()
        except:
            self.log.debug("Localsocket already closed")

    def run(self):
        try:
            if self.handleSocks(self.pSocket):
                self.log.debug("Staring reader")
                r = Thread(target=self.reader, args=())
                r.start()
                self.log.debug("Staring writer")
                w = Thread(target=self.writer, args=())
                w.start()
                r.join()
                w.join()
        except SocksCmdNotImplemented, si:
            self.log.error(si.message)
            self.pSocket.close()
        except SocksProtocolNotImplemented, spi:
            self.log.error(spi.message)
            self.pSocket.close()
        except Exception, e:
            self.log.error(e.message)
            self.closeRemoteSession()
            self.pSocket.close()



class SocksProxy(Thread):

    def __init__(self,callBack,listenPort,listenAddress,scriptUrl,bufferSize=1024):
        Thread.__init__(self)

        self.callBack=callBack
        self.listenPort=listenPort
        self.listenAddress=listenAddress
        self.scriptUrl=scriptUrl
        self.bufferSize=bufferSize
        tunnelSession=SessionEntity('root',sessionBelong=scriptUrl)
        self.log=StatusLog(self.callBack,tunnelSession)

    def run(self):

        self.log.info("Starting socks server [%s:%s], tunnel at [%s]" % (self.listenAddress, self.listenPort, self.scriptUrl))
        self.log.info("检查Georg是否运行良好")
        if not self.askGeorg(self.scriptUrl):
            self.log.info("Georg运行异常，请检查配置URL")
            exit()
        servSock = socket(AF_INET, SOCK_STREAM)
        servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        servSock.bind((self.listenAddress, int(self.listenPort)))
        servSock.listen(1000)
        while True:
            try:
                sock, addr_info = servSock.accept()
                sock.settimeout(SOCKTIMEOUT)
                self.log.debug("新的连接")
                session(sock, self.scriptUrl,self.callBack).start()
            except KeyboardInterrupt, ex:
                break
            except Exception, e:
                self.log.error(str(e))
        servSock.close()

    def askGeorg(self,connectString):
        connectString = connectString
        o = urlparse(connectString)
        try:
            httpPort = o.port
        except:
            if o.scheme == "https":
                httpPort = 443
            else:
                httpPort = 80
        httpScheme = o.scheme
        httpHost = o.netloc.split(":")[0]
        httpPath = o.path
        if o.scheme == "http":
            httpScheme = urllib3.HTTPConnectionPool
        else:
            httpScheme = urllib3.HTTPSConnectionPool

        conn = httpScheme(host=httpHost, port=httpPort)
        response = conn.request("GET", httpPath)
        if response.status == 200:
            if BASICCHECKSTRING == response.data.strip():
                self.log.info('远端Georg运行良好')
                return True
        conn.close()
        return False
