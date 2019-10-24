import hashlib
import os
import time
from uuid import uuid4

import requests

from config import QRCODE_URL, QRCODE_PATH, mongo


# QRCODE_URL = 'http://qr.liantu.com/api.php?text=%s'
# QRCODE_PATH = 'QRcode'


def get_code(count):
    code_list = []
    for i in range(count):
        code_name = hashlib.md5(f'{uuid4()}{time.time()}{uuid4()}'.encode('utf8')).hexdigest()
        code = requests.get(QRCODE_URL % code_name)
        code_path = os.path.join(QRCODE_PATH, code_name)
        # print(code_name)
        with open(f'{code_path}.jpg', 'wb') as fc:
            fc.write(code.content)
            code_list.append({'device_key': code_name})
    mongo.devices.insert_many(code_list)


if __name__ == '__main__':
    get_code(2)
