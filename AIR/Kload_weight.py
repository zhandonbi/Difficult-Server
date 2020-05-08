import io
import numpy as np
from PIL import Image
from keras_efficientnets import EfficientNetB5
from AIR.Groupnormalization import GroupNormalization
from keras.layers import Dense,  Dropout, GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import Nadam

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


def load_model():
    model = EfficientNetB5(weights=None,
                           include_top=False,
                           input_shape=(456, 456, 3),
                           classes=40,
                           pooling=max)
    for i, layer in enumerate(model.layers):
        if "batch_normalization" in layer.name:
            model.layers[i] = GroupNormalization(groups=32, axis=-1, epsilon=0.00001)
    x = model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    predictions = Dense(40, activation='softmax')(x)  # activation="linear",activation='softmax'
    model = Model(input=model.input, output=predictions)
    optimizer = Nadam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.004)
    # optimizer = SGD(lr=FLAGS.learning_rate, momentum=0.9)
    objective = 'categorical_crossentropy'
    metrics = ['accuracy']
    model.compile(loss=objective, optimizer=optimizer, metrics=metrics)
    model.load_weights('AIR/HDF5/weights_028_0.5235.h5')
    print('模型完成载入')
    return model


Kmodel = load_model()


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
    img = Image.open(img)
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
    return img


def run(image):
    image = preprocess_img(image)
    result = kmodel.predict(image)
    return result
