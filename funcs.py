from ipts import *
from hashlib import md5
import time
import platform

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

def hashPassword(password, username):
    h = platform.uname()[1] 

    return md5((password + username.lower()+h).encode()).hexdigest()
 
def convertToHashes():

    data = db('logins.json')

    for i in data.keys():

        uhashed = data.get(i)

        hashed = hashPassword(uhashed, i)

        data.set(i, hashed)
 
    with open("./USINGHASHES", "w") as f:
        f.write("DON'T DELETE THIS FILE OR YOUR PASSWORDS WILL BREAK!!!")

if not os.path.exists("./USINGHASHES"):

    print("USINGHASHES file not found, converting existing passwords to hashes. (if passwords are already hashed this will break them!)")

    print("Waiting 30 seconds, kill program to cancel!")

    time.sleep(30)

    convertToHashes()

    print("Done hashing passwords, program now starting.")





