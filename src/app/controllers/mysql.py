# -*- coding: utf-8 -*-HTTP_PATH
import pkg_resources, pathlib
from flask import Blueprint, render_template
from flask.json import jsonify
from flasgger import swag_from
from app.utils import get_openid_user

TEMPLATE = pkg_resources.resource_filename(__name__, '../views/templates/mysql.html.j2')

mysql_controllers = Blueprint('fakenames',
                                  __name__,
                                  template_folder=pathlib.Path(TEMPLATE).parent.as_posix())

import logging
logger = logging.getLogger(__name__)

from flask_restful import Resource

from app.models.mysql import Fakenames

class MySQLApis(Resource):
    @staticmethod
    @swag_from(pkg_resources.resource_filename(__name__, 'swagger/fakenames/GET.yaml'))
    @mysql_controllers.route('/apis/v1/fakenames', methods=['GET'])
    def get_all() -> list:
        """ Returns all fake identities """
        response = []
        
        for item in Fakenames.read_all():
            response.append(item.serialize)
        logger.debug(f'Response: {response}')
        return response
    
    @staticmethod
    @swag_from(pkg_resources.resource_filename(__name__, 'swagger/identity/GET.yaml'))
    @mysql_controllers.route('/apis/v1/fakenames/identity/<string:guid>', methods=['GET'])
    def get(guid) -> dict:
        """ Returns a fake identity based on its GUID """
        response = Fakenames.read(guid=guid)
        logger.debug(f'Response: {response}')
        return response.serialize

    @mysql_controllers.route('/mysql')
    def dashboard():
        return render_template(pathlib.Path(TEMPLATE).name, dash_url="/fakenames/")