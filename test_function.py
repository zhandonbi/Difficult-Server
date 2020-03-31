# 此文件用来测试每个功能模块
# 为防止文件路径以及其它问题，请在此文件内测试您的功能模块
from db_operator.item_db import ItemDb
from ASR.ASR import ASR

if __name__ == '__main__':
    print('正在运行功能测试，注意不要使用在正式环境中')
    IT = ItemDb()

    print(IT.items_read_all('0'))