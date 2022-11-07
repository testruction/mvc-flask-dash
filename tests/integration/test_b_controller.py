# -*- coding: utf-8 -*-
import pytest
import json

from project.controllers.postgres import PostgresApis

import logging
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("app_ctx")
class TestControllers:
    def test_api_get_all(app):
        response =  PostgresApis.get_all()
        d = json.loads(response.data)
        assert len(d) == 1000
        assert response.status_code == 200

    def test_api_get(app):
        response = PostgresApis.get(guid='ee8d5509-dbce-4ae1-98c8-ba8e00ca8180')
        d = json.loads(response.data)
        assert len(d) == 45
        assert response.status_code == 200
