from ipts import *
from funcs import *

# create the application object
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'\xa1\x98\xee\x04\x9d.\xa3\xcf\xc6\xc5\xb5\xf9\xc8u(\xef'

app.register_blueprint(f2)

if not os.path.exists("logins.json"):

    with open("logins.json", "w") as file:

        file.write("{}")

@app.route('/', methods=['GET', 'POST'])
def home():

    #iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><div class=\"navbar\" style='background-color: white;'><div class=\"dropdown\"><button class=\"dropbtn\" style='background-color: gray;'>Options <i class=\"fa fa-caret-down\"></i><div class=\"dropdown-content\"><a> </a><a href={2} class=\"fa fa-download\"> Download</a><a> </a><a href={3} class=\"fa fa-trash\"> Delete</a></div></button></div></div> </div></li><br><br><br>"

    iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='{4}';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\" class='menu' ><table><tr><th><a href={5} class=\"fa fa-edit\"> Edit</a></th><th><a href={2} class=\"fa fa-download\"> Download</a></th><th><a href={3} class=\"fa fa-trash\"> Delete</a></th></tr></table></div></li><br><br><br>"

    fTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img src=https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678084-folder-512.png width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><table><tr><th><a href={2} class=\"fa fa-trash\"> Delete</a> </th></tr></table></div></li><br><br><br>"

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
            links.append(iTemplate.format('/uploads/'+thing, thing,'/uploads/'+thing+"/download", '/uploads/'+thing+"/delete", "https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png" if isImage(getExt(thing)) else "https://cdn4.iconfinder.com/data/icons/48-bubbles/48/12.File-512.png", f'/uploads/'+thing+"/edit"))

        for folder in fo:

            links.append(fTemplate.format('/'+folder, folder, '/uploads/'+folder+'/delete'))

        links.append("\n  <li><table><tr><th><a href='/newfolder'><i class='fa fa-plus'></i><b> New Folder</b></a></th><th><a href='/newfile'><i class='fa fa-plus'></i><b> New File</b></a></th></tr></table></li>")
        #links.append("\n  <li></li>")
        links.append('</ul></div>')

        if 'username' in session:

            return render_template('sitemap.html', links=''.join(links), logged='Logged in as {}'.format(escape(session['username'])), username=escape(session['username']), loggedin=True)
        
        else:

            return render_template('sitemap.html', links=''.join(links), logged='You are not logged in')

@app.route('/<path:folder>/', methods=['GET', 'POST'])
def folderview(folder):

    fTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img src=https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678084-folder-512.png width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><table><tr><th><a href={2} class=\"fa fa-trash\"> Delete</a> </th></tr></table></div></li><br><br><br>"

    iTemplate = "\n  <li><a align='left' href='{0}'><span align=left><img onerror=\"this.onerror=null;this.src='{4}';\" src={0} width='100' height='100' align=left/></span> <span class='rig'><b><br><br><br>{1}</b></span></a><div align=\"right\"><table><tr><th><a href={5} class=\"fa fa-edit\"> Edit</a></th><th><a href={2} class=\"fa fa-download\"> Download</a></th><th><a href={3} class=\"fa fa-trash\"> Delete</a></th></tr></table></div></li><br><br><br>"

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
            return redirect('/uploads/{}/{}'.format(folder, filename))

        else:

            return redirect("/")

    else:

        breadcrumbs = folder.split("/")

        bread = []
        active=""

        for i in breadcrumbs:

            active += "/"+i

            bread.append(f"<a href=\"{active}\" style='color: gray; text-decoration: underline dotted;' >{i}</a>")

        breadcrumb = " > ".join(bread)

        links=[f'<!--This Page Was Auto Generated-->\n<div align=\"center\">\n<br><h1>{breadcrumb}</h1><br>\n<input type="text" id="mySearch" onkeyup="myFunction()" placeholder="Search.." title="Type in a category">\n<br><ul id="myMenu">']

        f, fo = getFiles(UPLOAD_FOLDER + f"/{session['username']}" + "/" + folder)

        for thing in f:
            links.append(iTemplate.format(f'/uploads/{folder}/'+thing, thing, f'/uploads/{folder}/'+thing+"/download", f'/uploads/{folder}/'+thing+"/delete", "https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-image-512.png" if isImage(getExt(thing)) else "https://cdn4.iconfinder.com/data/icons/48-bubbles/48/12.File-512.png", f'/uploads/{folder}/'+thing+"/edit",))

        for folder2 in fo:
            links.append(fTemplate.format('/'+folder+"/"+folder2, folder2, '/uploads/'+folder+"/"+folder2+'/delete'))

        links.append(f"\n  <li><table><tr><th><a href='/{'/'.join(folder.split('/')[0:-1])}'><i class='fa fa-arrow-left'></i><b> Back</b></a></th><th><a href='/{folder}/newfolder'><i class='fa fa-plus'></i><b> New Folder</b></a></th><th><a href='/{folder}/newfile'><i class='fa fa-plus'></i><b> New File</b></a></th></tr></table></li>")
        #links.append(f"\n  <li></li>")
        #links.append(f"\n  <li></li>")
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

        if "/" in filename:
        
            return redirect('/' + '/'.join(filename.split('/')[0:-1]))
        
        else:

            return redirect("/")

@app.route('/uploads/<path:filename>/download')
def download_file(filename):
    if filename!='<path:filename>':
        return send_from_directory(app.config['UPLOAD_FOLDER'] + f"/{session['username']}",
                                filename, as_attachment=True)
    else:

        if "/" in filename:
        
            return redirect('/' + '/'.join(filename.split('/')[0:-1]))
        
        else:

            return redirect("/")

@app.route('/uploads/<path:filename>/delete')
def delete_file(filename):

    if os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + "/"  + filename):

        try:

            os.remove(UPLOAD_FOLDER + f"/{session['username']}" + "/" + filename)

        except:

            try:

                os.rmdir(UPLOAD_FOLDER + f"/{session['username']}" + "/" + filename)

            except Exception as e:

                abort(405, f"{filename} is a folder and is not empty!")
    
    if "/" in filename:
        
        return redirect('/' + '/'.join(filename.split('/')[0:-1]))
    
    else:

        return redirect("/")

@app.route('/uploads/<path:filename>/edit', methods=['GET', 'POST'])
def edit_file(filename):

    if request.method == 'POST':

        with open(UPLOAD_FOLDER + f"/{session['username']}" + '/' + filename, 'w') as f:

            f.write(request.form['nm'])

            return redirect(f'/uploads/{filename}')
    
    else:

        with open(UPLOAD_FOLDER + f"/{session['username']}" + '/' + filename, 'r') as f:
            
            o = f.read()

        return render_template('edit.html', old=o)

@app.route('/newfolder', methods=['GET', 'POST'])
def makeFolder():

    if request.method == 'POST':
    
        folder = request.form['name']

        if not os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + '/' + folder):

            os.mkdir(UPLOAD_FOLDER + f"/{session['username']}" + '/' + folder)

        return redirect("/")
        
    else:

        return render_template("newfolder.html")
        
@app.route('/<path:fo>/newfolder', methods=['GET', 'POST'])
def makeFolderNested(fo):

    if request.method == 'POST':
    
        folder = request.form['name']

        if not os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + '/' + fo + "/" + folder):

            os.mkdir(UPLOAD_FOLDER + f"/{session['username']}" + '/' + fo + "/" + folder)

        return redirect(f"/{fo}")
        
    else:

        return render_template("newfolder.html")

@app.route('/newfile', methods=['GET', 'POST'])
def makeFile():

    if request.method == 'POST':
    
        filename = request.form['name']

        if not os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + '/' + filename):

            with open(UPLOAD_FOLDER + f"/{session['username']}" + "/" + filename, 'w') as f:

                f.write("")

        return redirect("/")
        
    else:

        return render_template("newfile.html")
        
@app.route('/<path:fi>/newfile', methods=['GET', 'POST'])
def makeFileNested(fi):

    if request.method == 'POST':
    
        filename = request.form['name']

        if not os.path.exists(UPLOAD_FOLDER + f"/{session['username']}" + '/' + fi + "/" + filename):

            with open(UPLOAD_FOLDER + f"/{session['username']}" + '/' + fi + "/" + filename, 'w') as f:

                f.write("")

        return redirect(f"/{fi}")
        
    else:

        return render_template("newfile.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e)

@app.errorhandler(400)
def bad_requesthandler(e):
    return render_template('400.html', error=e)

@app.errorhandler(403)
def permissiondeniedhandler(e):
    return render_template('403.html', error=e)

@app.errorhandler(405)
def methodNotAllowedhandler(e):
    return render_template('405.html', error=e)

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

        user = request.form['username']

        if user in keys:

            if hashPassword(request.form['password'], user) == data.get(user):

                session['username'] = user

                return redirect(url_for('home'))
            
            else:

                return render_template('login.html', error = f"Incorrect password for {user}...")

        else:

            return render_template('login.html', error = f"Username {user} not found...")

    return render_template('login.html')

@app.route('/register/', methods=['POST', 'GET'])
def register():

    if request.method=='POST':

        data = db('logins.json')
        keys = data.keys()

        user = request.form['username']

        if not user in keys:

            data.set(user, hashPassword(request.form['password'], user))

            os.mkdir(UPLOAD_FOLDER + f"/{user}")

            return render_template('register.html', error = 'You Are now Registered As {}'.format(user))

        else:

            return render_template('register.html', error = 'The username "{}" is already in use.'.format(user))

    return render_template('register.html')

@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/restart/')
def restartServer():

    restart_program()

app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
