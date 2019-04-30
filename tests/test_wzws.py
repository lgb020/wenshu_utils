# coding: utf-8
"""
测试包含:
1. 列表页wzws_cid(列表页wzws_cid可绕过(截止至2019.04.30)，headers中加入 X-Requested-With: XMLHttpRequest 即可)
2. 详情页wzws_cid(详情页wzws_cid也是可以绕过的(截止至2019.04.30)，请求method改为POST 即可)
"""
import unittest

import requests

from wenshu_utils.wzws.decrypt import wzws_cid_decrypt
from wenshu_utils.vl5x.args import Vl5x, Number, Guid


class TestWZWS(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        })

    def tearDown(self):
        self.session.close()

    def test_list(self):
        response = self.session.get("http://wenshu.court.gov.cn/list/list/")
        if "请开启JavaScript并刷新该页".encode() in response.content:
            redirect_url = wzws_cid_decrypt(response.content)
            _ = self.session.get(redirect_url)

        url = "http://wenshu.court.gov.cn/List/ListContent"
        data = {
            "Param": "关键词:合同",
            "Index": 1,
            "Page": 10,
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": Vl5x(self.session.cookies["vjkl5"]),
            "number": Number(),
            "guid": Guid(),
        }
        response = self.session.post(url, data=data)

        self.assertNotIn("请开启JavaScript并刷新该页", response.content.decode())
        print(response.text)

    def test_detail(self):
        url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
        params = {
            "DocID": "13d4c01a-0734-4ec1-bbac-658f8bb8ec62",
        }
        response = self.session.post(url, params=params)

        if "请开启JavaScript并刷新该页".encode() in response.content:
            redirect_url = wzws_cid_decrypt(response.content)
            response = self.session.get(redirect_url)

        self.assertNotIn("请开启JavaScript并刷新该页", response.content.decode())
        print(response.text)


if __name__ == '__main__':
    unittest.main()
