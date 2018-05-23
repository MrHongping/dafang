# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: config.py
@time: 2018/2/18 21:14
"""
SPLIT_SYMBOL_LEFT='->|'
SPLIT_SYMBOL_RIGHT='|<-'

ERROR_LABEL='ERROR://'

FILE_TREE_ROOT_TEXT='$#root#$'

SHELL_MANAGE_MENU=u'添加 编辑 删除 || 文件管理 数据库管理 虚拟终端 || HTTP参数 内网通道'

FILE_MANAGE_MENU=u'下载文件到服务器 上传 下载 编辑 删除 新建'

DIRECTORY_MANAGE_MENU=u'下载文件到服务器 上传 删除 新建'

EMPTY_DIRECTORY_MANAGE_MENU=u'下载文件到服务器 上传'

TAB_MANAGE_MENU=u'关闭当前选项卡 关闭其他选项卡 关闭右侧所有选项卡 关闭左侧所有选项卡 关闭所有选项卡'

MANAGE_MENU=u'添加 关于'

SHELL_SCRIPT_LIST=['PHP','JSP']

SHELL_ENCODE_LIST=['UTF-8','GB2312']

TUNNEL_LISTEN_IP_LIST=['0.0.0.0','127.0.0.1']

HTTP_DEFAULT_COOKIE='hello=201802200559'

HTTP_DEFAULT_UA='Mozilla/5.0 (Dafang1.0)'

USER_AGENT_LIST=['Mozilla/5.0 (Linux; U; Android 4.1.1; ja-jp; Galaxy Nexus Build/JRO03H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 ',
                 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko']

TERMINAL_PATH_TEMPLATE='[{0}]$'

DATABASE_SETTING_TEMPLATE=[
    '''<T>XDB</T>
<X>
com.mysql.jdbc.Driver\r\njdbc:mysql://localhost/test?user=root&password=123456
</X>''',
    '''<T>XDB</T>
<X>
com.microsoft.sqlserver.jdbc.SQLServerDriver\r\njdbc:sqlserver://127.0.0.1:1433;databaseName=test;user=sa;password=123456
</X>''',
    '''<T>XDB</T>
<X>
oracle.jdbc.driver.OracleDriver\r\njdbc:oracle:thin:user/password@127.0.0.1:1521/test
</X>''']

#请求返回值
REQUESTS_SENDING=0
SUCCESS_RESPONSE=1
ERROR_RESPONSE_NO_SYMBOL=2
ERROR_RESPONSE_WITH_SYMBOL=3
ERROR_DAFANG=4

#任务类型
TASK_GET_START=1
TASK_GET_DIRECTORY_CONTENT=2
TASK_GET_FILE_CONTENT=3
TASK_CREATE_FILE=4
TASK_DELETE_FILE_OR_DIRECTORY=5
TASK_DOWNLOAD_FILE=6
TASK_UPLOAD_FILE=7
TASK_EXCUTE_COMMAND=8
TASK_GET_DATABASES=9
TASK_GET_TABLES=10
TASK_GET_COLUMNS=11
TASK_EXCUTE_SQLQUERY=12

