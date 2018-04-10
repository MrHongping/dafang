# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: dbHelp.py
@time: 2018/4/6 20:13
"""

import sqlite3
from entity import *


class DatabaseConnector:

    def __init__(self,dbName):
        self.connect=sqlite3.connect(dbName,timeout=3)
        self.cursor=self.connect.cursor()

    def getCursor(self):
        return self.cursor

    def saveShellEntity(self,shellEntity):

        sqlStr="insert into shell (shellAddress,shellPassword,databaseConnectInfo,shellRemark,scriptType,encodeType,createTime) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(shellEntity.shell_address,shellEntity.shell_password,shellEntity.shell_script_type,shellEntity.shell_encode_type,shellEntity.database_info,shellEntity.shell_remark,shellEntity.createTime)
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def saveHttpSettingEntity(self,httpSettingEntity):
        sqlStr = "insert into httpSetting (shellID,Cookie,User_Agent) VALUES ('{0}','{1}','{2}')".format(
            httpSettingEntity.shellID,httpSettingEntity.cookie,httpSettingEntity.user_agent)
        print sqlStr
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def saveTunnelSettingEntity(self,tunnelSettingEntity):
        sqlStr = "insert into tunnelSetting (shellID,tunnelPort,tunnelIP) VALUES ('{0}','{1}','{2}')".format(
            tunnelSettingEntity.shellID,tunnelSettingEntity.port,tunnelSettingEntity.IP)
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def updateShellEntityByID(self,shellEntity,shellID):
        sqlStr = "update shell set shellAddress='{0}',shellPassword='{1}',databaseConnectInfo='{2}',shellRemark='{3}',scriptType='{4}',encodeType='{5}' WHERE shellID={6}".format(
            shellEntity.shell_address, shellEntity.shell_password, shellEntity.shell_script_type,
            shellEntity.shell_encode_type, shellEntity.database_info, shellEntity.shell_remark,shellID)
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def getShellEntityList(self):
        shellEntityList=[]
        sqlStr = "select *from shell"
        dataSet=self.cursor.execute(sqlStr)
        for item in dataSet:
            shellEntityList.append(shell_entity(item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[0]))
        return shellEntityList

    def deleteShellEntityByID(self,id):
        sqlStr = "delete from shell where shellID={0}".format(id)
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def getHttpSettingEntityByShellID(self,shellID):
        sqlStr = "select *from httpSetting where shellID='{0}'".format(shellID)
        dataSet = self.cursor.execute(sqlStr)
        for item in dataSet:
            return HttpSettingEntity(item[2], item[3],shellID)
        return None

    def updateHttpSettingEntity(self,httpSettingEntity):
        sqlStr = "update httpSetting set Cookie='{0}',User_Agent='{1}' WHERE shellID={2}".format(
            httpSettingEntity.cookie,httpSettingEntity.user_agent, httpSettingEntity.shellID)
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def getTunnelSettingEntityByShellID(self,shellID):
        sqlStr = "select *from tunnelSetting where shellID='{0}'".format(shellID)
        dataSet = self.cursor.execute(sqlStr)
        for item in dataSet:
            return TunnelSettingEntity(item[2], item[3],shellID)
        return None

    def updateTunnelSettingEntity(self,tunnelSettingEntity):
        sqlStr = "update tunnelSetting set tunnelPort={0},tunnelIP='{1}' WHERE shellID={2}".format(
            tunnelSettingEntity.port,tunnelSettingEntity.IP, tunnelSettingEntity.shellID)
        self.cursor.execute(sqlStr)
        self.connect.commit()

DatabaseHelper=DatabaseConnector('../dafang.db')

if __name__ == '__main__':
    DatabaseHelper.saveShellEntity()