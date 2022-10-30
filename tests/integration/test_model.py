# -*- coding: utf-8 -*-
import logging
import typing
from flask_sqlalchemy import SQLAlchemy
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger.setLevel('DEBUG')

import pkg_resources
dataset = pkg_resources.resource_filename(__name__, 'fakenames.csv')

import pytest

from mvc_flask_dash.models.postgres import Fakenames, Base, db


@pytest.mark.usefixtures("app_ctx")
def test_model_populate(app) -> None:
    db = SQLAlchemy(app, model_class=Fakenames)
    db.create_all()
    import itertools
    def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    import csv
    from contextlib import closing
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        
        for row in reader:
            db.session.add(Fakenames(**row))
        db.session.commit()
  
@pytest.mark.usefixtures("app_ctx")          
def test_model_read_all(tables):
    response =  Fakenames.read_all()
    logger.info(response)
    assert len(response) == 1000

# def test_model_read(flask_app):
#     flask_app.app_context().push()
    
#     response = Fakenames.read(guid='ee8d5509-dbce-4ae1-98c8-ba8e00ca8180')
#     logger.info(response)
#     assert response