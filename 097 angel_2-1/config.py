# 静态文件配置
MUSIC_PATH = 'Musics'
COVER_PATH = 'Covers'
QRCODE_PATH = 'QRcode'
CHAT_PATH = 'Chats'

# 数据库配置
from pymongo import MongoClient

MG = MongoClient('localhost', 27017)
mongo = MG['Angel']

# 返回配置
RET = {
    "CODE": 0,
    "MSG": "",
    "DATA": {}
}

# 二维码生成API
QRCODE_URL = 'http://qr.liantu.com/api.php?text=%s'

# 百度ai
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '16981700'
API_KEY = 'cHLC0p7dsOUVA0idSWQxV0lf'
SECRET_KEY = 'VZCXoeuHfViaAA2EThwIHLukAYcT0pf9'

AI_CLIENT = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

VOICE = {
    'vol': 5,
    'spd': 5,
    'pit': 6,
    'per': 4,
}
