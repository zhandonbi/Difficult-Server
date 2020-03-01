# coding=UTF-8
from flask import Flask, request
from db_operator.item_db import ItemDb
from ASR.ASR import ASR

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)


# 此行以下编辑你的代码
@app.route('/get_classID/', methods=['GET'])
def get_classID():
    return {
        '1': '可回收垃圾',
        '2': '其他垃圾',
        '3': '有害垃圾',
        '4': '厨余垃圾'
    }

@app.route('/exact_search/', methods=['GET', 'POST'])
def exact_search():
    result = {}
    if request.method == 'POST':
        item_name = request.form['item_name']
        item = ItemDb()
        result = item.item_search_exact(item_name)
        item.close()
    else:
        result = {'接口返回示例': {'ID': 5249, 'Name': '鸡蛋', 'ClassID': 4},
                  '如果您发出的物品名不存在': {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
                  }
    return result

@app.route('/exact_search_ID/', methods=['GET', 'POST'])
def exact_search_ID():
    result = {}
    if request.method == 'POST':
        item_ID = request.form['item_ID']
        item = ItemDb()
        result = item.item_search_exact_ID(item_ID)
        item.close()
    else:
        result = {'接口返回示例': {'ID': 5249, 'Name': '鸡蛋', 'ClassID': 4},
                  '如果您发出的物品名不存在': {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
                  }
    return result

@app.route('/vague_search/', methods=['GET', 'POST'])
def vague_search():
    pass