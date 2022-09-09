from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.mime.application
from flask import Flask, render_template
from datetime import datetime
import os
import csv
import logging
from waitress import serve
import pdfkit
import smtplib

app = Flask(__name__)


@app.route("/")
@app.route('/index')
def index():
    today = datetime.today()
    report_date = today.strftime("%d/%m/%Y %H:%M:%S")
    file_date = today.strftime("%d_%m_%Y_%H_%M_%S")
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
    else:
        allusers = []
        logging.warning('No "All Users" File Found!')
    temp = render_template("index.html", site_data=site_data, addedusers=addedusers, deletedusers=deletedusers,
                           allusers=allusers, incorrectusers=incorrectusers)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(temp, "output.pdf", configuration=config)
    send_email(report_date, file_date)
    return render_template("index.html", site_data=site_data, addedusers=addedusers, deletedusers=deletedusers,
                           allusers=allusers, incorrectusers=incorrectusers)


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
    mail_user = 'johan@amberitservices.com.au'
    mail_password = '#4J$HiLRu$^Lv@&x^2i'
    s.login(mail_user, mail_password)

    msg = MIMEMultipart()
    msg['Subject'] = 'TbD Invite-Only script Daily Report - ' + str(report_date)
    msg['From'] = mail_user
    msg['To'] = 'tradetravelchill@gmail.com'
    msg['CC'] = 'johan@amberitservices.com.au'

    txt = MIMEText('Hi Annii,\n\nPlease find the report for today attached to this email.\n\nThe Report includes a '
                   'list of all new users added today, users removed today, users with incorrect TV usernames or '
                   'ones we could not removed because the TV username does not exist on our list, and a list of all '
                   'users with access to the Trade By Design Indicator.\n\nRegards,\nIT Team')
    msg.attach(txt)

    filename = 'TbD_Report_' + str(file_date) + '.pdf'
    fo = open(attachmentpath, 'rb')
    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attach)
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    serve(app, host="127.0.0.1", port=9456)
