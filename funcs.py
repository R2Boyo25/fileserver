from ipts import *

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'}
UPLOAD_FOLDER = r'/home/pi/files'

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
