# coding:utf-8

from flask import Blueprint

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')

from app.user import views
