# coding: utf8
import sys
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms

from settings import AES_KEY, AES_IV


class AesCbc(object):
    def __init__(self, key, iv):
        self.key = key.encode("utf8")
        self.iv = iv.encode("utf8")
        self.mode = AES.MODE_CBC

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text: str):
        try:
            cryptor = AES.new(self.key, self.mode, self.iv)
            # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
            # length = 16
            # count = len(text)
            # if count % length != 0:
            #     add = length - (count % length)
            # else:
            #     add = 0

            text = text.encode("utf8")
            text = self.pkcs7_padding(text)

            self.ciphertext = cryptor.encrypt(text)
            # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串 ,当然也可以转换为base64加密的内容，可以使用b2a_base64(self.ciphertext)
            return base64.b64encode(self.ciphertext).decode("utf8")
        except Exception as e:
            return None

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, encrypt_str):
        try:
            cipher = AES.new(self.key, self.mode, self.iv)
            # encrypt_str += (len(encrypt_str) % 4)*"="
            # decrypt_bytes = base64.urlsafe_b64decode(encrypt_str)
            decrypt_bytes = base64.b64decode(encrypt_str)
            msg = str(cipher.decrypt(decrypt_bytes), encoding='utf-8')
            unpad = lambda s: s[0:-ord(s[-1])]
            return unpad(msg)
        except Exception as e:
            return None


aes_cbc = AesCbc(AES_KEY, AES_IV)
