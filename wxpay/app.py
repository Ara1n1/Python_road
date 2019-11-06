# -*- coding: utf-8 -*-

# from weixin import WeixinPay, WeixinError
from flask import jsonify, request, Flask
from weixin.pay import WeixinPay, WeixinPayError
from settings import *

wx_pay = WeixinPay(app_id, mch_id, mch_key, NOTIFY_URL)
app = Flask(__name__)


@app.route("/pay/create")
def pay_create():
    """
    微信JSAPI创建统一订单，并且生成参数给JS调用
    """
    try:
        out_trade_no = wx_pay.nonce_str
        raw = wx_pay.jsapi(openid="openid", body=u"测试", out_trade_no=out_trade_no, total_fee=1)
        print(raw)
        return jsonify(raw)
    except WeixinPayError as e:
        # except WeixinError, e
        print(e)
        return e, 400


@app.route("/pay/notify")
def pay_notify():
    """
    微信异步通知
    """
    data = wx_pay.to_dict(request.data)
    if not wx_pay.check(data):
        return wx_pay.reply("签名验证失败", False)
    # 处理业务逻辑
    return wx_pay.reply("OK", True)


if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()
