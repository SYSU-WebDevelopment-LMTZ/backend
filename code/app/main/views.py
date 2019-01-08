from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return 'OK'

