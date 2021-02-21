# import the Flask class from the flask module
from flask import Flask, abort, render_template, redirect, url_for, request, session, send_from_directory, flash, jsonify
from markupsafe import escape
import random
import os
from werkzeug.utils import secure_filename
import json
from math import *
from database import Database as db

# create the application object
app = Flask(__name__)
UPLOAD_FOLDER = r'/home/pi/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'}
from os import walk

app.secret_key = b'\xa1\x98\xee\x04\x9d.\xa3\xcf\xc6\xc5\xb5\xf9\xc8u(\xef'
# use decorators to link the function to a url

def allowed_file(filename):
    return "." in filename

def getFiles(UPLOAD_FOLDER):
    f = []
    fo = []
    for (dirpath, dirnames, filenames) in walk(UPLOAD_FOLDER):
        f.extend(filenames)
        fo.extend(dirnames)
        break

    return f, fo

@app.route('/', methods=['GET', 'POST'])
def home():

    #iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><div class=\"navbar\" style='background-color: white;'><div class=\"dropdown\"><button class=\"dropbtn\" style='background-color: gray;'>Options <i class=\"fa fa-caret-down\"></i><div class=\"dropdown-content\"><a> </a><a href={2} class=\"fa fa-download\"> Download</a><a> </a><a href={3} class=\"fa fa-trash\"> Delete</a></div></button></div></div> </div></li><br><br><br>"

    iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><a href={2} class=\"fa fa-download\"> Download</a><a href={3} class=\"fa fa-trash\"> Delete</a></div></li><br><br><br>"

    fTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img src=https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678084-folder-512.png width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><a href={2} class=\"fa fa-trash\"> Delete</a> </div></li><br><br><br>"

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:

            return 'file not in files'
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename

        if file.filename == '':

            return 'no filename'
            return redirect(request.url)

        elif file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + f"/{session['username']}", filename))
            return redirect('/uploads/{}'.format(filename))

        else:

            return redirect("/")

    else:

        links=['<!--This Page Was Auto Generated-->\n<div align=\"center\">\n<br>\n<input type="text" id="mySearch" onkeyup="myFunction()" placeholder="Search.." title="Type in a category">\n<br><ul id="myMenu">']

        try:

            f, fo = getFiles(UPLOAD_FOLDER + f"/{session['username']}")
        
        except:

            return render_template('sitemap.html', links=" ", logged='You are not logged in')

        for thing in f:
            links.append(iTemplate.format('/uploads/'+thing, thing,'/uploads/'+thing+"/download", '/uploads/'+thing+"/delete"))

        for folder in fo:

            links.append(fTemplate.format('/folder/'+folder, folder, '/uploads/'+folder+'/delete'))

        links.append("\n  <li><a href='/newfolder'><i class='fa fa-plus'></i><b> New Folder</b></a></li>")
        links.append('</ul></div>')

        if 'username' in session:

            return render_template('sitemap.html', links=''.join(links), logged='Logged in as {}'.format(escape(session['username'])), username=escape(session['username']), loggedin=True)
        
        else:

            return render_template('sitemap.html', links=''.join(links), logged='You are not logged in')

@app.route('/folder/<folder>', methods=['GET', 'POST'])
def folderview(folder):

    #iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><div class=\"navbar\" style='background-color: white;'><div class=\"dropdown\"><button class=\"dropbtn\" style='background-color: gray;'>Options <i class=\"fa fa-caret-down\"></i><div class=\"dropdown-content\"><a> </a><a href={2} class=\"fa fa-download\"> Download</a><a> </a><a href={3} class=\"fa fa-trash\"> Delete</a></div></button></div></div> </div></li><br><br><br>"

    iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><a href={2} class=\"fa fa-download\"> Download</a><a href={3} class=\"fa fa-trash\"> Delete</a></div></li><br><br><br>"

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            
            return 'file not in files'
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename

        if file.filename == '':

            return 'no filename'
            return redirect(request.url)

        elif file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + f"/{session['username']}" + '/' + folder, filename))
            return redirect('/fuploads/{}/{}'.format(folder, filename))

        else:

            return redirect("/")

    else:

        links=[f'<!--This Page Was Auto Generated-->\n<div align=\"center\">\n<br><h1><b>{folder}</b></h1><br>\n<input type="text" id="mySearch" onkeyup="myFunction()" placeholder="Search.." title="Type in a category">\n<br><ul id="myMenu">']

        f, fo = getFiles(UPLOAD_FOLDER + f"/{session['username']}" + "/" + folder)

        for thing in f:
            links.append(iTemplate.format(f'/fuploads/{folder}/'+thing, thing,f'/fuploads/{folder}/'+thing+"/download", f'/fuploads/{folder}/'+thing+"/delete"))

        links.append("\n  <li><a href='/'><i class='fa fa-arrow-left'></i><b> Main Folder</b></a></li>")

        links.append('</ul></div>')

        if 'username' in session:

            return render_template('sitemap.html', links=''.join(links), logged='Logged in as {}'.format(escape(session['username'])), username=escape(session['username']), loggedin=True)

        else:

            return render_template('sitemap.html', links=''.join(links), logged='You are not logged in')

@app.route('/uploads/<path:filename>')
def display_file(filename):
    if filename!='<path:filename>':
        return send_from_directory(app.config['UPLOAD_FOLDER'] + f"/{session['username']}",
                                filename)
    else:

        return redirect('/')

@app.route('/uploads/<path:filename>/download')
def download_file(filename):
    if filename!='<path:filename>':
        return send_from_directory(app.config['UPLOAD_FOLDER'] + f"/{session['username']}",
                                filename, as_attachment=True)
    else:

        return redirect('/')

@app.route('/uploads/<path:filename>/delete')
def delete_file(filename):

    if os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + "/"  + filename):

        try:

            os.remove(UPLOAD_FOLDER + f"/{session['username']}" + "/" + filename)

        except:

            os.rmdir(UPLOAD_FOLDER + f"/{session['username']}" + "/" + filename)
    
    return redirect("/")

@app.route('/fuploads/<folder>/<path:filename>')
def fdisplay_file(folder, filename):
    if filename!='<path:filename>':
        return send_from_directory(app.config['UPLOAD_FOLDER'] + f"/{session['username']}" + f"/{folder}",
                                filename)
    else:

        return redirect('/')

@app.route('/fuploads/<folder>/<path:filename>/download')
def fdownload_file(folder, filename):
    if filename!='<path:filename>':
        return send_from_directory(app.config['UPLOAD_FOLDER'] + f"/{session['username']}" + f"/{folder}",
                                filename, as_attachment=True)
    else:

        return redirect('/folder/' + folder)

@app.route('/fuploads/<folder>/<path:filename>/delete')
def fdelete_file(folder, filename):

    if os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + f"/{folder}/" + filename):

        try:

            os.remove(UPLOAD_FOLDER + f"/{session['username']}" + f"/{folder}/" + filename)

        except:

            os.rmdir(UPLOAD_FOLDER + f"/{session['username']}" + f"/{folder}/" + filename)

    return redirect('/folder/' + folder)

@app.route('/newfolder', methods=['GET', 'POST'])
def makeFolder():

    if request.method == 'POST':
    
        folder = request.form['name']

        if not os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + '/' + folder):

            os.mkdir(UPLOAD_FOLDER + f"/{session['username']}" + '/' + folder)

        return redirect("/")
        
    else:

        return render_template("newfolder.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e)

@app.errorhandler(400)
def bad_requesthandler(e):
    return render_template('400.html', error=e)

@app.errorhandler(403)
def permissiondeniedhandler(e):
    return render_template('403.html', error=e)

@app.route("/sitemap/")
def sitemap():
    links = ['<!--This Page Was Auto Generated-->\n<div align=\"center\">\n<br>\n<input type="text" id="mySearch" onkeyup="myFunction()" placeholder="Search.." title="Type in a category">\n<br><ul id="myMenu">']
    for rule in app.url_map.iter_rules():
        if not str(rule.rule).startswith('/static/'):
            links.append("\n  <li><a align='center' href='{}'>{}</a><br></li>".format(rule.rule,rule.rule.title()))
    # links is now a list of url, endpoint tuples
    links.append('</ul></div>')
    return render_template('sitemap.html', links='\n'.join(links))

@app.route('/login/', methods=['POST', 'GET'])
def login():

    if request.method=='POST':

        data = db('logins.json')
        keys = data.keys()

        if request.form['username'] in keys:

            if request.form['password'] == data.get(request.form['username']):

                session['username'] = request.form['username']

                return redirect(url_for('home'))
            
            else:

                return render_template('login.html', error = f"Incorrect password for {request.form['username']}...")

        else:

            return render_template('login.html', error = f"Username {request.form['username']} not found...")

    return render_template('login.html')

@app.route('/register/', methods=['POST', 'GET'])
def register():

    if request.method=='POST':

        data = db('logins.json')
        keys = data.keys()

        if not request.form['username'] in keys:

            data.set(request.form['username'], request.form['password'])

            os.mkdir(UPLOAD_FOLDER + f"/{request.form['username']}")

            return render_template('register.html', error = 'You Are now Registered As {}'.format(request.form['username']))

        else:

            return render_template('register.html', error = 'The username "{}" is already in use.'.format(request.form['username']))

    return render_template('register.html')

@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
