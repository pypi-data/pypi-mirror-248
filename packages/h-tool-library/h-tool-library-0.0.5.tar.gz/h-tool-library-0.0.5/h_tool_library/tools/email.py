from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from typing import List

from .base import validate_email


class Email:
    def __init__(self, password: str, host="smtp.qq.com", port=465):
        """
        :param password: 授权码
        :param host: 邮箱服务商 默认smtp.qq.com
        :param port: 端口
        """
        self.password = password
        self.host = host
        self.port = port

    def send_email(self, sender: str, receivers: List[str], subject: str, message: str, name: str):
        """
            发送邮件
        :param name: 接收者的别名
        :param sender: 发送人的邮箱地址
        :param receivers: 接收人邮箱地址，支持多个
        :param subject: 邮件的标题
        :param message: 信息
        :return:
        """
        assert sender, "Sender Required"
        assert validate_email(sender), "Sender is Email"
        assert len(receivers) > 0, "Receivers Required"
        assert all([validate_email(i) for i in receivers]), "Receivers is Email"
        message = MIMEText(message, _subtype='plain', _charset='utf-8')
        message['From'] = Header(sender)  # 邮件的发送者
        message['To'] = Header(name, 'utf-8')  # 邮件的接收者
        message['Subject'] = Header(subject, 'utf-8')  # 邮件的标题
        with SMTP_SSL(host=self.host, port=self.port) as smtp:
            smtp.login(sender, self.password)
            smtp.sendmail(sender, receivers, message.as_string())
