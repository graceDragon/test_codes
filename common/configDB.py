# coding:utf-8

import pymysql
import readConfig as readConfig
from .Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class MyDB:
    global host, username, password, port, database, config
    host = localReadConfig.get_db("host")
    username = localReadConfig.get_db("username")
    password = localReadConfig.get_db("password")
    port = localReadConfig.get_db("port")
    database = localReadConfig.get_db("database")
    config = {
        'host': str(host),
        'user': username,
        'passwd': password,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectDB(self):
        """
        connect to database
        :return:
        """
        try:
            # connect to DB
            self.db = pymysql.connect(**config)
            # create cursor
            self.cursor = self.db.cursor()
            print "Connect DB successfully! 连接数据库成功！"
        except Exception as ex:
            print "连接数据库失败"
            self.logger.error(str(ex))
            assert True is False

    def executeSQL(self, sql):
        """
        execute sql
        :param sql:
        :return:
        """
        self.connectDB()
        # executing sql
        print "执行sql语句"
        self.cursor.execute(sql)
        # executing by committing to DB
        self.db.commit()
        # 返回执行的结果
        return self.cursor

    def get_all(self, cursor):
        """
        get all testResult after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        get one testResult after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("Database closed!")
# --------------------智寓测试环境数据库执行----------------

    def zhiyu_yzm(self, sql):
        cursor = self.executeSQL(sql)
        result = self.get_one(cursor)  # 返回元组格式
        result = result[0]  # 转成字符串
        print '读取的值：', result, '类型', type(result)
        return result

    def zhiyu_getone(self, sql):
        cursor = self.executeSQL(sql)
        result = self.get_one(cursor)  # 返回元组格式
        result = result[0]  # 转成字符串
        print '读取的值：', result
        return result

    def zhiyu_delete(self, sql):
        self.executeSQL(sql)

    def zhiyu_run_sql(self, sql):
        self.executeSQL(sql)






