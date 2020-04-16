import base64, requests, json
from db_operator.item_db import ItemDb


def temp_AIR(image):
    url = 'http://api.tianapi.com/txapi/imglajifenlei/index'
    key = '6fda4f8543d58907405dc57896532b64'
    headers = 'Content-Type: application/x-www-form-urlencoded'
    post_image = str(base64.b64encode(image), encoding='utf-8')
    datas = {
        'key': key,
        'img': post_image
    }
    res = requests.post(url=url, data=datas).text
    # res = '{"code":200,"msg":"success","newslist":[{"name":"塑料盒","trust":73,"lajitype":0,"lajitip":"塑料盒是可回收垃圾，常见包括各类废金属、玻璃瓶、饮料瓶、电子产品等。投放时应注意轻投轻放、清洁干燥、避免污染。"},{"name":"手机后盖","trust":50,"lajitype":4,"lajitip":"手机后盖的垃圾分类系统暂时无法判别，请重新尝试拍摄物体的主要特征。"},{"name":"平板手机","trust":33,"lajitype":0,"lajitip":"平板手机是可回收垃圾，常见包括各类废金属、玻璃瓶、饮料瓶、电子产品等。投放时应注意轻投轻放、清洁干燥、避免污染。"},{"name":"一次性餐具","trust":16,"lajitype":3,"lajitip":"一次性餐具是其它干垃圾，常见包括砖瓦陶瓷、卫生间废纸、猫砂、毛发、一次性制品等。投放时应尽量沥干水分、平整轻放。"},{"name":"包装袋\/盒","trust":1,"lajitype":4,"lajitip":"包装袋\/盒的垃圾分类系统暂时无法判别，请重新尝试拍摄物体的主要特征。"}]}'
    get_res = json.loads(res)
    result = {}
    if int(get_res['code']) == 200:
        item_list = list(get_res['newslist'])
        i = 0
        for item in item_list:
            if i >= 3:
                break
            ClassID = int(item['lajitype'])
            if ClassID == 0:
                ClassID = 1
            elif ClassID == 1:
                ClassID = 3
            elif ClassID == 2:
                ClassID = 4
            elif ClassID == 3:
                ClassID = 2
            temp = {
                'ClassID': ClassID,
                'Name': item['name']
            }
            result[str(i)] = temp
            i +=1
        print(res)
        return result
    else:
        print(res)
        return {'Name': 'ERROR'}
