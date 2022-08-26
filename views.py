from flask import Blueprint, render_template
import os
views = Blueprint(__name__, "views")

@views.route("/")
@views.route('/index')
def show_index():
    image_folder = os.path.join('static', 'img')
    app.config['IMAGE_FOLDER'] = image_folder
    ttc_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo_ttc.png')
    return render_template("index.html", name1="Johan", name2="Gerrit", action1="Added!", action2="Removed!",logo_image=ttc_logo)