#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: luozaibo
# date : 2019-07-30 10:51:42
import requests
from lxml import etree
from fake_useragent import UserAgent
import re
from pprint import pprint
import json
from pathlib import Path
import logging
import time


COOKIE = 't=def7dc94586a0ad9861c6d51517f6e5b; _tb_token_=75d60138e94e3; cookie2=102e06b9a1ac621a119bf08869660146; cna=G2rGFes6mmkCAXWIAKXgN4aK; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; swfstore=91515; enc=VQFqHtUcEdCSdq2DUKAvsOT2SAR4OvA6XbOHrcjJpoSwjeKzktkE%2F2LJvFYjY7l8qFucbLfRjJumok8loj4kXQ%3D%3D; OZ_SI_2061=sTime=1565927938&sIndex=38; OZ_1U_2061=vid=vd562a0232b27e.0&ctime=1566004382&ltime=1565928189; OZ_1Y_2061=erefer=-&eurl=https%3A//detail.tmall.com/item.htm%3Fid%3D586668058289%26rn%3Db9d8ab5abba8d043dff7bb4273f67e15%26abbucket%3D0&etime=1565927938&ctime=1566004382&ltime=1565928189&compid=2061; dnk=tb154072867; uc1=pas=0&existShop=false&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie14=UoTaHoqUDMwKxw%3D%3D&cookie21=Vq8l%2BKCLiYYu&lng=zh_CN; uc3=vt3=F8dBy3K0WuAlvWa2074%3D&id2=UUphyu7jVL7UPgcgBg%3D%3D&lg2=URm48syIIVrSKA%3D%3D&nk2=F5REO%2By5JP4c1LE%3D; tracknick=tb154072867; lid=tb154072867; uc4=id4=0%40U2grEagn5RiQf54ywf41sjal3asfzQqD&nk4=0%40FY4PaQ6F115cAdZMsq3Wr8bARasQ0A%3D%3D; lgc=tb154072867; csg=12838cb8; whl=-1%260%260%260; cq=ccp%3D1; UM_distinctid=16daa54ce0b63b-0d91a97e100c32-30750f58-1fa400-16daa54ce0c5a2; _m_h5_tk=e0f9a4b34567d78de362117688baf358_1571139556293; _m_h5_tk_enc=e766c6d9deb3043cb8066a7ca359e80a; pnm_cku822=098%23E1hvOQvUvbpvUpCkvvvvvjiPRszUQjDCPFcUgjthPmPvzjYPP2L9QjimPF5y0j3CPFyCvvpvvhCv2QhvCvvvvvmivpvUvvCCbhSs1cREvpvVvpCmpnswKphv8vvvpHQvvvmXvvCjm9vv9xIvvhNjvvvmjvvvBQIvvvURvvCjm9vvv9gEvpCWvk77D3zZdip7%2B3%2BuaNoAdXkK4Qtrz8g7rEtAB%2BF9HFKzrmphQRA1%2BbeAOHjZT2eARdIAcUmD5d8reB6k1W9XViyaw6jhzCOqrqpyCvhCvvOv9hCvvvm5vpvhvvCCBv%3D%3D; l=dBN0iSjnqYPYMzy2BOCZlurza77TJIRf_uPzaNbMi_5a11-FZV7OkglfleJ6cjWcGg8p4Rr5tB9tREVbJzLfSVAuC9cdvd3eBef..; isg=BDAwZKsBGZVBccVzIJ1ASJjiAfeCeRTDEWIEbSqBwgve5dGP046mUyGXOa0g8syb'
# COOKIE = "t=def7dc94586a0ad9861c6d51517f6e5b; _tb_token_=75d60138e94e3; cookie2=102e06b9a1ac621a119bf08869660146; cna=G2rGFes6mmkCAXWIAKXgN4aK; hng=CN%7Czh-CN%7CCNY%7C156; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; enc=VQFqHtUcEdCSdq2DUKAvsOT2SAR4OvA6XbOHrcjJpoSwjeKzktkE%2F2LJvFYjY7l8qFucbLfRjJumok8loj4kXQ%3D%3D; OZ_SI_2061=sTime=1565927938&sIndex=38; OZ_1U_2061=vid=vd562a0232b27e.0&ctime=1566004382&ltime=1565928189; OZ_1Y_2061=erefer=-&eurl=https%3A//detail.tmall.com/item.htm%3Fid%3D586668058289%26rn%3Db9d8ab5abba8d043dff7bb4273f67e15%26abbucket%3D0&etime=1565927938&ctime=1566004382&ltime=1565928189&compid=2061; dnk=tb154072867; uc1=pas=0&existShop=false&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie14=UoTaHoqUDMwKxw%3D%3D&cookie21=Vq8l%2BKCLiYYu&lng=zh_CN; uc3=vt3=F8dBy3K0WuAlvWa2074%3D&id2=UUphyu7jVL7UPgcgBg%3D%3D&lg2=URm48syIIVrSKA%3D%3D&nk2=F5REO%2By5JP4c1LE%3D; tracknick=tb154072867; lid=tb154072867; uc4=id4=0%40U2grEagn5RiQf54ywf41sjal3asfzQqD&nk4=0%40FY4PaQ6F115cAdZMsq3Wr8bARasQ0A%3D%3D; lgc=tb154072867; csg=12838cb8; whl=-1%260%260%260; _m_h5_tk=86e008502ecefb1d0eec9dc27d45630f_1567003990238; _m_h5_tk_enc=1c29eb159c27aba67807aac3a5d17464; pnm_cku822=; cq=ccp%3D1; swfstore=207568; x5sec=7b2273686f7073797374656d3b32223a223031323162393833633533653263626265663439663066363235613537393635435061566e657346454b334c3659546b6c37543754526f4e4d546b354d5455334f4449794e4473784f513d3d227d; l=cBN0iSjnqYPYMCpFBOCanurza77OSIRYouPzaNbMi_5BL6LsOtbOkumdaFp6VjWdtnLB48zylNe9-eteidqtmEU75Q1d.; isg=BMXFMVmNNCN47RDczTYdH-051Aj_gnkU6BaD_8cqgfwLXuXQj9KJ5FM4aMINGJHM",
class TmallSpider(object):
    def headers(self, shop_name):
        headers = {
                "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "cookie": COOKIE,
                "host": f"{shop_name}.tmall.com",
                "method": "GET",
                "scheme": "https",
                "referer": f"https://{shop_name}.tmall.com/search.htm?spm=a1z10.3-b-s.w4011-14528072910.533.401835318BT7pX&search=y&pageNo=1&tsearch=y",
                "user-agent": UserAgent().random
                }
        return headers

    # 获取详情页的url
    def get_detail_page(self, url, shop_name):
        headers = {
                "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "cookie": COOKIE,
                "host": f"{shop_name}.tmall.com",
                "method": "GET",
                "scheme": "https",
                "referer": f"https://{shop_name}.tmall.com/search.htm?spm=a1z10.3-b-s.w4011-14528072910.533.401835318BT7pX&search=y&pageNo=1&tsearch=y",
                "user-agent": UserAgent().random
                }
        response = requests.get(url, headers=headers)
        pattern = re.compile(r'  href=\\"//detail.tmall.com(.*?)\\" ')
        # 获取商品的地址
        detail_urls = pattern.findall(response.text)
        detail_url_list = list(set([f'https://detail.tmall.com{url}' for url in detail_urls]))[:-8]
        # 是否有下一页
        next_page = re.findall(r'<a class=\\"disable\\">下一页',response.text)
        return detail_url_list, next_page

    # 从详情页提取需要的数据
    def parse_detail_page(self, detail_url, shop_name):
        headers = {
                'user-agent': UserAgent().random,
                'referer': f'https://{shop_name}.tmall.com/category.htm?spm=a1z10.3-b-s.w5001-14593428624.15.32dc24b6ydoH4p&scene=taobao_shop'
                }
        response = requests.get(detail_url, headers=headers)
        html = etree.HTML(response.text)
        item = {}
        item['goods_url'] = detail_url
        # 商品标题
        item['goods_name'] = html.xpath('string(//div[@class="tb-detail-hd"]/h1)').strip()
        # print(item)
        # 商品属性
        params = html.xpath('//ul[@id="J_AttrUL"]/li/text()')#.strip()
        params = {re.sub(r'\xa0', '', i) for i in params if '：' not in i}
        try:
            item['params']  = {i.split(':')[0]:i.split(':')[1] for i in params}
        except:
            item['params'] = {}
            print('params null')
        # 商品预览图片
        images = html.xpath('//ul[@id="J_UlThumb"]/li/a/img/@src')
        item['preview_img'] = ['https:' + '_'.join(image.split('_')[:-1]) + '_2200x2200q90.jpg' for image in images]
        # 商品价格
        item['price'] =re.findall(r'"reservePrice":"(\d+.00)"', response.text)
        # print(item['price'])
        if item['price']:
            item['price'] = '￥' + re.findall(r'"reservePrice":"(\d+.00)"', response.text)[0]
        # 获取商品ID和店铺ID
        itemId = re.findall(r'itemId:"(\d+)"', response.text)[0]
        sellerId = re.findall(r'sellerId:"(\d+)"', response.text)[0]
        item['seller_id'] = sellerId
        item['goods_id'] = itemId
        try:
            # 商品描述图片
            desc_url = re.findall(r'"httpsDescUrl":"(.*?)"', response.text)[0]
            desc_url = f'https:{desc_url}'
            item['desc_img'] = self.get_desc_imgs(desc_url, detail_url)
        except:
            print('error  ' + detail_url)
        return item

    # 获取描述页的图片
    def get_desc_imgs(self, desc_url, detail_url):
        headers = {
                'user-agent': UserAgent().random,
                'referer': detail_url,
                'cookie': COOKIE
                }
        try:
            response = requests.get(desc_url, headers=headers)
            pattern = re.compile('src="(.*?)"')
            desc_imgs = pattern.findall(response.text)
        except:
            print('error  get_desc_img')
        return desc_imgs

    # 商品信息存入json
    def save_to_json(self, item, detail_url, shop_name):
        itemId = re.findall('id=(\d+)', detail_url)[0]
        Path(f'./{shop_name}').mkdir(parents=True, exist_ok=True)
        with open(f'./{shop_name}/{itemId}_info.json', 'w') as f:
            f.write(json.dumps(item, ensure_ascii=False))
        print(f'save success {detail_url}')

    def run(self): # 实现主要逻辑
        shop_name_list = ['adidas']
        for shop_name in shop_name_list:
            next_page = False
            pageNo = 1
            while not next_page:  # 是否有下一页
                url = 'https://{}.tmall.com/i/asynSearch.htm?_ksTS=1571209253940_664&callback=jsonp665&mid=w-14694769140-0&wid=14694769140&path=/category.htm&spm=a1z10.5-b-s.w4011-14694769140.110.70131ca23yvjFR&search=y&orderType=defaultSort&pageNo={}'
                # 1.获取店铺某一页所有商品详情页的url
                detail_url_list, next_page = self.get_detail_page(url.format(shop_name,pageNo), shop_name)
                # 处理每一页中确定的一个商品
                i = 0
                for detail_url in detail_url_list[:-8]:
                    # 2.进入详情页提取数据
                    item = self.parse_detail_page(detail_url, shop_name)
                    # 3.保存json
                    self.save_to_json(item, detail_url, shop_name)
                    i += 1
                    if i > 9:  # 爬取10件商品，可自行修改或注释
                        break
                pageNo += 1
                time.sleep(2)
                break  # 爬取一页，可注释
            break  # 爬取一个品牌，可注释


if __name__ == '__main__':
    tmall = TmallSpider()
    start = time.time()
    tmall.run()
    end = time.time()
    print(f'用时：{end -start} s')
