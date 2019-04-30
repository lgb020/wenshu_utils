# coding: utf-8
"""
测试包含:
1. vl5x的生成(vjkl5可以自生成, 服务器不会校验vjkl5, 只需让vjkl5和vl5x相互配对即可)
2. RunEval的解析
3. DocID的解密
"""
import json
import unittest

import requests

from wenshu_utils.vl5x.args import Vjkl5, Vl5x, Number, Guid
from wenshu_utils.docid.runeval import parse_run_eval
from wenshu_utils.docid.decrypt import decrypt_doc_id


class TestDecryption(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        })

    def tearDown(self):
        self.session.close()

    def test_decrypt(self):
        vjkl5 = Vjkl5()
        self.session.cookies["vjkl5"] = vjkl5

        url = "http://wenshu.court.gov.cn/List/ListContent"
        data = {
            "Param": "关键词:合同",
            "Index": 1,
            "Page": 10,
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": Vl5x(vjkl5),
            "number": Number(),
            "guid": Guid(),
        }
        response = self.session.post(url, data=data)

        json_data = json.loads(response.json())
        print(f"列表数据: {json_data}")

        run_eval = json_data.pop(0)["RunEval"]
        try:
            key = parse_run_eval(run_eval)
        except ValueError as e:
            raise ValueError("返回脏数据") from e
        else:
            print(f"RunEval解析完成: {key}\n")

        key = key.encode()
        for item in json_data:
            cipher_text = item["文书ID"]
            print(f"解密: {cipher_text}")
            plain_text = decrypt_doc_id(doc_id=cipher_text, key=key)
            print(f"成功, 文书ID: {plain_text}\n")


if __name__ == '__main__':
    unittest.main()
