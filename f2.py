from ipts import *
from funcs import *

f2 = Blueprint('simple_page', __name__, template_folder='templates')

@f2.route('/folder/<folder>/<fo2>', methods=['GET', 'POST'])
def folder2view(folder, fo2):

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
            file.save(os.path.join(UPLOAD_FOLDER + f"/{session['username']}" + '/' + folder + "/" + fo2, filename))
            return redirect('/fuploads/{}/{}/{}'.format(folder, fo2, filename))

        else:

            return redirect("/")

    else:

        links=[f'<!--This Page Was Auto Generated-->\n<div align=\"center\">\n<br><h1><b>{folder}</b></h1><br>\n<input type="text" id="mySearch" onkeyup="myFunction()" placeholder="Search.." title="Type in a category">\n<br><ul id="myMenu">']

        f, fo = getFiles(UPLOAD_FOLDER + f"/{session['username']}" + "/" + folder + "/" + fo2)

        for thing in f:
            links.append(iTemplate.format(f'/fuploads/{folder}/{fo2}'+thing, thing,f'/fuploads/{folder}/{fo2}/'+thing+"/download", f'/fuploads/{folder}/{fo2}/'+thing+"/delete"))

        links.append("\n  <li><a href='/'><i class='fa fa-arrow-left'></i><b> Main Folder</b></a></li>")

        links.append('</ul></div>')

        if 'username' in session:

            return render_template('sitemap.html', links=''.join(links), logged='Logged in as {}'.format(escape(session['username'])), username=escape(session['username']), loggedin=True)

        else:

            return render_template('sitemap.html', links=''.join(links), logged='You are not logged in')
