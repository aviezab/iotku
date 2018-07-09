from flask import Blueprint, request, session, jsonify, url_for
from .iotku_database import Iotku
from .natslib import NATS

name = 'api'
api = Blueprint(name, __name__)
iotku = Iotku()
c = NATS()

from . import core, user, device, sensor, rule
