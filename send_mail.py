#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import smtplib
import string
import shutil
#import  wget
import  os
import time
from datetime import timedelta, datetime

###################################################################################
def chushihua():
    os.chdir('/home/legend_zhang/logs/')
    riqi = time.strftime("%Y%m%d")
    try:
        shutil.rmtree(riqi)
    except:
        print "Nothing to be done"
    os.mkdir(riqi)
    os.chdir(riqi)

def youjian():
    f = open('/home/legend_zhang/kehu.txt','r+')
    for url in f:
        try:
            #wget.download(url)
            os.environ['url'] = str(url)
            print "开始下载: %s" % url
            os.popen("wget -c -t2 -T5 $url")
            print "oops，下载完成"
        except:
            print "糟糕，下载出错,没有抓到"

    for list in  os.listdir('.'):
        content = open(list, 'r+')
        #shell用python变量
        #os.environ['list'] = str(list)
        print list
        name1 = list.split('.')[0]
        print name1
        #name = os.popen("tail -6 $list|head -1|awk  '{print $2}'|awk -F'.' '{print $1,$2}' OFS='.'").read().strip()
        yesterday = datetime.today() + timedelta(-1)
        yesterday_format = yesterday.strftime('%Y-%m-%d')
        name = name1 + '.' + yesterday_format + '.' + 'daoku'
        print name
        HOST = "smtp.exmail.qq.com"
        SUBJECT = name
        print SUBJECT
        TO = "要发送给的用户"
        FROM = "发件人"
        text = content.read()
        BODY = string.join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "Subject: %s" % SUBJECT ,
                "",
                text
                ), "\r\n")
        server = smtplib.SMTP()
        server.connect(HOST,"25")
        server.starttls()
        server.login("发件人","密码")
        server.sendmail(FROM, [TO], BODY)
        server.quit()
        content.close()
    f.close()

if __name__ == '__main__':
    chushihua()
    youjian()
