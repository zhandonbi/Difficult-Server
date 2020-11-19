# coding=UTF-8

from db_operator.load_db import Load
import datetime


class CanStatusDb(object):
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
        self.table_items = 'Can_status'

    def Can_status_add(self, Can_ID: str, GK152_state: str, GK152_data: str, HCSR04_state: str, HCSR04_distance,
                       LEDBuzzer_1: str, LEDBuzzer_2: str, LEDBuzzer_3: str, LEDBuzzer_4: str, LEDBuzzer_5: str,
                       Time: str):
        '''
        向数据库中添加垃圾桶运行的状态
        :param Can_ID: 垃圾桶编号
        :param GK152_state: 红外对射状态
        :param GK152_data: 红外对射工作状态
        :param HCSR04_state: 超声波状态
        :param HCSR04_distance: 超声波测出的距离
        :param LEDBuzzer_1: 蜂鸣器1状态
        :param LEDBuzzer_2: 蜂鸣器2 状态
        :return:
        '''
        Can_ID = 'IMX6_ENV_RBELONG_001'
        # sql = 'insert into Can_Records(Can_ID,GK152_state,GK152_data,HCSR04_state,HCSR04_distance,LEDBuzzer_1,LEDBuzzer_2,Time) values('"{0}"','"{1}"','"{2}"','"{3}"','"{4}"','"{5}"','"{6}"','"{7}"') '.format(
        #     Can_ID, GK152_state, GK152_data, HCSR04_state, HCSR04_distance, LEDBuzzer_1, LEDBuzzer_2, Time)
        sql = 'insert into Can_status(Can_ID,GK152_state,GK152_data,HCSR04_state,HCSR04_distance,LEDBuzzer_1,LEDBuzzer_2,LEDBuzzer_3,LEDBuzzer_4,LEDBuzzer_5,Time) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}") '.format(
            Can_ID, GK152_state, GK152_data, HCSR04_state, HCSR04_distance, LEDBuzzer_1, LEDBuzzer_2, LEDBuzzer_3,
            LEDBuzzer_4, LEDBuzzer_5, Time)
        self.db_cur.execute(sql)
        self.db_operator.commit()
        return '成功向数据库中添加信息'

    def Can_status_search(self, Can_ID: str):
        """
        通过设备读取到的设备ID
        在数据库中进行搜索
        并返回数据库中当前设备ID的最新一条记录
        :param Can_ID: 设备号
        :return: 返回当前数据中当前设备号的最新一条记录
        """
        result = {}
        sql = 'SELECT * FROM Can_status WHERE Can_ID = "{}"'.format(Can_ID)
        self.db_cur.execute(sql)
        search_results = self.db_cur.fetchall()
        res = Can_ID + "号垃圾桶工作一切正常;\n"
        if len(search_results) != 0:
            print(len(search_results))
            result['Can_ID'] = search_results[len(search_results) - 1][0]
            result['GK152_state'] = search_results[len(search_results) - 1][1]
            result['GK152_data'] = search_results[len(search_results) - 1][2]
            result['HCSR04_state'] = search_results[len(search_results) - 1][3]
            result['HCSR04_distance'] = search_results[len(search_results) - 1][4]
            result['LEDBuzzer_1'] = search_results[len(search_results) - 1][5]
            result['LEDBuzzer_2'] = search_results[len(search_results) - 1][6]
            result['LEDBuzzer_3'] = search_results[len(search_results) - 1][7]
            result['LEDBuzzer_4'] = search_results[len(search_results) - 1][8]
            result['LEDBuzzer_5'] = search_results[len(search_results) - 1][9]
            result['Time'] = search_results[len(search_results) - 1][10]

            for key in result.keys():
                if result[key] == "error":
                    res = Can_ID + "号垃圾桶出现故障\n请联系管理员进行维修;\n"

            res = res + "上次检查时间：" + result['Time']
        else:
            res = '不存在该设备ID的垃圾桶或该垃圾桶尚未有检查记录'
        return res

    def close(self):
        self.db_load.close()
