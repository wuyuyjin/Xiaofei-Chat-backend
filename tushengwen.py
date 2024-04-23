import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket
# 图像理解

appid = "4516d816"
api_secret = "ZjRkZjZiOTU5Y2VhNTg3MjZmMDRmMWI0"
api_key = "2540c6b8d64cef46ea0a8f7d3e95aef5"
imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"
text = []


class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, imageunderstanding_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(imageunderstanding_url).netloc
        self.path = urlparse(imageunderstanding_url).path
        self.ImageUnderstanding_url = imageunderstanding_url

    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.ImageUnderstanding_url + '?' + urlencode(v)
        return url


def on_error(ws, error):
    print("### error:", error)


def on_close(ws):
    print("WebSocket closed")


def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, question=ws.question))
    ws.send(data)


def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content, end="")
        global answer
        answer += content
        if status == 2:  # 如果回复状态为结束
            ws.close()


def gen_params(appid, question):
    data = {
        "header": {
            "app_id": appid
        },
        "parameter": {
            "chat": {
                "domain": "image",
                "temperature": 0.5,
                "top_k": 4,
                "max_tokens": 2028,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def main(appid, api_key, api_secret, imageunderstanding_url, question):
    wsParam = Ws_Param(appid, api_key, api_secret, imageunderstanding_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while getlength(text[1:]) > 8000:
        del text[1]
    return text


def tushengwen(content, imageBase, callback):
    global answer
    answer = ""

    if imageBase.startswith('http'):  # 检查 imageBase 是否是 URL
        # 如果 imageBase 是 URL，则下载图片数据
        import requests
        response = requests.get(imageBase)
        if response.status_code == 200:
            imagedata = response.content
        else:
            print(f"无法从 URL 下载图片：{imageBase}")
            return
    else:
        # 假设 imageBase 是指向本地图片的文件路径
        try:
            imagedata = open(f"public/{imageBase}", 'rb').read()

        except FileNotFoundError:
            print(f"找不到图片文件：{imageBase}")
            return

    # 将图片数据编码为 base64
    imageMessage = {
        "role": "user",
        "content": str(base64.b64encode(imagedata), 'utf-8'),
        "content_type": "image"
    }

    text.append(imageMessage)
    question = checklen(getText("user", content))
    databaseString = str(base64.b64encode(imagedata))

    print("String:",databaseString)
    print("答:", end="")
    main(appid, api_key, api_secret, imageunderstanding_url, question)
    callback(answer)  # 将结果传递给回调函数

    if answer.endswith('。'):
        return
