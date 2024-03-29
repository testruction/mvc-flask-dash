# -*- coding: utf-8 -*-
import pytest

import logging
logger = logging.getLogger(__name__)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
# logger.setLevel('DEBUG')

from project.models.postgres import Fakenames

@pytest.mark.usefixtures("app_ctx")
class TestModels:
    def test_read_all(app):
        response = Fakenames.read_all()
        logger.info(response)
        assert len(response) == 1000

    def test_read(app):
        response = Fakenames.read(guid='ee8d5509-dbce-4ae1-98c8-ba8e00ca8180')
        logger.info(response)
        assert response
