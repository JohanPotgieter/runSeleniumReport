import csv
import email.mime.application
import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import StringIO
from flask import Flask, render_template
from waitress import serve
import ftplib

app = Flask(__name__)


@app.route("/")
@app.route('/index')
def index():
    index_html = "index.html"
    today = datetime.now()
    report_date = today.strftime("%d/%m/%Y %H:%M:%S")
    site_data = {'report_date': report_date}
    data_file_path = "c:\\files\\addedusers.csv"
    if os.path.exists(data_file_path):
        addedusers = read_files(data_file_path, "add")
    else:
        addedusers = []
        logging.info('No Users where added')
    data_file_path = "c:\\files\\deletedusers.csv"
    if os.path.exists(data_file_path):
        deletedusers = read_files(data_file_path)
    else:
        deletedusers = []
        logging.info('No Users where deleted')
    data_file_path = "c:\\files\\incorrect_users.csv"
    if os.path.exists(data_file_path):
        incorrectusers = read_files(data_file_path)
    else:
        incorrectusers = []
        logging.info('No incorrect Users where found')
    data_file_path = "c:\\files\\full_user_list.csv"
    if os.path.exists(data_file_path):
        allusers = read_files(data_file_path)
        site_data['total_users'] = int(len(allusers))
    else:
        allusers = []
        logging.warning('No "All Users" File Found!')
    html = render_template(index_html, site_data=site_data, addedusers=addedusers, deletedusers=deletedusers,
                           allusers=allusers, incorrectusers=incorrectusers)
    new_index = f"index_{str(today.day)}_{str(today.month)}_{str(today.year)}_{str(today.hour)}_{str(today.minute)}_" \
                f"{str(today.second)}.html"
    save_to_file(html, new_index, False, True)
    strio = StringIO(html)
    strio.write(html)
    strio.seek(0)
    ftp_file("c:\\files\\" + new_index, new_index)
    return html


def read_files(data_file_path, filetype="deleted"):
    outoutvar = []
    with open(data_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) == 0:
                continue
            if filetype == 'add':
                outoutvar.append({'username': row, 'action': 'Added'})
            else:
                outoutvar.append({'username': row, 'action': 'Removed'})
    return outoutvar


def send_email(report_date, file_date):
    attachmentpath = "C:\\Users\\johan\\PycharmProjects\\runSeleniumReport\\output.pdf"
    smtp_ssl_host = 'mail.amberitservices.com.au'
    smtp_ssl_port = 465
    s = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    mail_user = 'xxx'
    mail_password = 'xxx'
    s.login(mail_user, mail_password)

    msg = MIMEMultipart()
    msg['Subject'] = f'TbD Invite-Only script Daily Report - {str(report_date)}'
    msg['From'] = mail_user
    msg['To'] = 'tradetravelchill@gmail.com'
    msg['CC'] = 'johan@amberitservices.com.au'

    txt = MIMEText('Hi Annii,\n\nPlease find the report for today attached to this email.\n\nThe Report includes a '
                   'list of all new users added today, users removed today, users with incorrect TV usernames or '
                   'ones we could not removed because the TV username does not exist on our list, and a list of all '
                   'users with access to the Trade By Design Indicator.\n\nRegards,\nIT Team')
    msg.attach(txt)

    filename = f'TbD_Report_{str(file_date)}.pdf'
    with open(attachmentpath, 'rb') as fo:
        attach = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")
    attach.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attach)
    s.send_message(msg)
    s.quit()


def ftp_file(filelocation, filename):
    host = "ftp.amberitservices.com.au"
    user = "python_user@ttc.amberitservices.com.au"
    password = ")W~6+!!VMRu=G#LfNb"
    # connect to the FTP server
    ftp = ftplib.FTP(host, user, password)
    # force UTF-8 encoding
    ftp.encoding = "utf-8"
    with open(filelocation, "rb") as file:
        # use FTP's STOR command to upload the file
        ftp.storbinary(f"STOR {filename}", file)
    ftp.quit()


def save_to_file(listitem, filename, blob=False, plaintext=False):
    data_file_path = "c:\\files\\" + str(filename)
    with open(data_file_path, mode='w') as myfile:
        if any(isinstance(el, list) for el in listitem):
            for newlist in listitem:
                myfile.write(','.join(newlist) + '\n')
        elif blob is True:
            lines_new = listitem.split("\n")
            for lines in lines_new:
                myfile.write(lines + '\n')
        else:
            if plaintext:
                myfile.write(listitem)
            else:
                for lines in listitem:
                    myfile.write(lines + '\n')


if __name__ == '__main__':
    #app.run("127.0.0.1", "9456", True)
    serve(app, host="127.0.0.1", port=9456)
