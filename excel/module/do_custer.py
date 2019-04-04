# -*- coding: utf-8 -*-
import time
import os
import shutil
import subprocess
import re
from module.log import *
class do_custer(object):
    #def __init__(self, name):
    #    self.name = name
    def do_command(self, cmd):
        """
        执行bash命令
        """
        return subprocess.call(cmd, shell=True)
    def init_folder(self, folder):
        try:
            os.mkdir(folder)
        except Exception, e:
            logger.info("创建文件失败 %s %s." % (folder, e))
        return folder
    def cd_logs(self, folder, riqi):
        os.chdir(folder)
        try:
            shutil.rmtree(riqi)
        except Exception, e:
            logger.info("删除logs文件出现异常 %s."  % e)
        os.mkdir(riqi)
        os.chdir(riqi)
        return os.path.join(folder, riqi)
    def wget_url(self, conf, pwd):
        f = open(conf,'r+')
        for url in f:
            logger.info("取出来的url是 %s." % url)
            str=" "
            a=("wget", "-t2", "-T3", "-P", pwd, url)
            cmd = str.join(a)
            logger.info("组合的下载命令是 %s." % cmd)
            try:
                status=self.do_command(cmd)
                logger.info("status的值是 %s."  % status)
                if status==0:
                    print "oops，%s 下载完成." % url
                else:
                    dbname=re.split(r'[/]', url)[-1]
                    logger.info("下载失败,取出的客户的数据库的名字是 %s."  % dbname)
                    self.touch_file(dbname)
                    return dbname
            except Exception, e:
                logger.info("下载文件出现异常 %s." % e)
    def touch_file(self, name):
        str=" "
        name = ("touch", name)
        cmd=str.join(name)
        logger.info("cmd的值是  %s." % cmd)
        self.do_command(cmd)
        return name
    def rm_backup(self, base_dir, date):
        str=" "
        a=("rm -f", os.path.join(base_dir, "backup", date))
        a=str.join(a)
        a=a+"."+"txt"
        logger.info("删除昨天的文件的完整命令是 %s." %a)
        try:
            self.do_command(a)
        except Exception, e:
            logger.info("删除backup下的文件失败 %s." % e)
        return a
