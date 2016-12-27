# coding: utf-8
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import traceback

smtpaddr_1 = "10.64.1.86"  
smtpaddr_2 = "10.64.1.85"
server = "10.204.16.7"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('email.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

msgIma = ""
msg_html = ""
mail_msg = MIMEMultipart('related')


def sendmail(content):
    logger.info('now entering sendmail...')
    if content['from_user'] == '' or not len(content['to_user']):
        print('from_user or to_user is empty!')
        logger.error('from_user or to_user is empty!')
        return

    if 'work_dir' not in content.keys():
        print('directory error!')
        logger.error('directory is empty!')
        return

    global msg_html, msgIma, mail_msg
    insert_image(content)
    read_html(content)
    msg = msgIma + msg_html
    if msg == '':
        print ('pic_num and html_num all is empty')
        logger.error('pic_num and html_num all is empty')
        return
    if not isinstance(content['subject'], unicode):
        content['subject'] = unicode(content['subject'], 'utf-8')
    mail_msg['Subject'] = content['subject']
    mail_msg['From'] = content['from_user']
    mail_msg['To'] = ','.join(content['to_user'])
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))

    read_image(content)
    try:
        s = smtplib.SMTP()
        s.connect(server)
        s.sendmail(mail_msg['From'], content['to_user'], mail_msg.as_string())
        s.quit()
        print('success')
    except Exception as e:
        print "Error: unable to send email", e
        print traceback.format_exc()


def insert_image(content):
    index = 0
    global msgIma
    for item in content['pic_name']:
        if os.path.isfile(os.path.join(content['work_dir'], item)):
            msgIma += '''<p style="text-align:center"><img alt="" src="cid:image''' + str(index) + ''' " width="800" height="600"></p> '''
            index += 1


def read_html(content):
    global msg_html
    for item in content['html_name']:
        if os.path.isfile(os.path.join(content['work_dir'], item)):
            with open(os.path.join(content['work_dir'], item), "r+") as file_handle:
                msg_html += file_handle.read()


def read_image(content):
    index = 0
    global mail_msg
    for item in content['pic_name']:
        if os.path.isfile(os.path.join(content['work_dir'], item)):
            with open(os.path.join(content['work_dir'], item), 'rb') as data:  # picture path
                msg_image = MIMEImage(data.read())
            msg_image.add_header('Content-ID', '<image' + str(index) + '>')
            mail_msg.attach(msg_image)
            index += 1


if __name__ == '__main__':
    fromaddr = "haitao_hu@trendmicro.com.cn"
    toaddrs = ["graysen_tong@trendmicro.com.cn"]
    pic_name = ['']
    html_name = ['3.html']
    work_dir = 'd:\\python\\'
    subject = "title"
    content_dict = {'to_user': toaddrs, 'from_user': fromaddr, 'pic_name': pic_name, 'html_name': html_name,
                    'work_dir': work_dir, 'subject': subject}
    sendmail(content_dict)





