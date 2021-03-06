# coding=UTF-8

from db_operator.load_db import Load
import datetime


class RecordsDb(object):
    """
    1可回收垃圾
    2其他垃圾
    3有害垃圾
    4厨余垃圾
    """

    def __init__(self):
        """
        在此类初始化时就已经自动连接目标数据库
        """
        self.db_load = Load('cfg/RcDb.json')
        # db_operator是pymysql库中pymysql.connect()的返回对象
        self.db_operator = self.db_load.get_DB_operator()
        # db_cur与pymysql库中cursor用法完全一致
        self.db_cur = self.db_load.get_DB_cur()
        self.table_items = 'Can_Records'

    def records_add(self, Can_ID: str, Rubbish_Class: int, Time: str):
        """
        向数据库添加物品条目
        :param Can_ID: 垃圾桶编号
        :param Rubbish_Class: 此参数类型为字典为垃圾所属类别
        :param Time：程序运行时的时间
        :return: 添加条目的信息
        """
        Can_ID = 'IMX6_ENV_RBELONG_001'
        sql = 'insert into Can_Records(Can_ID,Rubbish_Class,Time) values("{0}",{1},"{2}") '.format(Can_ID, Rubbish_Class,
                                                                                                 Time)
        self.db_cur.execute(sql)
        self.db_operator.commit()
        return '成功向数据库中添加如下信息：{{Can_ID:{0},Rubbish_Class:{1},Time:{2}}}\n'.format(Can_ID, Rubbish_Class, Time)

    def records_search(self, Can_ID: str):
        """
        通过设备读取到的设备ID
        在数据库中进行搜索
        并返回数据库中当前设备ID的最新一条记录
        :param Can_ID: 设备号
        :return: 返回当前数据中当前设备号的最新一条记录
        """
        result = {}
        sql = 'SELECT * FROM Can_Records WHERE Can_ID = "{}"'.format(Can_ID)
        self.db_cur.execute(sql)
        search_results = self.db_cur.fetchall()
        if len(search_results) != 0:
            result['Can_ID'] = search_results[len(search_results) - 1][0]
            result['ClassID'] = int(search_results[len(search_results) - 1][1])
            result['Time'] = search_results[len(search_results) - 1][2]
        else:
            return '不存在该设备ID的垃圾桶或该垃圾桶尚未有工作记录'
        rubbishclass = ""
        if result['ClassID'] == 1:
            rubbishclass = "可回收垃圾"
        elif result['ClassID'] == 2:
            rubbishclass = "其他垃圾"
        elif result['ClassID'] == 3:
            rubbishclass = "有害垃圾"
        elif result['ClassID'] == 4:
            rubbishclass = "厨余垃圾"
        res = Can_ID + "号设备:\n上一次工作结果为:" + rubbishclass + "\n上次工作时间为:" + result['Time']
        return res

    def cal_same_rubbish_class(self, Rubbish_Class: int):
        """

        :return:
        """
        sql = 'SELECT * FROM Can_Records WHERE Rubbish_Class = {}'.format(Rubbish_Class)
        self.db_cur.execute(sql)
        search_results = self.db_cur.fetchall()
        result = str(len(search_results))
        return result

    def cal_all_records(self):
        """

        :return: 数据库中所有同类的信息
        """
        class1 = self.cal_same_rubbish_class(1)
        class2 = self.cal_same_rubbish_class(2)
        class3 = self.cal_same_rubbish_class(3)
        class4 = self.cal_same_rubbish_class(4)
        res = "当前数据库中:\n可回收垃圾的记录的数目为:" + class1 + " 条\n其它垃圾的记录的数目为:" + class2 + " 条\n有害垃圾的记录的数目为:" + class3 + " 条\n厨余垃圾的记录的数目为:" + class4 + " 条"
        return res

    def close(self):
        self.db_load.close()
