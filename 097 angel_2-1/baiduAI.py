import os

from config import AI_CLIENT, VOICE, CHAT_PATH


# from aip import AipSpeech
#
# """ 你的 APPID AK SK """
# APP_ID = '16981700'
# API_KEY = 'cHLC0p7dsOUVA0idSWQxV0lf'
# SECRET_KEY = 'VZCXoeuHfViaAA2EThwIHLukAYcT0pf9'
#
# AI_CLIENT = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#
# VOICE = {
#     'vol': 5,
#     'spd': 5,
#     'pit': 6,
#     'per': 4,
# }
#
# CHAT_PATH = 'Chats'


def text2audio(str, audio='notification.mp3'):
    res = AI_CLIENT.synthesis(str, 'zh', 1, VOICE)
    if not isinstance(res, dict):
        audio_path = os.path.join(CHAT_PATH, audio)
        with open(audio_path, 'wb') as f:
            f.write(res)
    else:
        print(res)


# text2audio('欢迎来到沙河智能玩具中心')
# text2audio('设备未绑定，请使用手机应用扫描二维码绑定')
# text2audio('设备异常请联系设备经销商')
# text2audio('您还没有未读消息', audio='nomessage.mp3')
