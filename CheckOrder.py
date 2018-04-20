# -*- coding:utf-8 -*-

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import http.client
import time

# server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject="", text="", files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro  # 邮件的发件人
    msg['Subject'] = subject  # 邮件的主题
    msg['To'] = COMMASPACE.join(to)  # COMMASPACE==', ' 收件人可以是多个，to是一个列表
    msg['Date'] = formatdate(localtime=True)  # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期
    # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    for file in files:  # 添加附件可以是多个，files是一个列表，可以为空
        part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
        with open(file, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP()
    # smtp = smtplib.SMTP_SSL()  # 使用SSL的方式去登录(例如QQ邮箱，端口是465)
    smtp.connect(server['name'])  # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
    smtp.login(server['user'], server['passwd'])  # 用户名，密码
    smtp.sendmail(fro, to, msg.as_string())  # 发件人，收件人，发送信息
    smtp.close()  # 关闭连接


currentdate=time.strftime("%Y%m%d", time.localtime())
#currentdate="20180408"
conn = http.client.HTTPSConnection("8yn728b1.api.lncld.net")

headers = {
    'cache-control': "no-cache",
    'postman-token': "f821d1fe-2f97-cfdc-31a9-ee898e0d950c",
    'x-lc-id': "8yn728b10nhuaxdj7avn3t1kwvgql80o4gd9vchqp183y167",
    'x-lc-key': "ukyhg9ul7ef3v5qe6p3f9142haxs4sodufi0ot4etp9bafvt"
    }

conn.request("GET", "/1.1/cloudQuery?cql=select%20ordertime%2CrecipientName%2CrecipientPhone%2CrecipientAddress%20from%20ShdxEventOrder%20where%20ordertime%3E%22"+currentdate+"000000%22%20and%20orderStatus%3D%22%E6%94%AF%E4%BB%98%E6%88%90%E5%8A%9F%22%20order%20by%20createdAt%20desc%20limit%2020", headers=headers)

res = conn.getresponse()
data = res.read()

#print(data.decode("unicode-escape"))

if __name__ == '__main__':
    server = {'name': 'smtp.exmail.qq.com',
              'user': 'tv@720health.com',
              'passwd': '720Health!'}
    fro = 'tv@720health.com'
    to = ['liujiaxin@720health.com']
    subject = '上海电信活动-环境宝3一台-需要发货'
    text = data.decode("unicode-escape")

    if "recipientAddress" in data.decode("unicode-escape"):
        send_mail(server, fro, to, subject, text)
    else:
        print("There is no order today!")