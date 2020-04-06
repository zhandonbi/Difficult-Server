import io
import numpy as np
from PIL import Image
from tensorflow import keras
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

label_id_name_dict = \
    {
        "0": "其他垃圾/一次性快餐盒",
        "1": "其他垃圾/污损塑料",
        "2": "其他垃圾/烟蒂",
        "3": "其他垃圾/牙签",
        "4": "其他垃圾/破碎花盆及碟碗",
        "5": "其他垃圾/竹筷",
        "6": "厨余垃圾/剩饭剩菜",
        "7": "厨余垃圾/大骨头",
        "8": "厨余垃圾/水果果皮",
        "9": "厨余垃圾/水果果肉",
        "10": "厨余垃圾/茶叶渣",
        "11": "厨余垃圾/菜叶菜根",
        "12": "厨余垃圾/蛋壳",
        "13": "厨余垃圾/鱼骨",
        "14": "可回收物/充电宝",
        "15": "可回收物/包",
        "16": "可回收物/化妆品瓶",
        "17": "可回收物/塑料玩具",
        "18": "可回收物/塑料碗盆",
        "19": "可回收物/塑料衣架",
        "20": "可回收物/快递纸袋",
        "21": "可回收物/插头电线",
        "22": "可回收物/旧衣服",
        "23": "可回收物/易拉罐",
        "24": "可回收物/枕头",
        "25": "可回收物/毛绒玩具",
        "26": "可回收物/洗发水瓶",
        "27": "可回收物/玻璃杯",
        "28": "可回收物/皮鞋",
        "29": "可回收物/砧板",
        "30": "可回收物/纸板箱",
        "31": "可回收物/调料瓶",
        "32": "可回收物/酒瓶",
        "33": "可回收物/金属食品罐",
        "34": "可回收物/锅",
        "35": "可回收物/食用油桶",
        "36": "可回收物/饮料瓶",
        "37": "有害垃圾/干电池",
        "38": "有害垃圾/软膏",
        "39": "有害垃圾/过期药物"
    }


class AIR(object):
    def __init__(self):
        sess = tf.Session()
        self.input_size = 456
        self.model = tf.saved_model.loader.load(
            sess, [tag_constants.SERVING], './AIR/model')
        self.graph = tf.get_default_graph()

    def center_img(self, img, size=None, fill_value=255):
        h, w = img.shape[:2]
        if size is None:
            size = max(h, w)
        shape = (size, size) + img.shape[2:]
        background = np.full(shape, fill_value, np.uint8)
        center_x = (size - w) // 2
        center_y = (size - h) // 2
        background[center_y:center_y + h, center_x:center_x + w] = img
        return background

    def preprocess_img(self, img):
        resize_scale = self.input_size / max(img.size[:2])
        img = img.resize(
            (int(img.size[0] * resize_scale), int(img.size[1] * resize_scale)))
        img = img.convert('RGB')
        img = np.array(img)
        img = img[:, :, ::-1]
        img = self.center_img(img, self.input_size)
        img = img[np.newaxis, :, :, :]
        img = img.astype(img, np.float32) / 225.0
        mean = [0.56719673, 0.5293289, 0.48351972]
        std = [0.20874391, 0.21455203, 0.22451781]
        img[..., 0] -= mean[0]
        img[..., 1] -= mean[1]
        img[..., 2] -= mean[2]
        img[..., 0] /= std[0]
        img[..., 1] /= std[1]
        img[..., 2] /= std[2]
        return img

    def predict(self, image):
        result = {}
        img = self.preprocess_img(image)
        with self.graph.as_default():
            signature_key = 'predict_images'
            # get signature
            signature = self.model.signature_def
            # get tensor name
            in_tensor_name = signature[signature_key].inputs['input_img'].name
            out_tensor_name = signature[signature_key].outputs['output_score'].name
            # get tensor
            input_images = self.sess.graph.get_tensor_by_name(in_tensor_name)
            output_score = self.sess.graph.get_tensor_by_name(out_tensor_name)
            # run
            pred_score = self.sess.run(
                [output_score], feed_dict={input_images: img})

        if pred_score is not None:
            pred_label = np.argmax(pred_score[0], axis=1)[0]
            print(label_id_name_dict[str(pred_label)])
            result = {'result': label_id_name_dict[str(pred_label)]}
        else:
            result = {'result': 'predict score is None'}
        return result
