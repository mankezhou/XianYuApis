import base64
import json
import asyncio
import time

from loguru import logger
import websockets
from goofish_apis import XianyuApis

from utils.goofish_utils import generate_mid, generate_uuid, trans_cookies, generate_device_id, decrypt
from message import Message, make_text, make_image


class XianyuLive:
    def __init__(self, cookies_str):
        self.base_url = 'wss://wss-goofish.dingtalk.com/'
        self.cookies_str = cookies_str
        self.cookies = trans_cookies(cookies_str)
        self.myid = self.cookies['unb']
        self.device_id = generate_device_id(self.myid)
        self.xianyu = XianyuApis(self.cookies, self.device_id)
        self.ws = None

    async def list_all_conversations(self, ws, cid):
        msg = {
            "lwp": "/r/MessageManager/listUserMessages",
            "headers": {
                "mid": generate_mid()
            },
            "body": [
                f"{cid}@goofish",
                False,
                "9007199254740991",
                20,
                False
            ]
        }
        await ws.send(msg)
        try:
            has_more =
            ["body"]["userMessageModels"][0]["message"]["content"]["custom"]["title"]



    async def create_chat(self, ws, toid, item_id='891198795482'):
        msg = {
            "lwp": "/r/SingleChatConversation/create",
            "headers": {
                "mid": generate_mid()
            },
            "body": [
                {
                    "pairFirst": f"{toid}@goofish",
                    "pairSecond": f"{self.myid}@goofish",
                    "bizType": "1",
                    "extension": {
                        "itemId": item_id
                    },
                    "ctx": {
                        "appVersion": "1.0",
                        "platform": "web"
                    }
                }
            ]
        }
        await ws.send(json.dumps(msg))

    async def send_msg(self, ws, cid, toid, message: Message):
        msg_type = message["type"]
        msg = {
            "lwp": "/r/MessageSend/sendByReceiverScope",
            "headers": {
                "mid": generate_mid()
            },
            "body": [
                {
                    "uuid": generate_uuid(),
                    "cid": f"{cid}@goofish",
                    "conversationType": 1,
                    "content": {
                        "contentType": 101,
                        "custom": {
                            "type": None,
                            "data": None
                        }
                    },
                    "redPointPolicy": 0,
                    "extension": {
                        "extJson": "{}"
                    },
                    "ctx": {
                        "appVersion": "1.0",
                        "platform": "web"
                    },
                    "mtags": {},
                    "msgReadStatusSetting": 1
                },
                {
                    "actualReceivers": [
                        f"{toid}@goofish",
                        f"{self.myid}@goofish"
                    ]
                }
            ]
        }
        if msg_type == "text":
            payload = {
                "contentType": 1,
                "text": {
                    "text": message["text"]
                }
            }
            text_base64 = str(base64.b64encode(json.dumps(payload).encode('utf-8')), 'utf-8')
            msg["body"][0]["content"]["custom"]["type"] = 1
            msg["body"][0]["content"]["custom"]["data"] = text_base64
        elif msg_type == "image":
            payload = {
                "contentType": 2,
                "image": {
                    "pics": [
                        {
                            "type": 0,
                            "url": message["image_url"],
                            "width": message["width"],
                            "height": message["height"]
                        }
                    ]
                }
            }
            image_base64 = str(base64.b64encode(json.dumps(payload).encode('utf-8')), 'utf-8')
            msg["body"][0]["content"]["custom"]["type"] = 2
            msg["body"][0]["content"]["custom"]["data"] = image_base64
        elif msg_type == "audio":
            # TODO: handle audio message
            logger.error(f"不支持的消息类型: {msg_type}")
            return
        else:
            logger.error(f"不支持的消息类型: {msg_type}")
            return
        await ws.send(json.dumps(msg))

    async def init(self, ws):
        data = self.xianyu.get_token()
        token = data['data']['accessToken'] if 'data' in data and 'accessToken' in data['data'] else ''
        if not token:
            logger.error('获取token失败')
            exit(0)
        msg = {
            "lwp": "/reg",
            "headers": {
                "cache-header": "app-key token ua wv",
                "app-key": "444e9908a51d1cb236a27862abc769c9",
                "token": token,
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 DingTalk(2.1.5) OS(Windows/10) Browser(Chrome/133.0.0.0) DingWeb/2.1.5 IMPaaS DingWeb/2.1.5",
                "dt": "j",
                "wv": "im:3,au:3,sy:6",
                "sync": "0,0;0;0;",
                "did": self.device_id,
                "mid": generate_mid()
            }
        }
        await ws.send(json.dumps(msg))
        current_time = int(time.time() * 1000)
        msg = {
            "lwp": "/r/SyncStatus/ackDiff",
            "headers": {"mid": generate_mid()},
            "body": [
                {
                    "pipeline": "sync",
                    "tooLong2Tag": "PNM,1",
                    "channel": "sync",
                    "topic": "sync",
                    "highPts": 0,
                    "pts": current_time * 1000,
                    "seq": 0,
                    "timestamp": current_time
                }
            ]
        }
        await ws.send(json.dumps(msg))
        logger.info('init')


    async def send_msg_once(self, toid, item_id, send_message: Message):
        headers = {
            "Cookie": self.cookies_str,
            "Host": "wss-goofish.dingtalk.com",
            "Connection": "Upgrade",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Origin": "https://www.goofish.com",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        async with websockets.connect(self.base_url, extra_headers=headers) as websocket:
            await self.init(websocket)
            await self.create_chat(websocket, toid, item_id)
            async for message in websocket:
                try:
                    logger.info(f"message: {message}")
                    message = json.loads(message)
                    cid = message["body"]["singleChatConversation"]["cid"]
                    cid = cid.split('@')[0]
                    await self.send_msg(websocket, cid, toid, send_message)
                    logger.info('send message')
                    return
                except Exception as e:
                    pass

    async def heart_beat(self, ws):
        while True:
            msg = {
                "lwp": "/!",
                "headers": {
                    "mid": generate_mid()
                 }
            }
            await ws.send(json.dumps(msg))
            await asyncio.sleep(15)

    async def main(self):
        headers = {
            "Cookie": self.cookies_str,
            "Host": "wss-goofish.dingtalk.com",
            "Connection": "Upgrade",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Origin": "https://www.goofish.com",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        async with websockets.connect(self.base_url, extra_headers=headers) as websocket:
            asyncio.create_task(self.init(websocket))
            asyncio.create_task(self.heart_beat(websocket))
            async for message in websocket:
                # logger.info(f"message: {message}")
                try:
                    message = json.loads(message)
                    ack = {
                        "code": 200,
                        "headers": {
                            "mid": message["headers"]["mid"] if "mid" in message["headers"] else generate_mid(),
                            "sid": message["headers"]["sid"] if "sid" in message["headers"] else '',
                        }
                    }
                    if 'app-key' in message["headers"]:
                        ack["headers"]["app-key"] = message["headers"]["app-key"]
                    if 'ua' in message["headers"]:
                        ack["headers"]["ua"] = message["headers"]["ua"]
                    if 'dt' in message["headers"]:
                        ack["headers"]["dt"] = message["headers"]["dt"]
                    await websocket.send(json.dumps(ack))
                except Exception as e:
                    pass

                try:
                    data = message["body"]["syncPushPackage"]["data"][0]["data"]
                    logger.info(f"message: {data}")
                    try:
                        data = json.loads(data)
                        logger.info(f"无需解密 message: {data}")
                    except Exception as e:
                        logger.error(f'1 {e}')
                        data = decrypt(data)
                        message = json.loads(data)
                        logger.info(f"message: {message}")

                        send_user_name = message["1"]["10"]["reminderTitle"]
                        send_user_id = message["1"]["10"]["senderUserId"]
                        send_message = message["1"]["10"]["reminderContent"]
                        logger.info(f"user: {send_user_name}, 发送给我的信息 message: {send_message}")
                        # reply = f'Hello, {send_user_name}! I am a robot. I am not available now. I will reply to you later.'
                        reply = f'{send_user_name} 说了: {send_message}'
                        cid = message["1"]["2"]
                        cid = cid.split('@')[0]
                        await self.send_msg(websocket, cid, send_user_id, make_text(reply))

                        res_json = self.xianyu.upload_media(r"D:\Desktop\1.png")
                        image_object = res_json["object"]
                        width, height = map(int, image_object["pix"].split('x'))
                        await self.send_msg(websocket, cid, send_user_id, make_image(image_object["url"], width, height))
                except Exception as e:
                    logger.error(f'2 {e}')




if __name__ == '__main__':
    cookies_str = r'_samesite_flag_=true; cookie2=1bc5027d7f2fffd9ff59ecf678d19e01; t=d06336d57d1a6278c9bfb1d99eb23896; _tb_token_=37bebb14ea6b4; cna=u2VaIj2q8V8CAXAC/C1wzj43; xlly_s=1; tracknick=tb093613712; unb=3888777108; sgcookie=E100h0KObY67IH3dQd0PYmupdjQPPSdVNN%2BZpSSQ0e7H%2F%2BGuJ3iNQWriZALomhoevpDXHc4oFBxkV3paKB%2B%2FLrSE72usEkP6%2BqH3BgiN7Cx0qBU%3D; csg=49fcc58b; havana_lgc2_77=eyJoaWQiOjM4ODg3NzcxMDgsInNnIjoiNWUxNTgxMzgyODZhNzU2MTQzODhhOGZjNTNjYjI4ZGIiLCJzaXRlIjo3NywidG9rZW4iOiIxRmRpM2hHSmRtZDZkRjJIT01rYUcwdyJ9; _hvn_lgc_=77; havana_lgc_exp=1778058479377; isg=BMvLHFAjJkE-U3qVWjHOewFNWm-1YN_icuudHj3IbYphXOu-xTDXMmk_MlSy-zfa; sdkSilent=1775552889228; mtop_partitioned_detect=1; _m_h5_tk=ac05e051d07cb5c4fc1d46f192c0bf98_1775480876825; _m_h5_tk_enc=14a2c74c87c02bb1f9ea3b7dc39284c4; tfstk=gQzIp30LipvI6nfdep5w1gc-9kg7P172VQG8i7Lew23peLFxQJkE8_bSeJDa8vPEJaaS-PrezvWnP7eqPtWVuZP3tm0R3tyPSUdZkXhJyL8pWV3rNzwLIUN3t4AM_LI4XWbW2gRtw4e-WchjO4KKpDCsWXcjyenJJhptIb3-y0nKBFhS9HKK9UC_6AcryYe-v1gtIb3-e83-Hc9saMG8O_By01yllWVKCUL8JwmnhgDjsX41ncM49P8JygcIAxFKC9NETZnTZ0akZUMU9o2oMJpd3DV8fRGIPN-Kk5Z8hf4dupGgY5FqBSOkrWuQ5PGYW_LxUyZaMAgXwwFsRviY8D_fG-F_woo_7sQmR2HL42VyG9P_RJP357RJX2gUfmaIkZvKUlPbPbalENwbiP2s6-Q5pgRJuxMJL3OsmUGs3116q3cle4XaiWLJeDhi9Z511dtovfcs3116q3mKsXEV1196q'
    xianyuLive = XianyuLive(cookies_str)

    # 主动发送一次消息
    to_id = '2202640918079'
    item_id = '897742748011'
    # asyncio.run(xianyuLive.send_msg_once(to_id, item_id, make_text('Hello, this is an active message!')))

    res_json = xianyuLive.xianyu.upload_media(r"D:\Desktop\1.png")
    image_object = res_json["object"]
    width, height = map(int, image_object["pix"].split('x'))
    asyncio.run(xianyuLive.send_msg_once(to_id, item_id, make_image(res_json["object"]["url"], width, height)))

    # 常驻进程 用于接收消息和自动回复
    # asyncio.run(xianyuLive.main())
