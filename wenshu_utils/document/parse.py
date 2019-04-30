# coding: utf-8
import re

_data_pattern = re.compile(r'var caseinfo=JSON.stringify\((?P<case_info>.+?)\);\$'
                           r'.+(var dirData = (?P<dir_data>.+?);if)?'  # 2018年底改版了，dirData没有返回了
                           r'.+var jsonHtmlData = (?P<html_data>".+");', re.S)


def parse_detail(text):
    return _data_pattern.search(text).groupdict()
