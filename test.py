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
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=1, i"
}
cookies = {
    "cookie2": "102e0fa2d5f2e843347748770d589051",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "40b5982eef08b9e4a473def4cd391809_1775464427186",
    "_m_h5_tk_enc": "05e7ae716553b042bb5ec150ade94b90",
    "cna": "WzlaInyO3mICAXAC/C2M5zb2",
    "_samesite_flag_": "true",
    "t": "2b78901c0eb36a7e01084f582c7c47f0",
    "_tb_token_": "e3be4383e6b3e",
    "xlly_s": "1",
    "sgcookie": "E100sS33WS9DnNATp4U5fUwVfbH6XABVglfXiTuk6M7HNONDkxn0%2BNAGXRQDP7tDPvZS5oDSnQ%2FB9rmVSo27c%2Bslunhfzg2AdZnVqr4R6TELtZw%3D",
    "tracknick": "tb093613712",
    "csg": "12aa8652",
    "unb": "3888777108",
    "tfstk": "gIAZZBsg1fhNapmkzUfqLVhtb01Oiso7uIsfoEYc5Gjg15ZDL3xdfK91frJemHB1jdT_WpKWr5OsBsNV6sCmV0GSNNTOMsqG-NPlXeYdo2_iVCm85sCmVDwQiOhPMhPd6U5M-27fl-4MmNbn8a_li5X0sJqhvZfcitjM-XbAyR2cmnYn8ZIhmsfDm60FkMjcisDUEnxTTMWi7O8bDNmlWOSkSMPyJB7G6RLGYWFpTpWNqusUiSAF7E4RkEVrhgvRfT6pxXNNgeb2fMtoZW5hULLfuhlas19HpCC6O0zRQnS1EBBEEy52IhJcepl8eOXVbpAGLrVDJ6JhEK-ZbRIMCHWR-94qwwt5xFdMLqEHS3sNswXIZ48hnpOOeCi3__vJ519DDYwd_EvGTglLDwm0xIpam-WGJwSS82lHogg-zc68G-eALvQFV438H-BGJwSS82yYH9Rd8gg-y"
}
cookies_str = r'cookie2=174cc46140319474056cf8c8c105b3fe; mtop_partitioned_detect=1; _m_h5_tk=941b2abd24f8d5ca7614831bcbcd6f8d_1775465860195; _m_h5_tk_enc=92c4d9d2b75c387114bfa36f8bfc504b; cna=XEBaIvDCFgYCAXAC/C2/VHKP; _samesite_flag_=true; t=07245db896588d6836d6f1c2ede326d0; _tb_token_=fb0e33b5e8438; xlly_s=1; sgcookie=E100o0LTyBLgHNrZRyLdAHQF1lMwdkbYtUv9Gt%2BeEoHU9wyqeOCe3sv%2Bf9IQu2ofZO1%2BT3SLnCwgA2YWF8QZYGoEiVN9w5FXUr3RTVUq0gN20bA%3D; tracknick=tb093613712; csg=84deb362; unb=3888777108; x5sec=7b22733b32223a2261643531656137366337343739663837222c22617365727665723b33223a22307c43504f6b7a633447454a503871614c352f2f2f2f2f77456144444d344f4467334e7a63784d4467374d7a443271636d4c41773d3d227d; tfstk=gO0SBr_tnTXSQKRJpTRVG3q3-taCOI8NA6NKsXQP9zURp9hT3YyzzBYQpY2qz8lzyegQrqoP88JuRXHaRdJw7FloZl4pQdoeA1fuJWLUpnr8Zt_82dJw7E-RMy9WQby0K2rYt-F89wIJG-F_tyF8JJdbHWNGvTHLJIObsW6dpaUdMsFTwyeKpydjM-VQJ7HLJIGYnWHXZtNeVWhW9pwhkGb7KbefJw3vruwswM7dJqN7V2h8hmoql7Z7Bk12YZu-3X3rrovRFycqfviKpL_zickrroo5Hpwt4Y0ur2JNYrm-UqZoid_uFmHopzu9_MV0A8ixyo1dJja7dAmIFLsue0kbjSEAOFVqQ-hoymOhHbHaFzFY0FdsMknqrl0yHaatjbzrvvp5zSmZU4qqVTsrmNystIjCGlbQGRRXGMj30PlDM6JvhQE8i7LwGI6fxuF0GRRXGMj32SV-bIOfhMf..'
cookies = trans_cookies(cookies_str)
# print(cookies)
cookies = {
    "cookie2": "174cc46140319474056cf8c8c105b3fe",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "941b2abd24f8d5ca7614831bcbcd6f8d_1775465860195",
    "_m_h5_tk_enc": "92c4d9d2b75c387114bfa36f8bfc504b",
    "cna": "XEBaIvDCFgYCAXAC/C2/VHKP",
    "_samesite_flag_": "true",
    "t": "07245db896588d6836d6f1c2ede326d0",
    "_tb_token_": "fb0e33b5e8438",
    "xlly_s": "1",
    "sgcookie": "E100o0LTyBLgHNrZRyLdAHQF1lMwdkbYtUv9Gt%2BeEoHU9wyqeOCe3sv%2Bf9IQu2ofZO1%2BT3SLnCwgA2YWF8QZYGoEiVN9w5FXUr3RTVUq0gN20bA%3D",
    "tracknick": "tb093613712",
    "csg": "84deb362",
    "unb": "3888777108",
    "x5sec": "7b22733b32223a2261643531656137366337343739663837222c22617365727665723b33223a22307c43504f6b7a633447454a503871614c352f2f2f2f2f77456144444d344f4467334e7a63784d4467374d7a443271636d4c41773d3d227d",
    "tfstk": "gO0SBr_tnTXSQKRJpTRVG3q3-taCOI8NA6NKsXQP9zURp9hT3YyzzBYQpY2qz8lzyegQrqoP88JuRXHaRdJw7FloZl4pQdoeA1fuJWLUpnr8Zt_82dJw7E-RMy9WQby0K2rYt-F89wIJG-F_tyF8JJdbHWNGvTHLJIObsW6dpaUdMsFTwyeKpydjM-VQJ7HLJIGYnWHXZtNeVWhW9pwhkGb7KbefJw3vruwswM7dJqN7V2h8hmoql7Z7Bk12YZu-3X3rrovRFycqfviKpL_zickrroo5Hpwt4Y0ur2JNYrm-UqZoid_uFmHopzu9_MV0A8ixyo1dJja7dAmIFLsue0kbjSEAOFVqQ-hoymOhHbHaFzFY0FdsMknqrl0yHaatjbzrvvp5zSmZU4qqVTsrmNystIjCGlbQGRRXGMj30PlDM6JvhQE8i7LwGI6fxuF0GRRXGMj32SV-bIOfhMf.."
}
url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemessage.pc.login.token/1.0/"
params = {
    "jsv": "2.7.2",
    "appKey": "34839810",
    't': str(int(time.time()) * 1000),
    "v": "1.0",
    "type": "originaljson",
    "accountSite": "xianyu",
    "dataType": "json",
    "timeout": "20000",
    "api": "mtop.taobao.idlemessage.pc.login.token",
    "sessionOption": "AutoLoginOnly",
    "spm_cnt": "a21ybx.im.0.0",
    "spm_pre": "a21ybx.order-detail.0.0.47fc337eMFM5ao",
    "log_id": "47fc337eMFM5ao"
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