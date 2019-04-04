# -*- coding: utf-8 -*-

import pandas
import  codecs
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from module.log import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class util(object):
    def excel_to_html(self, excel, html):
        xd = pandas.ExcelFile(excel)
        df = xd.parse(xd.sheet_names[0], head=None, keep_default_na=True)
        with codecs.open(html,"w","utf-8") as html_fil:
            html_fil.write(df.to_html(header=True, index=True,))
    def sort_excel(self,file):
        data = pandas.read_excel(file)
        df=data.sort_values(by=[u'总的日志数'], ascending=False)
        df1=df.reset_index(drop=True)
        df1.to_excel(file)
    def send_mail(self, file, date):
        HOST = "smtp.163.com"  #用的163邮箱发送的
        SUBJECT = u"客户昨天日志报表分析表" + '.' + date
        TO = [收件人,]  #是以列表的形式存在的
        FROM = "发件人"
        report = open(file,'rb').read()
        msg = MIMEText(report,"html","utf-8")
        msg['Subject'] = Header(SUBJECT,'utf-8')
        msg['From']=self._format_addr('显示的发件人的名字 <%s>' % FROM)
        msg['To']=";".join(TO)
        try:
            server = smtplib.SMTP()
            server.connect(HOST,"25")
            server.starttls()
            server.login("发件人","密码")
            server.sendmail(FROM, TO, msg.as_string())
            server.quit()
            logger.info("邮件发送成功!")
        except Exception, e:
            logger.info("邮件发送出现异常! %s."  % e)

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
