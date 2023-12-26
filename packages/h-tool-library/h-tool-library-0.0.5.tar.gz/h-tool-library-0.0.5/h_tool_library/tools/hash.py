"""
    基础加密
"""

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


def md5_(s: str) -> str:
    """
    数据 -> md5
    :return:
    """
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()


def password_encry(password: str, method: str = "scrypt", salt_length: int = 16) -> str:
    """
        对密码进行sha256 加密
    :param salt_length:
    :param method:
    :param password:
    :return:
    """
    return generate_password_hash(password, method, salt_length)


def check_encry_password(pwhash: str, password: str):
    """
        对密码进行校验，判断是否是相同密码
    :param pwhash:
    :param password: 用户传递的密码
    :return:
    """
    return check_password_hash(pwhash, password)
