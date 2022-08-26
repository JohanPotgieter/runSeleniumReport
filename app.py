from flask import Flask, render_template
from datetime import datetime
import os
import csv
from var_dump import var_dump

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
    userdata = []
    count = 0
    # data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'users.csv')
    # with open(data_file_path, 'r') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in reader:
    #         if len(row) == 0:
    #             continue
    #         if count != 0:
    #             userdata.append({'username': row[3], 'action': row[4]})
    #         count += 1
    data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'addedusers.csv')
    addedusers = read_files(data_file_path, "add")
    data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'deletedusers.csv')
    deletedusers = read_files(data_file_path)
    # var_dump(addedusers)
    # var_dump(deletedusers)
    data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'incorrect_users.csv')
    incorrectusers = read_files(data_file_path)
    var_dump(incorrectusers)
    data_file_path = os.path.join(os.path.dirname(__file__), 'static\\files', 'full_user_list.csv')
    allusers = read_files(data_file_path)
    return render_template("index.html", site_data=site_data, addedusers=addedusers, deletedusers=deletedusers, allusers=allusers, incorrectusers=incorrectusers)


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
    app.run(debug=True, port=9456)