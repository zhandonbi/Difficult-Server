#! -*- coding: utf-8 -*-
import io
import os
import numpy as np
from PIL import Image
from keras_efficientnets import EfficientNetB5
from AIR.Groupnormalization import GroupNormalization
from keras.layers import Dense, Dropout, GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import Nadam
from db_operator.item_db import ItemDb
import tensorflow as tf
from keras import backend
from keras.optimizers import adam, Nadam
import shutil


def load_model():
    num_classes = 50
    model = EfficientNetB5(weights=None,
                           include_top=False,
                           input_shape=(456, 456, 3),
                           classes=num_classes,
                           pooling=max)
    for i, layer in enumerate(model.layers):
        if "batch_normalization" in layer.name:
            model.layers[i] = GroupNormalization(groups=32, axis=-1, epsilon=0.00001)
    x = model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation='softmax')(x)  # activation="linear",activation='softmax'
    model = Model(input=model.input, output=predictions)
    optimizer = Nadam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.004)
    # optimizer = SGD(lr=FLAGS.learning_rate, momentum=0.9)
    objective = 'categorical_crossentropy'
    metrics = ['accuracy']
    model.compile(loss=objective, optimizer=optimizer, metrics=metrics)
    model.load_weights('AIR/HDF5/res.h5')
    print('模型完成载入')
    return model


global graph, Kmodel
Kmodel = load_model()
#graph = tf.get_default_graph()

def get_SM():
    model = load_model()
    signature = tf.saved_model.signature_def_utils.predict_signature_def(
        inputs={'input_img': model.input}, outputs={'output_score': model.output})
    builder = tf.saved_model.builder.SavedModelBuilder('AIR/model')
    legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
    builder.add_meta_graph_and_variables(
        sess=backend.get_session(),
        tags=[tf.saved_model.tag_constants.SERVING],
        signature_def_map={
            'predict_images': signature,
        },
        legacy_init_op=legacy_init_op)
    builder.save()


def center_img(img, size=None, fill_value=255):
    h, w = img.shape[:2]
    if size is None:
        size = max(h, w)
    shape = (size, size) + img.shape[2:]
    background = np.full(shape, fill_value, np.uint8)
    center_x = (size - w) // 2
    center_y = (size - h) // 2
    background[center_y:center_y + h, center_x:center_x + w] = img
    return background


def preprocess_img(img):
    resize_scale = 456 / max(img.size[:2])
    img = img.resize(
        (int(img.size[0] * resize_scale), int(img.size[1] * resize_scale)))
    img = img.convert('RGB')
    img = np.array(img)
    img = img[:, :, ::-1]
    img = center_img(img, 456)
    img = img[np.newaxis, :, :, :]
    img = np.asarray(img, np.float32) / 255.0
    mean = [0.56719673, 0.5293289, 0.48351972]
    std = [0.20874391, 0.21455203, 0.22451781]
    img[..., 0] -= mean[0]
    img[..., 1] -= mean[1]
    img[..., 2] -= mean[2]
    img[..., 0] /= std[0]
    img[..., 1] /= std[1]
    img[..., 2] /= std[2]
    print('图像处理完成')
    return img


def AImage(image):
    result = {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
    image = preprocess_img(image)
    with graph.as_default():
        pred_score = Kmodel.predict(image)
        if pred_score is not None:
            pred_label = np.argmax(pred_score[0])
            db = ItemDb()
            label_id_name_dict = \
                {
                    "0": "一次性快餐盒",
                    "1": "污损塑料",
                    "2": "烟蒂",
                    "3": "牙签",
                    "4": "破碎花盆及碟碗",
                    "5": "竹筷",
                    "6": "剩饭剩菜",
                    "7": "大骨头",
                    "8": "水果果皮",
                    "9": "水果果肉",
                    "10": "茶叶渣",
                    "11": "菜叶菜根",
                    "12": "蛋壳",
                    "13": "鱼骨",
                    "14": "充电宝",
                    "15": "包",
                    "16": "化妆品瓶",
                    "17": "塑料玩具",
                    "18": "塑料碗盆",
                    "19": "塑料衣架",
                    "20": "快递纸袋",
                    "21": "插头电线",
                    "22": "旧衣服",
                    "23": "易拉罐",
                    "24": "枕头",
                    "25": "毛绒玩具",
                    "26": "洗发水瓶",
                    "27": "玻璃杯",
                    "28": "皮鞋",
                    "29": "砧板",
                    "30": "纸板箱",
                    "31": "调料瓶",
                    "32": "酒瓶",
                    "33": "金属食品罐",
                    "34": "锅",
                    "35": "食用油桶",
                    "36": "饮料瓶",
                    "37": "干电池",
                    "38": "软膏",
                    "39": "过期药物"
                }
            result = db.item_search_exact(label_id_name_dict[str(pred_label)])
            db.close()
        else:
            result = {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
    return result
