# # -*- coding: utf-8 -*-
# import pymysql
# # __Desc__ = 从数据库中导出数据到excel数据表中
# import xlwt
# import pymysql
#
#
# class MYSQL:
#     def __init__(self):
#         pass
#
#     def __del__(self):
#         self._cursor.close()
#         self._connect.close()
#
#     def connectDB(self):
#         """
#         连接数据库
#         :return:
#         """
#         try:
#             self._connect = pymysql.Connect(
#                 host='localhost',
#                 port=3306,
#                 user='root',
#                 passwd='zkyr1006',
#                 db='python',
#                 charset='utf8'
#             )
#
#             return 0
#         except:
#             return -1
#
#     def export(self, table_name):
#         self._cursor = self._connect.cursor()
#         count = self._cursor.execute('select * from '+table_name)
#         # print(self._cursor.lastrowid)
#         print(count)
#         # 重置游标的位置
#         self._cursor.scroll(0, mode='absolute')
#         # 搜取所有结果
#         results = self._cursor.fetchall()
#
#         # 获取MYSQL里面的数据字段名称
#         fields = self._cursor.description
#         workbook = xlwt.Workbook()
#         table_name=table_name+'.xlsx'
#
#         # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
#         # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
#         sheet = workbook.add_sheet('table_'+table_name, cell_overwrite_ok=True)
#
#         # 写上字段信息
#         for field in range(0, len(fields)):
#             sheet.write(0, field, fields[field][0])
#
#         # 获取并写入数据段信息
#         row = 1
#         col = 0
#         for row in range(1,len(results)+1):
#             for col in range(0, len(fields)):
#                 sheet.write(row, col, u'%s' % results[row-1][col])
#
#         workbook.save(table_name)
#
#
# if __name__ == '__main__':
#     mysql = MYSQL()
#     flag = mysql.connectDB()
#     if flag == -1:
#         print('数据库连接失败')
#     else:
#         print('数据库连接成功')
#         mysql.export('douban_books')
#
#
#
#
# import smtplib
# # import email.mime.multipart
# from email.header import Header
# import email.mime.text
# from email.mime.text import MIMEText

# msg = email.mime.multipart.MIMEMultipart()
# msgFrom = '826908021@qq.com' #从该邮箱发送
# msgTo = '799960740@qq.com' #发送到该邮箱
# smtpSever='smtp.163.com' # qq邮箱的smtp Sever地址
# smtpPort = '465' #开放的端口
# sqm='jtomjlibaioqbdch'  # 在登录smtp时需要login中的密码应当使用授权码而非账户密码
#
# msg['from'] = msgFrom
# msg['to'] = msgTo
# msg['subject'] = 'Python自动邮件-'#+dataNumber
# content = '''
# 你好:
#     这是一封python3发送的邮件
# '''
# txt = email.mime.text.MIMEText(content)
# msg.attach(txt)
# # smtp = smtplib
# smtp = smtplib.SMTP()
# '''
# smtplib的connect（连接到邮件服务器）、login（登陆验证）、sendmail（发送邮件）
# '''
# smtp.connect(smtpSever, smtpPort)
# smtp.login(msgFrom, sqm)
# smtp.sendmail(msgFrom, msgTo, str(msg))
# # s = smtplib.SMTP("localhost")
# # s.send_message(msg)
# smtp.quit()



# def sendmail(subject, content):
#     email_host = 'smtp.qq.com'     # 发送者是163邮箱
#     email_user = '826908021@qq.com'  # 发送者账号
#     email_pwd = 'jtomjlibaioqbdch'       # 发送者密码
#     maillist ='799960740@qq.com'    # 接收者账号，本来想写成[]list的，但是报错，还没解决！
#     # 三个参数：第一个为文本内容，第二个 html 设置文本格式，第三个 utf-8 设置编码
#     msg = email.mime.text.MIMEText(content, 'html', 'utf-8')    # 邮件内容
#     msg['Subject'] = subject    # 邮件主题
#     msg['From'] = email_user    # 发送者账号
#     msg['To'] = maillist    # 接收者账号
#
#     smtp = smtplib.SMTP(email_host) # 如上变量定义的，是163邮箱
#     smtp.login(email_user, email_pwd)   # 发送者的邮箱账号，密码
#     smtp.sendmail(email_user, maillist, str(msg))    # 参数分别是发送者，接收者，第三个不知道
#     smtp.quit() # 发送完毕后退出smtp
#     print ('email send success.')
#
#
# sendmail('test', 'aaa')    # 调用发送邮箱的函数

# from email import encoders
# from email.header import Header
# from email.mime.text import MIMEText
# from email.utils import parseaddr, formataddr
# import smtplib
#
# def _format_addr(s):
#     name, addr = parseaddr(s)
#     return formataddr((Header(name, 'utf-8').encode(), addr))
#
# from_addr = '826908021@qq.com'
# password = 'jtomjlibaioqbdch'
# to_addr = '799960740@qq.com'
# smtp_server = 'smtp.qq.com'
#
# msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
# msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
# msg['To'] = _format_addr('管理员 <%s>' % to_addr)
# msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
#
# server = smtplib.SMTP(smtp_server, 587)
# server.set_debuglevel(1)
# server.login(from_addr, password)
# server.sendmail(from_addr, [to_addr], msg.as_string())
# server.quit()

