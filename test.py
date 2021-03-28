import os
import random
import sys
import time
from _md5 import md5

import requests

url = 'https://www.instagram.com/xiezi000/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'cookie': 'ig_did=6A7D5C2A-E73A-4071-AABA-9214805D7E0A; mid=X8X-iwALAAERSlIcf9X14EZ90Gc9; ig_nrcb=1;csrftoken=5KaZk9aQJWk7MExg0nwXJAnJa95ouU7b; ds_user_id=5729010920; sessionid=5729010920:D0VzTfaukAuRoR:13;shbid=8458; shbts=1616835211.2197564; rur=FTW'
}

proxies = {'http': 'http://127.0.0.1:4780', 'https': 'http://127.0.0.1:4780'}


def get_urls(url0):
    try:
        response = requests.get(url0, headers=headers,)
        if response.status_code == 200:
            return response.text
        else:
            print('请求错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return response.text


html = get_urls(url)
# print(html)

import json
from pyquery import PyQuery as pq

urls = []
doc = pq(html)
items = doc('script[type="text/javascript"]').items()


def get_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print('请求照片二进制流错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None


for item in items:
    if item.text().strip().startswith('window._sharedData'):
        js_data = json.loads(item.text()[21:-1], encoding='utf-8')
        edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
        for edge in edges:
            url = edge['node']['display_url']
            # print(url)
            urls.append(url)
            content = get_content(url)
            file_path = './images'
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(content)
                    f.close()



