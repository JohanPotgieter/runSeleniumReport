from flask import Flask, render_template
from datetime import datetime
import os
import csv
import logging
from waitress import serve
app = Flask(__name__)


@app.route("/")
@app.route('/index')
def show_index():
    image_folder = os.path.join('static', 'img')
    app.config['IMAGE_FOLDER'] = image_folder
    ttc_logo = os.path.join(app.config['IMAGE_FOLDER'], 'logo_ttc.png')
    site_data = {'logo_image': ttc_logo}
    today = datetime.today()
    report_date = today.strftime("%d/%m/%Y %H:%M:%S")
    site_data['report_date'] = report_date
    data_file_path = "c:\\files\\addedusers.csv"
    if os.path.exists(data_file_path):
        addedusers = read_files(data_file_path, "add")
    else:
        addedusers = []
        logging.info('No Users where added')
    data_file_path = "c:\\files\\deletedusers.csv"
# data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'deletedusers.csv')
    if os.path.exists(data_file_path):
        deletedusers = read_files(data_file_path)
    else:
        deletedusers = []
        logging.info('No Users where deleted')
    data_file_path = "c:\\files\\incorrect_users.csv"
    # data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'incorrect_users.csv')
    if os.path.exists(data_file_path):
        incorrectusers = read_files(data_file_path)
    else:
        incorrectusers = []
        logging.info('No incorrect Users where found')
    data_file_path = "c:\\files\\full_user_list.csv"
    # data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'full_user_list.csv')
    if os.path.exists(data_file_path):
        allusers = read_files(data_file_path)
    else:
        allusers = []
        logging.warning('No All Users File Found!')
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


if __name__ == '__main__':
    serve(app, host="127.0.0.1", port=9456)
