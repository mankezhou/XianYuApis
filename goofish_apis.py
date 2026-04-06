'''
Description: 
Date: 2026-04-04 15:32:48
LastEditTime: 2026-04-06 19:10:56
FilePath: \XianYuApis\XianyuApis.py
'''
import json
import os
import time

import requests

from utils.goofish_utils import generate_sign, trans_cookies, generate_device_id


class XianyuApis:
    def __init__(self, cookies, device_id):
        self.login_url = 'https://h5api.m.goofish.com/h5/mtop.taobao.idlemessage.pc.login.token/1.0/'
        self.upload_media_url = 'https://stream-upload.goofish.com/api/upload.api'
        self.session = requests.Session()
        self.session.cookies.update(cookies)
        self.device_id = device_id

    def get_token(self):
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
        params = {
            'jsv': '2.7.2',
            'appKey': '34839810',
            't': str(int(time.time()) * 1000),
            'sign': '',
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'api': 'mtop.taobao.idlemessage.pc.login.token',
            'sessionOption': 'AutoLoginOnly',
            'spm_cnt': 'a21ybx.im.0.0',
            "spm_pre": "a21ybx.item.want.1.14ad3da6ALVq3n",
            "log_id": "14ad3da6ALVq3n"
        }
        data_val = '{"appKey":"444e9908a51d1cb236a27862abc769c9","deviceId":"' + self.device_id + '"}'
        data = {
            'data': data_val,
        }
        token = self.session.cookies['_m_h5_tk'].split('_')[0]
        sign = generate_sign(params['t'], token, data_val)
        params['sign'] = sign
        response = self.session.post(self.login_url, params=params, headers=headers, data=data, verify=False)
        res_json = response.json()
        return res_json

    def upload_media(self, media_path):
        headers = {
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7,ja;q=0.6",
            "cache-control": "no-cache",
            "origin": "https://www.goofish.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.goofish.com/",
            "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        }
        params = {
            "floderId": "0",
            "appkey": "xy_chat",
            "_input_charset": "utf-8"
        }
        with open(media_path, 'rb') as f:
            media_name = os.path.basename(media_path)
            files = {
                "file": (media_name, f, "image/png")
            }
            response = self.session.post(self.upload_media_url, headers=headers, params=params, files=files, verify=False)
            res_json = response.json()
            return res_json



if __name__ == '__main__':
    cookies_str = r'_samesite_flag_=true; cookie2=1bc5027d7f2fffd9ff59ecf678d19e01; t=d06336d57d1a6278c9bfb1d99eb23896; _tb_token_=37bebb14ea6b4; cna=u2VaIj2q8V8CAXAC/C1wzj43; xlly_s=1; tracknick=tb093613712; unb=3888777108; sgcookie=E100h0KObY67IH3dQd0PYmupdjQPPSdVNN%2BZpSSQ0e7H%2F%2BGuJ3iNQWriZALomhoevpDXHc4oFBxkV3paKB%2B%2FLrSE72usEkP6%2BqH3BgiN7Cx0qBU%3D; csg=49fcc58b; havana_lgc2_77=eyJoaWQiOjM4ODg3NzcxMDgsInNnIjoiNWUxNTgxMzgyODZhNzU2MTQzODhhOGZjNTNjYjI4ZGIiLCJzaXRlIjo3NywidG9rZW4iOiIxRmRpM2hHSmRtZDZkRjJIT01rYUcwdyJ9; _hvn_lgc_=77; havana_lgc_exp=1778058479377; isg=BMvLHFAjJkE-U3qVWjHOewFNWm-1YN_icuudHj3IbYphXOu-xTDXMmk_MlSy-zfa; sdkSilent=1775552889228; mtop_partitioned_detect=1; _m_h5_tk=ac05e051d07cb5c4fc1d46f192c0bf98_1775480876825; _m_h5_tk_enc=14a2c74c87c02bb1f9ea3b7dc39284c4; tfstk=gQzIp30LipvI6nfdep5w1gc-9kg7P172VQG8i7Lew23peLFxQJkE8_bSeJDa8vPEJaaS-PrezvWnP7eqPtWVuZP3tm0R3tyPSUdZkXhJyL8pWV3rNzwLIUN3t4AM_LI4XWbW2gRtw4e-WchjO4KKpDCsWXcjyenJJhptIb3-y0nKBFhS9HKK9UC_6AcryYe-v1gtIb3-e83-Hc9saMG8O_By01yllWVKCUL8JwmnhgDjsX41ncM49P8JygcIAxFKC9NETZnTZ0akZUMU9o2oMJpd3DV8fRGIPN-Kk5Z8hf4dupGgY5FqBSOkrWuQ5PGYW_LxUyZaMAgXwwFsRviY8D_fG-F_woo_7sQmR2HL42VyG9P_RJP357RJX2gUfmaIkZvKUlPbPbalENwbiP2s6-Q5pgRJuxMJL3OsmUGs3116q3cle4XaiWLJeDhi9Z511dtovfcs3116q3mKsXEV1196q'
    cookies = trans_cookies(cookies_str)
    xianyu = XianyuApis(cookies, generate_device_id(cookies['unb']))
    res = xianyu.get_token()
    print(json.dumps(res, indent=4, ensure_ascii=False))

    res = xianyu.upload_media(r"D:\Desktop\1.png")
    print(json.dumps(res, indent=4, ensure_ascii=False))
