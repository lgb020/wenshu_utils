# coding: utf-8
from typing import Union
from urllib import parse

from lxml.etree import HTML
from execjs.runtime_names import Node
import execjs

nodejs = execjs.get(Node)


def wzws_cid_decrypt(text: Union[str, bytes]) -> str:
    """
    :param text: 提示"请开启JavaScript并刷新该页"的响应text
    :return: 重定向url，访问重定向url后会返回wzws_cid的cookie
    """
    base_url = "http://wenshu.court.gov.cn"
    custom_js = """
    window = {};
    document = {
        createElement: () => ({ style: "", appendChild: () => ({}), submit: () => ({}) }),
        body: { appendChild: obj => { window.location = obj.action } }
    };
    atob = str => Buffer.from(str, "base64").toString("binary");
    get_location = () => window.location;
    """

    html = HTML(text)
    js = html.xpath("//script/text()")[0]

    ctx = nodejs.compile(custom_js + js)
    location = ctx.call("get_location")

    redirect_url = parse.urljoin(base_url, location)
    return redirect_url
