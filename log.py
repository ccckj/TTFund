import os, sys
import requests
from bs4 import BeautifulSoup
import json
import time
import pdb 

def is_connected(resp):
    if resp.status_code == 200:
        return True
    else:
        return False
class TTFund(object):
    def __init__(self, urls, headers=None, cookies=None):
        self.urls = urls
        self.headers = headers
        self.cookies = cookies
        self.index_page()
        
    def index_page(self):
        if self.cookies is None:
            result = self._login()
            pdb.set_trace()

    def _login(self):
        url = self.urls['login']
        #登录页面
        login_page = requests.get(url, headers=headers, verify=False)
        if not is_connected(login_page):
            raise EOFError
        self.cookies = {}
        self.cookies.update(login_page.cookies.get_dict())
        #获取二维码图片
        qr_url = "https://login.1234567.com.cn/scancode?r=0.285364411886317"
        qr_img_resp = requests.get(qr_url, self.headers, cookies=self.cookies, verify=False)
        with open('test.jpg', 'wb') as f:
            f.write(qr_img_resp.content)
        self.cookies.update(qr_img_resp.cookies.get_dict())
        # 验证是否扫码
        control_url = "https://login.1234567.com.cn/LoginController.aspx/QrCodeLogin"
        payload = {"directURL": ""}

        control_resp = requests.post(control_url, json=payload, headers=self.headers, cookies=self.cookies, verify=False)
        while(json.loads(json.loads(control_resp.text)['d'])['ErrorMessageCode']!=1003):
            print('等待扫码...')
            time.sleep(1)
            control_resp = requests.post(control_url, json=payload, headers=self.headers, cookies=self.cookies, verify=False)
        ## TODO：扫码超时
        
        #确认超时
        control_resp = requests.post(control_url, json=payload, headers=self.headers, cookies=self.cookies, verify=False)
        result = json.loads(json.loads(control_resp.text)['d'])
        while(not result['IsSucceed']):
            print('扫码成功，等待确认')
            time.sleep(1)
            control_resp = requests.post(control_url, json=payload, headers=self.headers, cookies=self.cookies, verify=False)
            result = json.loads(json.loads(control_resp.text)['d'])
        print("登录成功")
        self.cookies.update(control_resp.cookies.get_dict())
        #保存cookies
        with open('cookies','w')as f:
            f.write(json.dumps(self.cookies))
        return result


if __name__ == "__main__":
    urls = {"index":"https://fund.eastmoney.com",
            "login":"https://login.1234567.com.cn/login"}
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Connection":"keep-alive",
        "Accept":"application/json, text/javascript, */*; q=0.01"    }

    cookies = {
        'TradeLoginToken':'688747aaa0cc4d28867b49dcc0a63525',
        'cp_token':'887af6b4537a4b1db51532bd1a0852f1',
        'ASP.NET_SessionId':'cvcokp3bw3g2sdsd1qrkepli'
    }
    ttFund = TTFund(urls=urls, headers=headers)