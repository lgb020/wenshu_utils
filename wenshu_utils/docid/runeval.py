# coding: utf-8
import re

from execjs.runtime_names import Node
import execjs

from ._unzip import unzip

nodejs = execjs.get(Node)


def parse_run_eval(run_eval: str) -> str:
    if run_eval.startswith("w63"):
        raise ValueError("invalid RunEval: w63")

    raw_js = unzip(run_eval).decode()
    js_code = raw_js.replace("_[_][_](", "return ")[:-4]

    ctx = nodejs.compile(js_code)
    js_result = ctx.eval("")

    if "while" in js_result:
        raise ValueError("invalid RunEval: while(1)")

    key = re.search(r'com\.str\._KEY="(?P<key>\w+)"', js_result).group("key")
    return key
