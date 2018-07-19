#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import smtplib
import string
import shutil
import  os
import time
import datetime
import linecache
import xlsxwriter
import pandas
import  codecs
from email.mime.text import MIMEText
###################################################################################
def chushihua():
    os.chdir('/home/python/test/test/logs/')
    riqi = time.strftime("%Y%m%d")
    try:
        shutil.rmtree(riqi)
    except:
        print "Nothing to be done"
    os.mkdir(riqi)
    os.chdir(riqi)

def youjian():
    f = open('/home/python/test/test/kehu.txt','r+')
    for url in f:
        try:
            #wget.download(url)
            os.environ['url'] = str(url)
            print "开始下载: %s" % url
            os.popen("wget -c -t2 -T5 $url")
            print "oops，下载完成"
        except:
            print "糟糕，下载出错,没有抓到"

    try:
        os.system("rm -f /home/python/test/test/backup/`date -d last-day +%Y-%m-%d`.txt")
    except:
        print "没有内容，你删个啥"
    for list in  os.listdir('.'):
        content = open(list, 'r+')
        #shell用python变量
        os.environ['list'] = str(list)
        print list
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=-1)
        d1 = yes_time.strftime('%Y-%m-%d')
        print d1
        os.environ['d1'] = str(d1)
        try:
            a1 = os.system("cat  $list|grep -A 1 -B 2 ^mysqllog|grep -A 3 $d1 >> /home/python/test/test/backup/$d1.txt")
            if a1 == 0:
               os.popen("echo -- >> /home/python/test/test/backup/$d1.txt")
               print "追加文件成功 %s" % list
            else:
               print "没抓到我就不加啦 %s" % list
        except:
            print "糟糕，追加文本失败 %s" % list
        #print d1.txt
#    f.close()


def excel():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    yes_time_nyr = yes_time.strftime('%Y-%m-%d')
    file_name = '/home/python/test/test/backup/' + yes_time_nyr + '.' + 'txt'
    os.chdir("/home/python/test/test/excel/")
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('mysqllog.xlsx')
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)

    # Add a bold format to use to highlight cells.
    #bold = workbook.add_format({'bold': True})
    bold = workbook.add_format()
    bold.set_bold()

    # Write some simple text.
    worksheet.write('A1', u'客户名',bold)
    worksheet.write('B1', u'总的日志数',bold)
    worksheet.write('C1', u'入库日志数',bold)
    worksheet.write('D1', u'差值',bold)
    worksheet.write('E1', u'客户倒库日志日期',bold)
    worksheet.write('E2', yes_time_nyr, bold)
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    j = 2
    count = len(open(file_name).readlines())
    #print count

    for i in range(1,count,5):
        pname=linecache.getline(file_name,i)
        ptotal=linecache.getline(file_name,i+1)
        pmysqllog=linecache.getline(file_name,i+3)
        try:
            name = pname.strip().split('.')[0].split()[1]
            total = ptotal.strip().split()[0]
            mysqllog = pmysqllog.strip().split('.')[0]
            try:
                diff = int(total) - int(mysqllog)
            except:
                diff = 0
            print "Name is %s" % name
            print "Total is %s" % total
            print "Mysqllog is %s" % mysqllog
            print "Diff is %s"  % diff
            worksheet.write(A + str(j), str(name), bold)
            worksheet.write(B + str(j), int(total))
            worksheet.write(C + str(j), int(mysqllog))
            worksheet.write(D + str(j), int(diff))
            j = j + 1
            print "J is %d" % j
            print "==================================================================================================================================================="
        except:
            print "something is wrong"
    workbook.close()

def html():
    os.chdir("/home/python/test/test/html/")
    xd = pandas.ExcelFile('/home/python/test/test/excel/mysqllog.xlsx')
    df = xd.parse(xd.sheet_names[0], head=None, keep_default_na=True)
    with codecs.open("report.html","w","gb2312") as html_fil:
            html_fil.write(df.to_html(header=True, index=True,))

def mail():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    yes_time_nyr = yes_time.strftime('%Y-%m-%d')
    HOST = "smtp.exmail.qq.com"
    SUBJECT = u"客户昨天日志报表分析表" + '.' + yes_time_nyr
    TO = "收件人信息"
    FROM = "发件人信息"
    report = open('/home/python/test/test/html/report.html','rb').read()
    msg = MIMEText(report,"html","gb2312")
    msg['Subject'] = SUBJECT
    msg['From']=FROM
    msg['To']=TO
    try:
        server = smtplib.SMTP()
        server.connect(HOST,"25")
        server.starttls()
        server.login("发件人信息","密码")
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print "邮件发送成功！"
    except Exception, e:
        print "失败："+str(e)


def main():
    chushihua()
    youjian()
    excel()
    html()
    mail()

if __name__ == '__main__':
    main()
