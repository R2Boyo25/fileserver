# import the Flask class from the flask module
from flask import *
from markupsafe import escape
import random
import os
from werkzeug.utils import secure_filename
import json
from math import *
from database import Database as db
from os import walk
from f2 import f2
