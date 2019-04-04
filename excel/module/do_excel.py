# -*- coding: utf-8 -*-
import xlsxwriter
from xlrd import open_workbook
from xlutils.copy import copy
import pandas as pd
from module.log import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class do_excel(object):
    #def __init__(self, name):
    #    self.name = name
    def c_excel(self, name):
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(name)
        worksheet = workbook.add_worksheet()
        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)

        # Add a bold format to use to highlight cells.
        #bold = workbook.add_format({'bold': True})
        bold = workbook.add_format()
        bold.set_bold()

        # Write some simple text.
        worksheet.write('A1', u'网站',bold)
        worksheet.write('B1', u'DB',bold)
        worksheet.write('C1', u'总的日志数',bold)
        worksheet.write('D1', u'入库日志数',bold)
        worksheet.write('E1', u'差值',bold)
        worksheet.write('F1', u'客户倒库日志日期',bold)
        workbook.close()
        return name

    def insert_excel(self, name, website, db, total, mysqllog, diff, date):
        ##  操作excle表格
        r_xls = open_workbook(name) # 读取excel文件
        row = r_xls.sheets()[0].nrows # 获取已有的行数
        logger.info("xlsx表格现在有的行数是 %s." % row)
        excel = copy(r_xls) # 将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0) # 获取要操作的sheet

        #对excel表追加一行内容
        table.write(row, 0, website) #括号内分别为行数、列数、内容
        table.write(row, 1, db)
        table.write(row, 2, total)
        table.write(row, 3, mysqllog)
        table.write(row, 4, diff)
        table.write(row, 5, date)
        excel.save(name) # 保存并覆盖文件
        return name, website, db, total, mysqllog, diff, date
    def cat_excel(self, name):
        df = pd.read_excel(name)
        return df
