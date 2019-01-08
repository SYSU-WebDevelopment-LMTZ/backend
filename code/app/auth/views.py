from . import auth 
from .. import db


@auth.route('/', methods=['GET', 'POST'])
def index():
    return 'Auth OK'

