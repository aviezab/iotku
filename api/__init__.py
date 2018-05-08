from flask import Blueprint, request, session, jsonify, url_for
from .iotku_database import Iotku

name = 'api'
api = Blueprint(name, __name__)

from . import core, user, device, sensor, rule
