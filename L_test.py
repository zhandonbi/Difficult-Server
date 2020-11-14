import datetime

from db_operator.load_db import Load
from db_operator.records_db import RecordsDb
from db_operator.item_db import ItemDb
from AIR.SM_load import GCS




if __name__ == '__main__':
    print(1412412414)
    load = Load('cfg/1.json')
    load.load_db_link('cfg/1.json')
    temp = RecordsDb()
    print(temp.cal_all_records())
    load.close()


