from ipts import *

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'}
UPLOAD_FOLDER = r'/home/pi/files'
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tif', 'tiff'}
LIMIT_EXTENSIONS = False

def allowed_file(filename):
    
    if LIMIT_EXTENSIONS:
        
        return filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

    else:
    
        return "." in filename

def getFiles(UPLOAD_FOLDER):
    f = []
    fo = []
    for (dirpath, dirnames, filenames) in walk(UPLOAD_FOLDER):
        f.extend(filenames)
        fo.extend(dirnames)
        break

    return f, fo

def restart_program():

    python = sys.executable

    os.execl(python, python, *sys.argv)

def getExt(filename):

    ext = filename.split('.')[-1]

    return ext.lower()

def isImage(filename):

    if getExt(filename) in IMAGE_EXTENSIONS:

        return True
    
    else:

        return False