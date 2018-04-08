# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: dbHelp.py
@time: 2018/4/6 20:13
"""

import sqlite3
from entity import shell_entity


class DatabaseConnector:

    def __init__(self,dbName):
        self.connect=sqlite3.connect(dbName,timeout=3)
        self.cursor=self.connect.cursor()

    def getCursor(self):
        return self.cursor

    def saveShellEntity(self,shellEntity):

        sqlStr="insert into shell (shellAddress,shellPassword,databaseConnectInfo,shellRemark,scriptType,encodeType,useHttpDefault,useTunnelDefault,createTime) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(shellEntity.shell_address,shellEntity.shell_password,shellEntity.shell_script_type,shellEntity.shell_encode_type,shellEntity.database_info,shellEntity.shell_remark,shellEntity.httpSettingDefault,shellEntity.tunnelSettingDefault,shellEntity.createTime)
        self.cursor.execute(sqlStr)
        self.connect.commit()

    def getShellEntityList(self):
        shellEntityList=[]
        sqlStr = "select *from shell"
        dataSet=self.cursor.execute(sqlStr)
        for item in dataSet:
            shellEntityList.append(shell_entity(item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9]))
        return shellEntityList

DatabaseHelper=DatabaseConnector('../dafang.db')

if __name__ == '__main__':
    DatabaseHelper.saveShellEntity()