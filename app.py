# coding=UTF-8
from flask import Flask, request, send_from_directory
from db_operator.item_db import ItemDb
from PIL import Image
from ASR.ASR import ASR
from AIR.Kload_weight import *
import json
import random
import os
import base64
import threading

global lock

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# air = AIR()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11233, threaded=False)


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
    result = {}
    if request.method == 'POST':
        item_key = request.form['item_key']
        item = ItemDb()
        result = item.items_search_vague(item_key)
        item.close()
    else:
        result = {'接口返回示例': {'items_num': 22,
                             '667': {'Name': '鸡蛋包装盒', 'CLassID': '1'},
                             '668': {'Name': '鸡蛋盒', 'CLassID': '1'},
                             '670': {'Name': '鸡蛋盒包装', 'CLassID': '1'},
                             '675': {'Name': '鸡蛋塑料保护壳', 'CLassID': '1'},
                             '1313': {'Name': '塑料鸡蛋盒', 'CLassID': '1'},
                             '1880': {'Name': '包裹着鸡蛋壳的餐巾纸', 'CLassID': '1'}},
                  '如果您发出的物品不存在': {'item_num': 0},
                  }
    return result


@app.route('/asr_search/', methods=['GET', 'POST'])
def asr_search():
    result = {}
    if request.method == 'POST':
        talk_text = request.form['talk_text']
        result = ASR(talk_text)
    else:
        result = {'接口返回示例': {'鸡蛋': {'ID': 5249, 'Name': '鸡蛋', 'ClassID': 4},
                             '垃圾袋': {'ID': 2668, 'Name': '垃圾袋', 'ClassID': 2}},
                  '如果您发出的物品名不存在': {}
                  }
    return result


@app.route('/get_all_item/', methods=['GET', 'POST'])
def get_all_item():
    result = {}
    if request.method == 'POST':
        class_ID = request.form['class_ID']
        item = ItemDb()
        result = item.items_read_all(class_ID)
        item.close()
    else:
        result = {'接口返回示例': {'items_num': 665,
                             '3958': {'Name': '1号电池', 'CLassID': '3'},
                             '3959': {'Name': '502胶水', 'CLassID': '3'},
                             '3960': {'Name': '5号电池', 'CLassID': '3'},
                             '3961': {'Name': '704粘合剂', 'CLassID': '3'},
                             '3962': {'Name': '7号电池', 'CLassID': '3'}},
                  '如果您发出的ID异常': {}
                  }
    return result


@app.route('/air_search/', methods=['GET', 'POST'])
def air_search():
    result = {}
    if request.method == 'POST':
        if request.files.get("item_picture"):
            img = request.files.get('item_picture')
            img_b64encode = base64.b64encode(img.read())  # base64编码
            img_b64decode = base64.b64decode(img_b64encode)  # base64解码
            image = io.BytesIO(img_b64decode)
            result = AImage(Image.open(image))
        else:
            result = {'ID': -1, 'Name': '未检测到图片', 'classID': -1}
        print(result)
    else:
        result = {'ID': -1, 'Name': '测试用例', 'classID': -1}
    return result


@app.route('/update_version/', methods=['GET', 'POST'])
def update_version():
    if request.method == 'POST':
        with open('./Update/version.json') as f:
            version = json.load(f)
        return version
    else:
        return send_from_directory(directory="./Update/", filename="RBelong.apk", as_attachment=True)
