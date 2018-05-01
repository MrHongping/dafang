# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: shellEntity.py
@time: 2018/2/18 16:38
"""
import urllib

import sys

class shell_entity:

    def __init__(self,shell_address,shell_password,shell_script_type,shell_encode_type,database_info,shell_remark,createTime,shell_id=-1):
        self.shell_address=shell_address
        self.shell_password=shell_password
        self.shell_script_type=shell_script_type
        self.shell_encode_type=shell_encode_type
        self.shell_host=self.getShellHost(shell_address)
        self.database_info=database_info
        self.shell_remark=shell_remark
        self.createTime=createTime
        self.shell_id=shell_id

    def getShellHost(self,shell_address):
        proto_host_path = urllib.splittype(shell_address)

        if proto_host_path:
            host_port_path = urllib.splithost(proto_host_path[1])

            if host_port_path:

                host_port = urllib.splitnport(host_port_path[0], 80)

                if host_port:
                     return host_port[0]
                else:
                    return 'no host'

class HttpSettingEntity:

    def __init__(self,cookie,user_agent,shellID=-1):
        self.cookie=cookie
        self.user_agent=user_agent
        self.shellID=shellID

class TunnelSettingEntity:

    def __init__(self,port,IP,shellID):
        self.port=port
        self.IP=IP
        self.shellID=shellID

