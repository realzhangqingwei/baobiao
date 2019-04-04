# -*- coding: utf-8 -*-
import linecache
from module.log import *
##################################################################################
class do_file(object):
    def get_info(self, file):
        lines = linecache.getlines(file)
        logger.info("lines的值是 %s." % lines)
        line = len(lines)
        logger.info("lines的长度是 %d."  % line)
        if line > 3:
            for i in range(line):
                if 'mysqllog' in lines[i]:
                    logger.info("mysqllog所在的行是  %s" % i)
                    mysqllog = lines[i-1].strip().split()[0]
                    logger.info("mysqlllog实际入库数是 %s" % mysqllog)
                    total = lines[i+1].strip()
                    logger.info("mysqllog总的日志数是 %s" % total)
                    dbname = file.split("/")[-1].split(".")[0]
                    logger.info("客户数据库的名字是 %s." % dbname)
                    diff = int(total) - int(mysqllog)
                    logger.info("总的和入库的差值是 %s."  % diff)
                    date = lines[i-2].split(".")[1]
                    logger.info("倒库的日期是  %s." % date)
        elif line == 3:
            for i in range(line):
                if 'mysqllog' in lines[i]:
                    logger.info("mysqllog所在的行数是 %s." % i)
                    mysqllog = lines[i-1].split()[0].strip()
                    logger.info("mysqlllog实际入库数是 %s" % mysqllog)
                    total = lines[i+1].strip()
                    logger.info("mysqllog总的日志数是 %s" % total)
                    diff = int(total) - int(mysqllog)
                    logger.info("总的和入库的差值是 %s."  % diff)
                    date = lines[i-1].split(".")[1]
                    logger.info("倒库的日期是  %s." % date)
                    dbname = file.split("/")[-1].split(".")[0]

        else:
            mysqllog = 0
            total = 0
            dbname = dbname = file.split("/")[-1].split(".")[0]
            diff = 0
            date = "unknow"
            logger.info("mysqlllog实际入库数是 0.")
            logger.info("mysqllog总的日志数是 0.")
            logger.info("倒库的日期不确定 %s." % date)
        return total, mysqllog, dbname, diff, date


