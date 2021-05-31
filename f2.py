from ipts import *
from funcs import *

f2 = Blueprint('simple_page', __name__, template_folder='templates')

@f2.route("/source/<filename>/")
def returnSourceData(filename):
    return send_from_directory('./source',
                            filename)