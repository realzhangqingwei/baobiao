# -*- coding: utf-8 -*-
# 操作excle文件
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'module'))
from module.log import *
import datetime
import time
from module.do_excel import do_excel
from module.do_custer import do_custer
from module.do_file import do_file
from module.util import util
################################################################################### #
# 基本目录初始化
dc=do_custer()
foler_list=['logs', 'backup', 'excel', 'html']
foler_do =[dc.init_folder(i) for i in foler_list]
logger.info("需要创建的文件名字是 %s." % foler_list)
logger.info("foler_do的值是 %s." % foler_do)

## 生成且初始化excel表格
in_excel = do_excel()
name = in_excel.c_excel(os.path.join(BASE_DIR,"excel", "test.xlsx"))
logger.info("生成的excel表格的名字是 %s." % name)

riqi = time.strftime("%Y%m%d")
logger.info("riqi的值是 %s."  % riqi)
pwd_log = dc.cd_logs(foler_do[0], riqi)
logger.info("pwd_log的值是 %s."  % pwd_log)
conf=os.path.join(BASE_DIR, 'kehu.txt')
db=dc.wget_url(conf, os.path.join(BASE_DIR,pwd_log))
logger.info("db的名字是 %s."  % db)
dc.rm_backup(BASE_DIR, riqi)
for list in os.listdir(os.path.join(BASE_DIR,"logs",riqi)):
    logger.info("列出的文件是 %s." % list)
    dfile=do_file()
    total, mysqllog, dbname,diff, date = dfile.get_info(list)
    try:
        in_excel.insert_excel(name, "website", dbname, total, mysqllog, diff, date)
    except Exception,e:
        logger.info("追加进excel中出现错误 %s." % e)

## 往表格中插入数据
in_excel.insert_excel(name, 'website1', 'db1', '200', '200', 'diff1', '2019-04-02')
in_excel.insert_excel(name, 'website1', 'db1', '100', '100', 'diff1', '2019-04-02')

##按照某列排序且转化excel表格成html文件
e_h=util()
e_h.sort_excel(name)
e_h.excel_to_html(name, os.path.join(BASE_DIR, "html", "report.html"))

##发送邮件
e_h.send_mail(os.path.join(BASE_DIR, "html", "report.html"), riqi )
## 查看excel表格
logger.info("excel文件的路径是 %s."  % name)
l1=in_excel.cat_excel(name)
logger.info("表格的内容是 %s." % l1)
