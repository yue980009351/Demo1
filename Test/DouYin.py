#!/usr/bin/env python
# coding:utf-8

import requests

url = 'http://www.baidu.com'
data = requests.get(url)
print(data)

print(data.text)  # 这里.text等同于read()
code = data.encoding
print(code)
page_status = data.status_code
print(page_status)