# -*- coding: utf-8 -*-HTTP_PATH
import pkg_resources, pathlib
from flask import Blueprint, render_template
from flask.json import jsonify
from flasgger import swag_from
from project.utils import get_openid_user

TEMPLATE = pkg_resources.resource_filename(__name__, '../views/templates/postgres.html.j2')

postgres_controllers = Blueprint('fakenames',
                                  __name__,
                                  template_folder=pathlib.Path(TEMPLATE).parent.as_posix())

import logging
logger = logging.getLogger(__name__)

from flask_restful import Resource

from project.models.postgres import Fakenames

class PostgresApis(Resource):
    @staticmethod
    @swag_from(pkg_resources.resource_filename(__name__, 'swagger/fakenames/GET.yaml'))
    @postgres_controllers.route('/apis/v1/fakenames', methods=['GET'])
    def get_all() -> list:
        """ Returns all fake identities """
        response = []
        
        for item in Fakenames.read_all():
            response.append(item.serialize)
        logger.debug(f'Response: {response}')
        return jsonify(response)
    
    @staticmethod
    @swag_from(pkg_resources.resource_filename(__name__, 'swagger/identity/GET.yaml'))
    @postgres_controllers.route('/apis/v1/fakenames/identity/<string:guid>', methods=['GET'])
    def get(guid) -> dict:
        """ Returns a fake identity based on its GUID """
        response = Fakenames.read(guid=guid)
        logger.debug(f'Response: {response}')
        return jsonify(response.serialize)

    @postgres_controllers.route('/postgres')
    def dashboard():
        return render_template(pathlib.Path(TEMPLATE).name, dash_url="/fakenames/")