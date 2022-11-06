# -*- coding: utf-8 -*-
import pytest

import logging
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger.setLevel('DEBUG')

from project.models.postgres import Fakenames, db

@pytest.mark.usefixtures("app_ctx")
def test_read_all(app):
    response = Fakenames.read_all()
    # response = db.session.query(Fakenames).all()
    logger.info(response)
    assert len(response) == 1000


# @pytest.mark.usefixtures("app_ctx")
# def test_read(app, tables):
#     response = Fakenames.read(guid='ee8d5509-dbce-4ae1-98c8-ba8e00ca8180')
#     logger.info(response)
#     assert response
