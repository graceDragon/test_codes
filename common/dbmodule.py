# coding=utf-8

"""
    mysql数据库操作
    Created on 2017/11/15
    @author: Liu Yuliang
"""

import MySQLdb
from warnings import filterwarnings
# import cx_Oracle
filterwarnings('error', category=MySQLdb.Warning)


class MySQL(object):
    """
        MYSQL数据库操作类
    """
    __conn = None
    __cursor = None

    def __init__(self, name, user, password, host, port):
        try:
            self.__conn = MySQLdb.connect(db=name, user=user, passwd=password, host=host, port=int(port),
                                          charset='utf8')
            self.__cursor = self.__conn.cursor()
            print '初始化完成!'
        except MySQLdb.Warning, war:
            print '警告信息: %s' % str(war)
        except MySQLdb.Error, err:
            print '错误信息: %d %s' % (err.args[0], err.args[1])

    def insert(self, table, data_dict):
        """
            插入数据
            eg: insert into 'table1'('key1', 'key2') values('value1', 'value2')
        :param table: 数据表
        :param data_dict: 数据内容
        :return: last_id
        """
        if len(data_dict) == 0:
            print '插入数据为空!'
            return False
        keys = data_dict.keys()
        print keys
        key_str = ''
        variate = ''
        value_list = []
        for key in keys:  # 拼接字符串
            key_str += ''.join(('`', str(key), '`,'))
            value_list.append(data_dict[key])
            variate += '%s,'
        # print s
        key_str = key_str.rstrip(',')  # 去除字符串最后的','
        variate = variate.rstrip(',')
        sql = ''.join(("INSERT INTO ", str(table), "(", key_str, ") VALUES", "(", variate, ")"))
        print '执行插入的语句: %s' % sql
        try:
            self.__cursor.execute(sql, tuple(value_list))
            last_id = self.__cursor.lastrowid
            self.__conn.commit()
            return last_id
        except Exception, err:
            print err
            print '插入数据异常!执行回滚!'
            self.__conn.rollback()
            return False

    def fetchone(self, table, fields='*', where='', order='id desc'):
        """
            查询一条数据
        :param table: 表名
        :param fields: 查询字段,默认为所有
        :param where: 查询条件
        :param order: 排序方式
        :return: 查询结果
        """
        sql = ''.join(('select ', str(fields), ' from ', str(table), ' where '))
        if where != '':
            sql = ''.join((sql, str(where)))
        sql = ''.join((sql, 'order by ', str(order)))
        print '执行的查询语句: %s' % sql
        try:
            self.__cursor.execute(sql)
            return self.__cursor.fetchone()
        except:
            print '查询失败!'
            return False

    def fetchmany(self, table, fields='*', where='', order='id desc', limit=20):
        """
            查询多条数据
        :param table: 表名
        :param fields: 查询字段
        :param where: 查询条件
        :param order: 排序条件
        :param limit: 限制的结束值
        :return:  设定的查询结果
        """
        sql = ''.join(('select', str(fields), ' from `', str(table), '` '))
        if where != '':
            sql = ''.join((sql, str(where)))
        sql = ''.join((sql, 'order by ', str(order)))
        print "查询多条执行的语句: %s" % sql
        try:
            self.__cursor.execute(sql)
            return self.__cursor.fetchmany(limit)
        except:
            print '查询失败!'
            return False

    def fetchall(self, table, fields='*', where='', order='id desc'):
        """
            查询所有的数据
        :param table: 数据表
        :param fields: 查询字段
        :param where: 查询条件
        :param order: 排列顺序
        :return:  所有的查询数据
        """
        sql = ''.join(('select ', str(fields), ' from `', str(table), '` '))
        if where != '':
            sql = ''.join((sql, str(where)))
        sql = ''.join((sql, 'order by ', str(order)))
        print "查询的语句: %s" % sql
        try:
            self.__cursor.execute(sql)
            return self.__cursor.fetchall()
        except:
            print '查询失败!'
            return False

    def delete(self, table, where, limit=1):
        """
            删除数据
        :param table:
        :param where:
        :param limit:
        :return:
        """
        sql = ''.join(('delete from ', str(table), ' where ', str(where)))
        if limit > 0:
            sql = ''.join((sql, ' limit ', str(limit)))
        print "执行的语句: %s" % sql
        try:
            self.__cursor.execute(sql)
            self.__conn.commit()
            # return self.__cursor.fetchall()
            return True
        except:
            print '删除异常!执行回滚!'
            self.__conn.rollback()
            return False

    def update(self, table, update_data_dict, where):
        """
            更新数据
        :param table:  表名
        :param update_data_dict: 更新数据
        :param where:  查询条件
        :return:  空
        """
        keys = update_data_dict.keys();
        update_str = ''
        for key in keys:  # 拼接字符串
            update_str += ''.join(( str(key), ' = "', str(update_data_dict[key]), '",'))
        update_str = update_str.rstrip(',')  # 去除字符串最后的','
        sql = ''.join(("update ", str(table), " set ", update_str, " where ", where))
        print '执行插入的语句: %s' % sql
        try:
            self.__cursor.execute(sql)
            self.__conn.commit()
            return True
        except:
            print '更新数据异常!执行回滚!'
            self.__conn.rollback()
            return False

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()

# class Oracle(object):
#     """
#         Oracle数据库操作
#     """
#     def __init__(self, dbname, username, password, ipadr, port):
#         try:
#             self.db = cx_Oracle.connect(username, password, ipadr + ':' + port + '/' + dbname)
#             self.cursor = self.db.cursor()
#             print '连接数据库成功！'
#         except:
#             print '数据库连接失败！'
#
#     def update(self, table, update_data_dict, where):
#         """
#             更新数据
#         :param table:  表名
#         :param update_data_dict: 更新数据
#         :param where:  查询条件
#         :return:  空
#         """
#         keys = update_data_dict.keys();
#         update_str = ''
#         for key in keys:  # 拼接字符串
#             update_str += ''.join((str(key), ' = "', str(update_data_dict[key]), '",'))
#         update_str = update_str.rstrip(',')  # 去除字符串最后的','
#         sql = ''.join(("update ", str(table), " set ", update_str, " where ", where))
#         print '执行插入的语句: %s' % sql
#         try:
#             self.cursor.execute(sql)
#             self.db.commit()
#             return True
#         except:
#             print '更新数据异常!执行回滚!'
#             self.db.rollback()
#             return False
#
#     def delete(self, table, where):
#         """
#             删除数据
#         :param table:
#         :param where:
#         :param limit:
#         :return:
#         """
#         sql = ''.join(('delete from ', str(table), ' where ', str(where)))
#         print "执行的语句: %s" % sql
#         try:
#             self.cursor.execute(sql)
#             self.db.commit()
#             return True
#         except:
#             print '删除异常!执行回滚!'
#             self.db.rollback()
#             return False
#
#
#     def __del__(self):
#         self.cursor.close()
#         self.db.close()

if __name__ == '__main__':
    pass
#     from gome import interface_settings
#
#     db_info = interface_settings.DATABASE['default']
#     print db_info
#     s = MySQL(**db_info)
#     # print s.fetchall('product')
#     # print s.fetchmany('product',limit=2)
#     # print s.fetchone('product')
#     insert_data_dict = {
#         'id_no': 'test',
#         'name': 'test',
#         'status': '1',
#         'pub_date': '2016-11-7 10:20:00',
#         'mod_date': '2016-11-7 10:20:00',
#
#     }
#     # print s.insert('product', data_dict=insert_data_dict)
#     s.update('product', insert_data_dict,'id=6')
#     print s.fetchone('product')
