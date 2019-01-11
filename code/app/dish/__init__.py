from flask import Blueprint

dish = Blueprint('dish', __name__)

from . import views

