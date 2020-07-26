#!/usr/bin/python
# -*- encoding:utf-8 -*-
import sys
import subprocess
from email.mime.text import MIMEText
import smtplib

class sendMail():

    def txtMail(self,content):
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')
        msg['to'] = '646861172@qq.com'
        msg['from'] = 'csplserver@xdcyber.cn'
        msg['subject'] = 'exec result'
        try:
            server = smtplib.SMTP_SSL('smtp.ym.163.com',994)
            # server.connect()
            server.login('csplserver@xdcyber.cn','7ZP3tsuZLq')
            server.sendmail(msg['from'], msg['to'],msg.as_string())
            server.quit()
            print("发送成功")
        except Exception as e:
            print(str(e))

if __name__=='__main__':
    comm= ' '.join( [ str(x) for x in sys.argv[1:]])
    (status, output) = subprocess.getstatusoutput(comm)
    sendMail().txtMail("comm:%s;status:%s;output:%s" % (comm,status,output))
