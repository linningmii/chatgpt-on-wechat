from WXBizMsgCrypt import WXBizMsgCrypt
from flask import request
from config import conf

sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
sCorpID = "ww1436e0e65a779aee"


def verify():
    config = conf()
    sToken = config.get("wechatcomapp_token")
    sEncodingAESKey = config.get("wechatcomapp_aes_key")
    sCorpID = config.get("wechatcom_corp_id")

    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    sVerifyMsgSig = request.args.get("msg_signature", "")
    # print ret
    sVerifyTimeStamp = request.args.get("timestamp", "")
    sVerifyNonce = request.args.get("nonce", "")
    sVerifyEchoStr = request.args.get("echostr", "")
    ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)

    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        return "ERR: VerifyURL ret: " + str(ret)
    # 验证URL成功，将sEchoStr返回给企业号
    # HttpUtils.SetResponse(sEchoStr)
    return sEchoStr
