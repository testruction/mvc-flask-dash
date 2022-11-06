# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def get_migrate(app):
    return Migrate(app, db)


def create_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


def init_db(app):
    db.init_app(app)
