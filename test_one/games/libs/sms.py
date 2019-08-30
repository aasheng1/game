'''
filename = sms.py
author = ZKY
date = 2019/08/06
'''

# urllib => 访问URL获取结果

import urllib.request
import urllib
import json
import logging

logger = logging.getLogger('apis')


def send_sms(mobile, captcha):
    """用云之汛接口发送短信验证码-"""
    # flag用于标记发送短信是否成功
    flag = True
    # 这个是短信API地址
    url = 'https://open.ucpaas.com/ol/sms/sendsms'
    # 准备一下头,声明body的格式
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    # 还有我们准备用Post传的值，这里值用字典的形式
    values = {
        "sid": "48886f56afa875b3cb5025cfd4d8e28a",
        "token": "a68566c239dedc30f64838cfa172a9d7",
        "appid": "983382a47eb8479fba03809c405b4be9",
        "templateid": "489939",
        # "param": str(captcha),
        "param": "{},10".format(str(captcha)),
        "mobile": mobile,
    }

    try:
        # 将字典格式化成bytes格式
        data = json.dumps(values).encode('utf-8')
        logger.info(f"即将发送短信: {data}")
        # 创建一个request,放入我们的地址、数据、头
        request = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        # html = '{"code":"000000","count":"1","create_date":"2018-07-23 13:34:06","mobile":"15811564298","msg":"OK","smsid":"852579cbb829c08c917f162b267efce6","uid":""}'
        code = json.loads(html)["code"]
        if code == "000000":
            logger.info(f"短信发送成功：{html}")
            flag = True
        else:
            logger.info(f"短信发送失败：{html}")
            flag = False
    except Exception as ex:
        logger.info(f"出错了,错误原因：{ex}")
        flag = False
    return flag


if __name__ == "__main__":
    # 测试短信接口是否是管用
    send_sms("18711176057", "123456")