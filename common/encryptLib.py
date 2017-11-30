# coding=utf-8

import base64
import hashlib
import json
import re
import pyDes
from Crypto.Cipher import AES


def md5_encode(data):
    """ md5加密 """
    if isinstance(data, str):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()
    else:
        print ('MD5加密传入的数据格式不正确。')
        return None


def sha1_encode(data):
    """ sha1加密 """
    s = hashlib.sha1()
    s.update(data)
    return s.hexdigest()


def base64_encode(data):
    """ base64加密 """
    b64 = base64.b64encode(data)
    return b64


def base64_decode(encrypted):
    """ base64解密 """
    '''补齐等号'''
    missing_padding = 4 - len(encrypted) % 4
    if missing_padding:
        encrypted += b'=' * missing_padding
    # print '需解密字符为: ', encrypted
    data = base64.b64decode(encrypted)
    return data


# def des_encode(data):
#     """ DES加密 """
#     k = pyDes.des('key', padmode=pyDes.PAD_PKCS5)
#     encodeStr = k.encrypt(json.dumps(data))
#     return base64.b64encode(encodeStr)  # 转base64编码返回

def des_encode(data):
    """ DES加密 """
    print type(data)
    if isinstance(data, dict):
        print '字典转成json'
        data = json.dumps(data)
    print type(data)
    # data = json.dumps(data)
    patten = re.compile("\s+")
    data = re.sub(patten, '', data)
    print '将json格式params去掉空格、换行: ', data

    k = pyDes.des(key='uirhfyyj', mode=pyDes.CBC, IV='uirhfyyj', padmode=pyDes.PAD_PKCS5)
    encodeStr = k.encrypt(data)
    miwen = base64.b64encode(encodeStr)  # 转base64编码返回
    print '加密后的密文：', miwen
    return miwen


def des_encode_new():
    pass


class AesEncode():
    """AES加密"""
    def __init__(self, key, iv, mode=AES.MODE_CBC):
        self.key = key
        self.iv = iv
        self.mode = mode
        print '加密key为: ', self.key
        print '加密iv为: ', self.iv
        print '加密模式为: ', self.mode

    def aes_encode(self, data):
        """加密通用方法"""
        # json格式都是双引号
        # 统一格式
        if isinstance(data, dict):
            # params = json.dumps(params, encoding='utf-8')
            # 转成json格式
            params = json.dumps(data)
            print params
            print type(params)
            patten = re.compile("\s+")
            params = re.sub(patten, '', params)
            print '将json格式params去空格、换行: ', params
        generator = AES.new(self.key, self.mode, self.iv)
        crypt = generator.encrypt(self._pkcs7padding(params))
        cryptedStr = base64.b64encode(crypt)
        print '加密后字符串为: ', cryptedStr
        return cryptedStr

    def _pkcs7padding(self, data):
        """
        对齐块
        size 16
        999999999=>9999999997777777
        """
        size = AES.block_size
        count = size - len(data) % size
        if count:
            data += (chr(count) * count)
        return data


def mj_aes_encode(params):
    """美借AES加密"""
    key = 'abcdnnnnnn123456'.encode('utf-8')
    iv = (md5_encode(b"meijie_2016")[8:24]).encode('utf-8')
    mj_aes = AesEncode(key, iv)

    if isinstance(params, dict):
        params = json.dumps(params, encoding='utf-8')
        patten = re.compile("\s+")
        params = re.sub(patten, '', params)
        print ('将字典格式params去空格、换行: ', params)

    cryptedStr = mj_aes.aes_encode(params)
    return cryptedStr


def zhiyu_aes_encode(data):
    # AES加密方式
    key = 'ia1Yh85O26LARD8M'
    iv = '1234567890123456'
    zhiyu_aes = AesEncode(key, iv)
    aes_code = zhiyu_aes.aes_encode(data)
    return aes_code


def zhiyu_des_encode(data):
    # app,DES加密方式
    des_code = des_encode(data)
    return des_code


if __name__ == '__main__':
    # data = {
    #         'source': 1, 'version': '1.0.1', 'mobile': '18211078892', 'password': '12345678'
    #         }

    # # data = 'hello world!'
    # data = {'user': '18211078892', 'pwd': '123456'}
    # # data = {'a': 'a', 'b': 'b'}
    # # a = mj_aes_encode(data)
    # a = base64_encode(data)
    # print a
    # data = {
    #     'a':'a',
    #     'b':'b'
    # }
    data = {"a":"a","b":"b"}
    s = zhiyu_des_encode(data)
    print s
