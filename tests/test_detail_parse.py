# coding: utf-8
"""
测试包含:
1. 详情页数据解析的正则
"""
from pprint import pprint
import unittest

import requests

from wenshu_utils.wzws.decrypt import wzws_cid_decrypt
from wenshu_utils.document.parse import parse_detail


class TestDetailParse(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        })

    def tearDown(self):
        self.session.close()

    def test_detail_parse(self):
        url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
        params = {
            "DocID": "13d4c01a-0734-4ec1-bbac-658f8bb8ec62",
        }
        response = self.session.get(url, params=params)

        if "请开启JavaScript并刷新该页".encode() in response.content:
            redirect_url = wzws_cid_decrypt(response.content)
            response = self.session.get(redirect_url)

        self.assertNotIn("请开启JavaScript并刷新该页", response.content.decode())

        group_dict = parse_detail(response.text)
        pprint(group_dict)


if __name__ == '__main__':
    unittest.main()
