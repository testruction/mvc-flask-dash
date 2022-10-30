# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import pkg_resources
dataset = pkg_resources.resource_filename(__name__, 'fakenames.csv')

from mvc_flask_dash.controllers.postgres import PostgresApis
           
def test_controller_get_all(app):
    app.app_context().push()

    response =  PostgresApis.get_all()
    logger.debug(response)
    assert len(response) == 1000

def test_controller_get(app):
    app.app_context().push()
    
    response = PostgresApis.get(guid='ee8d5509-dbce-4ae1-98c8-ba8e00ca8180')
    logger.info(response)
    assert isinstance(response, dict)
