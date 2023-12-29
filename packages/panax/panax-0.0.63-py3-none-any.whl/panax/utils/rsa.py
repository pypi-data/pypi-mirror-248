import sys, os

sys.path.append(os.getcwd())
try:
    from config import APP_SETTING
except Exception:
    APP_SETTING = {}

import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA


public_key = APP_SETTING["key"]["public"] if "key" in APP_SETTING else ""
private_key = APP_SETTING["key"]["private"] if "key" in APP_SETTING else ""


# ------------------------生成密钥对------------------------
def create_rsa_pair(is_save=False):
    '''
    创建rsa公钥私钥对
    :param is_save: default:False
    :return: public_key, private_key
    '''
    f = RSA.generate(2048)
    private_key = f.exportKey("PEM")  # 生成私钥
    public_key = f.publickey().exportKey()  # 生成公钥
    if is_save:
        with open("crypto_private_key.pem", "wb") as f:
            f.write(private_key)
        with open("crypto_public_key.pem", "wb") as f:
            f.write(public_key)
    return public_key, private_key


def read_public_key(file_path="crypto_public_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


def read_private_key(file_path="crypto_private_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


# ------------------------加密------------------------
def encryption(text: str):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


# ------------------------解密------------------------
def decryption(text_encrypted_base64: str):
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted


if __name__ == '__main__':
    # 生成密钥对
    # create_rsa_pair(is_save=True)
    # public_key = read_public_key()
    # private_key = read_private_key()
    public_key, private_key = create_rsa_pair(is_save=False)

    print("=== python ===")
    print(public_key)
    print(private_key)

    print("=== javascript ===")
    print(str(public_key).replace('\\n', ''))
    print(str(private_key).replace('\\n', ''))



    # python 中 直接使用生成的key，js中要去掉 \n

    # 加密
    # text = '123456'
    # text_encrypted_base64 = encryption(text)
    # print('密文：', text_encrypted_base64)

    # 解密
    # text_decrypted = decryption(text_encrypted_base64)
    # print('明文：', text_decrypted)
