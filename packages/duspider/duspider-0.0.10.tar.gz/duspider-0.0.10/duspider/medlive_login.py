# -*- coding: utf-8 -*-
# @project: duspider
# @Author：dyz
# @date：2023/12/22 16:02
# 医脉通登录
import json
import time
from pathlib import Path
from random import choice
from typing import List

import requests
from parsel import Selector
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from playwright.async_api import async_playwright

from playwright._impl._api_structures import Cookie
from duspider.tools import get_ua


class MedLiveLogin:
    def __init__(self, auth: list):
        self.login_url = 'https://www.medlive.cn/auth/login'
        self.download_url = 'https://guide.medlive.cn/guide/download'
        self.params = {'service': 'https://www.medlive.cn/'}
        self.headers = {'user-agent': get_ua()}
        self.headers = {

            'DNT': '1',
            'Origin': 'https://www.medlive.cn',
            'Pragma': 'no-cache',
            # 'Referer': url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_ua(),
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'}
        self.user_list: List[(str, str)] = auth
        self.cookies_path = Path('cookies.json')
        if not self.cookies_path.exists():
            self.cookies_path.touch()
        self.cookies = None
        self.browser = None
        self.context = None
        self.page = None

        self.sess = None

        self.path = Path(__file__).parent

    def get_user(self):
        return choice(self.user_list)

    async def login(self, url=None):
        cookies = None
        with open(self.cookies_path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                cookies = json.loads(data)
                self.cookies = cookies
                self.sess = requests.Session()
                self.sess.headers = self.headers
                # self.sess.cookies = dict_from_cookiejar(cookies)
                # if url:
                #     await self.page.goto(url)
                # if not await self.test():
                #     cookies = None
                return
        async with async_playwright() as playwright:
            # self.browser = await playwright.chromium.launch(headless=False)
            self.browser = await playwright.chromium.connect_over_cdp('ws://10.168.2.57:3000')
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            # if cookies:
            #     await self.context.add_cookies(cookies)
            js = """Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"""
            print('加载js...')
            await self.page.add_init_script(js)
            if not cookies:
                await self.page.goto(self.login_url)
                await self.page.click('div.rightTab-R')
                user, pwd = self.get_user()
                await self.page.fill('#username', user)
                await self.page.fill('#showPassword', pwd)
                time.sleep(2)
                await self.page.click('#loginsubmit')
                if url:
                    await self.page.goto(url)
                await self.page.reload()
                cookies: List[Cookie] = await self.context.cookies()

                cookies_dict = {}
                for row in cookies:
                    if 'medlive' in row["domain"]:
                        cookies_dict[row["name"]] = row["value"]

                print('c:', cookies_dict, cookies_dict)
                # headers = await self.context.headers()
                self.cookies = cookies

                # 保存cookie信息到文件
                with open(self.cookies_path, 'w', encoding='utf-8') as f:
                    json.dump(cookies_dict, f, ensure_ascii=False)
            time.sleep(200)
            return

    async def load_sess(self, url=None):
        if not self.sess:
            await self.login(url)

    def get_params(self, doc, url):
        down = doc.css('div.downLoad::attr(onclick)').get('').strip().lstrip('download_info("').rstrip('")')
        down = down.split('","')
        # https://guide.medlive.cn/guide/download?id=30618&sub_type=1&fid=29535ef9039addc056a673f5b36ddd56&fn=%E5%86%A0%E7%8A%B6%E5%8A%A8%E8%84%89%E5%BE%AE%E8%A1%80%E7%AE%A1%E7%96%BE%E7%97%85%E7%9A%84%E8%AF%8A%E6%96%AD%E4%B8%8E%E6%B2%BB%E7%96%97%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%AE%B6%E5%85%B1%E8%AF%86%EF%BC%882023%E7%89%88%EF%BC%89-%E8%8B%B1%E6%96%87%E7%89%88.pdf&sk=bd7958db%20
        params = {
            "id": url.split('/')[-1].strip(),
            "sub_type": "1",
            "fid": down[0],
            "fn": down[1],
            "sk": down[2],
        }
        return params

    async def test(self, url=None):
        """测试登录状态"""
        url = url or 'https://guide.medlive.cn/guideline/16090'
        await self.load_sess(url)
        print('a:', self.cookies)
        resp = self.sess.get(url, cookies=self.cookies)
        doc = Selector(resp.text)
        params = self.get_params(doc, url)
        print("params:", params)
        self.download('16090', params)

    def download(self, params, file):
        """下载"""
        try:
            resp = self.sess.get(url=self.download_url,
                                 cookies=self.cookies,
                                 params=params,
                                 headers=self.headers
                                 )
            # logger.debug(params, resp.status_code)
            print(params, resp.status_code)
            if resp.headers['Content-Type'] != 'application/octet-stream':
                if '超过本日最大下载次数限制' in resp.text:
                    # logger.info('超过本日最大下载次数限制')
                    print('超过本日最大下载次数限制')
                    return '超过本日最大下载次数限制'
            suffix = Path(params['fn']).suffix
            if suffix != '.pdf':
                return False
            with open(file, 'wb') as f:
                f.write(resp.content)
            return file
        except Exception as e:
            print('eee:', e)
            return False


if __name__ == '__main__':
    auth = [('user', 'pwd')]

    med = MedLiveLogin(auth=auth)
    import asyncio

    url = 'https://guide.medlive.cn/guideline/16090'
    # asyncio.run(med.run(url=url))
    # asyncio.run(med.run(url=url))
    asyncio.run(med.test(url=url))
