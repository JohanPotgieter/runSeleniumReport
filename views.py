from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
import email.mime.application

attachmentpath = "C:\\Users\\johan\\PycharmProjects\\runSeleniumReport\\output.pdf"
smtp_ssl_host = 'mail.amberitservices.com.au'
smtp_ssl_port = 465
s = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
mail_user = 'johan@amberitservices.com.au'
mail_password = '#4J$HiLRu$^Lv@&x^2i'
s.login(mail_user, mail_password)

msg = MIMEMultipart()
msg['Subject'] = 'I have a picture'
msg['From'] = mail_user
msg['To'] = mail_user

txt = MIMEText('I just bought a new camera.')
msg.attach(txt)

filename = 'output.pdf' #path to file
fo = open(attachmentpath, 'rb')
attach = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")
fo.close()
attach.add_header('Content-Disposition', 'attachment', filename=filename)
msg.attach(attach)
s.send_message(msg)
s.quit()
