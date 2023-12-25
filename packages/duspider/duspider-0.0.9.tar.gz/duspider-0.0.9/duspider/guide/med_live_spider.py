# -*- coding: utf-8 -*-
# @Author：dyz
# @date：2023/11/22 10:29
import json
import random
import re
import time
from pathlib import Path

import requests
from duspider.drugs.medlive import MedLive

from duspider.exceptions import RequestError

from duspider.tools import make_md5
from parsel import Selector
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio


path = Path('capt.jpg')


class MedLiveSpider(MedLive):

    def __init(self):
        super().__init__()
        self.start_url = 'https://guide.medlive.cn/more_filter'

    async def save_capt(self, url='https://drugs.medlive.cn/captchaAction.do'):
        """保存图片"""
        params = {
            'cd': random.random(),
        }
        res = await self.get(url, params=params, headers=self.headers, cookies=self.cookies)
        with open(path, 'wb') as f:
            f.write(res.content)

    async def get(self, url, **kwargs):
        for i in range(self.max_retry):
            try:
                resp = self.sess.get(url,
                                     timeout=self.timeout,
                                     **kwargs)
                return await self.capt(url, resp)
            except Exception as err:
                time.sleep(0.5)
                if i == self.max_retry - 1:
                    raise RequestError(url, err=err, retry=i)
        return ''

    async def post(self, url, **kwargs):
        for i in range(self.max_retry):
            try:
                resp = self.sess.post(url,
                                      timeout=self.timeout,
                                      **kwargs)

                return resp
            except Exception as err:
                time.sleep(0.5)
                if i == self.max_retry - 1:
                    raise RequestError(url, err=err, retry=i)
        return ''

    async def capt(self, orgin_url, resp):
        """验证码"""
        if '您的访问过于频繁' in resp.text:
            print('您的访问过于频繁...')
            await self.save_capt()
            captcha = get_ocr(path)
            print("captcha:", captcha)
            data = {
                'orginUrl': orgin_url,
                'captcha': captcha,
            }
            response = await self.post('https://drugs.medlive.cn/validCaptcha.do',
                                       cookies=cookies,
                                       headers=headers,
                                       data=data)
            return response
        return resp

    @load_db
    async def run(self):
        async for row in tqdm_asyncio(self.all()):
            if row.status_code == 200:
                html = row.text
                url = row.url
                await self.parse(html, url)
                time.sleep(5)
            else:
                print(row.status_code)
                headers = input('headers >')
                if headers:
                    self.headers = json.loads(headers)
                cookies = input('cookies >')
                if cookies:
                    self.cookies = json.loads(cookies)

                input('开始>')

    @staticmethod
    async def parse(html, url):
        doc = Selector(html)
        uid = make_md5(url)
        name = doc.xpath('//label[contains(text(), "通用名称")]/../text()').get('').strip()
        approval_number = doc.xpath('string(//a[contains(text(),"批准文号")]/../following-sibling::div/p[2])').get(
            '').strip()
        if approval_number:
            approval_number = re.sub('(\\s+)', '', approval_number)
            # print(approval_number, row.url)
        if not await MedLiveDB.filter(uid=uid).exists():
            await MedLiveDB.create(uid=uid, html=html, approval_number=approval_number, name=name, url=url)

    def get_approval_number(self, data):
        data_list = []
        if data:
            for span in data:
                for span_text in span.get().split('<br>'):
                    if re.findall('(国药准字\\s+)', span_text):
                        span_text = re.sub('(国药准字\\s+)', '国药准字', span_text)
                    text_list = re.split('\\s+|；|：|。|:|）|（|\)|\(', span_text)
                    for text in text_list:
                        text = my_replace(text)
                        if '国药准字' in text and len(text) != 4:
                            data_list.append(text)
        return data_list

    @load_db
    async def update_approval_number(self):
        id_ = 0
        while True:
            data = await MedLiveDB.filter(id__gt=id_).order_by('id').limit(100)
            if not data:
                break
            id_ = data[-1].id
            for row in tqdm(data):
                doc = Selector(row.html)
                approval_number_data = doc.xpath(
                    '//a[contains(text(),"批准文号")]/../following-sibling::div/p')
                approval_number = self.get_approval_number(approval_number_data)
                await MedLiveDB.filter(id=row.id).update(
                    approval_number=json.dumps(approval_number, ensure_ascii=False))

    @staticmethod
    def parse_ingredients(p_list, item):
        """解析成分"""
        for i in p_list:
            text = i.css('p').get('')
            text_list = text.split('：', 1)
            if len(text_list) > 1:
                if text_list[0] == '辅料为':
                    item.accessories = text_list[-1]
                elif text_list[0] == '辅料为':
                    item.accessories = text_list[-1]
            else:
                if '主要成份' in text:
                    text = my_replace(text)
                    if text:
                        item.ingredients = text

        return item

    @staticmethod
    def parse_data(data) -> DrugsItem:
        item = DrugsItem()
        doc = Selector(data)
        # todo
        ename = doc.xpath('//label[contains(text(),"【英文名称】")]/../text()').get('').strip()
        if ename:
            item.ename = ename
        trade_name = doc.xpath('//label[contains(text(),"【商品名称】")]/../text()').get('').strip()
        if trade_name:
            item.trade_name = trade_name
        p_list = doc.xpath('//a[contains(@name,"ingredients")]/../following-sibling::div/p')
        item = MedLiveSpider.parse_ingredients(p_list, item)
        indications = my_replace([
            _.xpath('.').get('').strip()
            for _ in doc.xpath('//a[contains(text(),"适应症：")]/../following-sibling::div/p')
        ])
        if indications:
            item.indications = indications

        specification = my_replace(
            doc.xpath('string(//a[contains(text(),"规格：")]/../following-sibling::div)').get('').strip())
        if specification:
            item.specification = specification

        dosage = my_replace(
            [
                _.xpath('.').get('').strip() for _ in
                doc.xpath('//a[contains(text(),"用法用量：")]/../following-sibling::div/p')
            ])
        if dosage:
            item.dosage = dosage

        adverse_effects = my_replace(
            [
                _.xpath('.').get('').strip() for _ in
                doc.xpath('//a[contains(text(),"注意事项：")]/../following-sibling::div/p')
            ])
        if adverse_effects:
            item.adverse_effects = adverse_effects

        taboo = my_replace(
            [
                _.xpath('.').get('').strip() for _ in
                doc.xpath('//a[contains(text(),"药物相互作用：")]/../following-sibling::div/p')
            ])
        if taboo:
            item.taboo = taboo

        notes = my_replace(
            [
                _.xpath('.').get('').strip() for _ in
                doc.xpath('//a[contains(text(),"注意事项：")]/../following-sibling::div/p')
            ])
        if notes:
            item.notes = notes

        storage = my_replace(
            doc.xpath('string(//a[contains(text(),"贮藏：")]/../following-sibling::div/p)').get('').strip())
        if storage:
            item.storage = storage

        wrap = my_replace(
            doc.xpath('string(//a[contains(text(),"包装：")]/../following-sibling::div/p)').get('').strip())
        if wrap:
            item.wrap = wrap
        expiration_date = my_replace(
            doc.xpath('string(//a[contains(text(),"有效期：")]/../following-sibling::div/p)').get('').strip())
        if expiration_date:
            item.expiration_date = expiration_date
        production_units = my_replace(
            doc.xpath('string(//a[contains(text(),"生产企业：")]/../following-sibling::div/p)').get('').strip())
        if production_units:
            item.production_units = production_units

        return item

    @load_db
    async def t1(self):
        data = await MedLiveDB.all().order_by('id').limit(50)
        for row in data:
            item = self.parse_data(row.html)
            import json
            print(json.dumps(item.dict(), ensure_ascii=False))
            # print(item.json())


if __name__ == '__main__':
    cookies = {
        'Hm_lvt_62d92d99f7c1e7a31a11759de376479f': '1700558681',
        'ymtinfo': 'eyJ1aWQiOiI1MzIxMzQ3IiwicmVzb3VyY2UiOiIiLCJleHRfdmVyc2lvbiI6IjEiLCJhcHBfbmFtZSI6IiJ9',
        'ymt_pk_id': '1c47467b1bb9d241',
        'JSESSIONID': 'D47F29CEECD3758B3F5E124AD7B8BC34',
        '_pk_ref.3.a971': '%5B%22%22%2C%22%22%2C1700698495%2C%22https%3A%2F%2Fwww.medlive.cn%2F%22%5D',
        '_pk_ses.3.a971': '*',
        'Hm_lpvt_62d92d99f7c1e7a31a11759de376479f': '1700698506',
        '_pk_id.3.a971': '1c47467b1bb9d241.1700558683.5.1700698506.1700655545.',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'Hm_lvt_62d92d99f7c1e7a31a11759de376479f=1700558681; ymtinfo=eyJ1aWQiOiI1MzIxMzQ3IiwicmVzb3VyY2UiOiIiLCJleHRfdmVyc2lvbiI6IjEiLCJhcHBfbmFtZSI6IiJ9; ymt_pk_id=1c47467b1bb9d241; JSESSIONID=D47F29CEECD3758B3F5E124AD7B8BC34; _pk_ref.3.a971=%5B%22%22%2C%22%22%2C1700698495%2C%22https%3A%2F%2Fwww.medlive.cn%2F%22%5D; _pk_ses.3.a971=*; Hm_lpvt_62d92d99f7c1e7a31a11759de376479f=1700698506; _pk_id.3.a971=1c47467b1bb9d241.1700558683.5.1700698506.1700655545.',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Referer': 'https://drugs.medlive.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    med = MedLiveSpider(cookies=cookies, headers=headers)
    import asyncio

    asyncio.run(med.run())
    # asyncio.run(med.update_approval_number())
    # asyncio.run(med.t1())
