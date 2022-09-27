# -*- coding: utf-8 -*-
"""
cron: 1 8 * * *
new Env('精易论坛');
"""

import requests
import json
import sys
from notify import send

url = "https://bbs.125.la/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"

data = {
    "formhash": "04dc0f3a",
    "submit": "1",
    "targerurl": "",
    "todaysay": "",
    "qdxq": "kx"
}

message = ""


def printf(*args):
    global message
    print(*args)
    message += "\n" + " ".join(args)
    sys.stdout.flush()


def sign(us):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "cookie": us.get("ck")
    }
    res = requests.post(url, headers=headers, data=data)
    msg = ""
    if res.status_code == 200:
        try:
            da = res.json()
        except:
            return f"返回错误：{res.text}"
        if da.get("status") == 1:
            try:
                msg += f"""
    累计签到：{da["data"]["days"]} 天
    本月签到：{da["data"]["mdays"]} 天
    总得奖励：{da["data"]["reward"]} 精币
    本次奖励：{da["data"]["credit"]} 精币
    上次签到：{da["data"]["qtime"]}
    """
                return msg
            except:
                return f"格式化错误：{da}"
        else:
            return f"请求错误：{da}"
    else:
        return f"错误请求,{res.status_code}"


def main():
    with open("user.json", mode="r", encoding="utf8") as f:
        user = json.load(f)
        user = user.get("jingyi")
    if not user:
        printf("没有填写CK")
        return
    for i, us in enumerate(user):
        printf(f"开始第{i}个账号")
        res = sign(us)
        printf(res)


if __name__ == '__main__':
    main()
    send("精易论坛签到", message)
