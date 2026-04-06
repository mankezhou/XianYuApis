'''
Description: 
Date: 2026-04-06 17:09:36
LastEditTime: 2026-04-06 17:16:38
FilePath: \goodfish\XianYuApis\test1.py
'''
import requests
from utils.goofish_utils import generate_sign, trans_cookies, generate_device_id
import time


headers = {
    "Host": "h5api.m.goofish.com",
    "sec-ch-ua-platform": "\"Windows\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "accept": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua-mobile": "?0",
    "origin": "https://www.goofish.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.goofish.com/",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7,ja;q=0.6",
    "priority": "u=1, i"
}
cookies = {
    "cookie2": "1bc5027d7f2fffd9ff59ecf678d19e01",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "896fb63f7d91c4df5152b1735e666bd4_1775476147567",
    "_m_h5_tk_enc": "25741bde015885ab7f6540627f185bc9",
    "cna": "u2VaIj2q8V8CAXAC/C1wzj43",
    "_samesite_flag_": "true",
    "t": "d06336d57d1a6278c9bfb1d99eb23896",
    "_tb_token_": "37bebb14ea6b4",
    "xlly_s": "1",
    "sgcookie": "E100h0KObY67IH3dQd0PYmupdjQPPSdVNN%2BZpSSQ0e7H%2F%2BGuJ3iNQWriZALomhoevpDXHc4oFBxkV3paKB%2B%2FLrSE72usEkP6%2BqH3BgiN7Cx0qBU%3D",
    "csg": "49fcc58b",
    "unb": "3888777108",
    "tfstk": "gNqmZaflRrub5yAPxCofy5nMOr_-cmisk5Kt6chNzblWMIKYQCVgaWevDleZs5V-N-3YjRtiQRP1hfBfy-wjfc5d9fjLh-s6KfC5wcWaUcHgjSPWj-wjfL9J_wUzhGYa3Pcqb5orzvDmbEk4_3-rNAMwgA-VE8lSaARq7xJrzvkt_coa_8WoCblZbqPaUTDsafkERElLbyrPT-GV_WP_6uDmoXycPh-gqH3mT-lkb1ZonDGU3bxwbXRYwZ2uHsxQemw8tvFA4nV3duNoUWSGZcN775kgaMOtcyFbA42583y-mb3EakSyZYqupyk7EwXuElcm8oukBHnqmAPZSz1HvxmYr2q0lOOz3Wh08mw9Kseo-z0IU4JMumULplgU0iAIw2MgMbFFY3mr7grMzeSHKhMPBu865qkSEXQKmNVXWA8tiTXkJRgqFvGdETY6BqkSENWlEeUquYMqg"
}
url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemessage.pc.login.token/1.0/"
params = {
    "jsv": "2.7.2",
    "appKey": "34839810",
    't': str(int(time.time()) * 1000),
    'sign': '',
    "v": "1.0",
    "type": "originaljson",
    "accountSite": "xianyu",
    "dataType": "json",
    "timeout": "20000",
    "api": "mtop.taobao.idlemessage.pc.login.token",
    "sessionOption": "AutoLoginOnly",
    "spm_cnt": "a21ybx.im.0.0",
    "spm_pre": "a21ybx.item.want.1.14ad3da6ALVq3n",
    "log_id": "14ad3da6ALVq3n"
}
device_id = generate_device_id(cookies['unb'])
data_val = '{"appKey":"444e9908a51d1cb236a27862abc769c9","deviceId":"' + device_id + '"}'
data = {
    'data': data_val,
}
token = cookies['_m_h5_tk'].split('_')[0]
sign = generate_sign(params['t'], token, data_val)
params['sign'] = sign
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data, verify=False)

print(response.text)
print(response)