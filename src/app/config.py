# -*- coding: utf-8 -*-

import os, argparse
# CLI arguments composition
parser = argparse.ArgumentParser()
parser.add_argument('--debug',
                    help='Enable debug logging',
                    action='store_true')
parser.add_argument('--trace-stdout',
                    help="Show OpenTelemetry output to console",
                    action="store_true")
parser.add_argument('--host',
                    type=str,
                    help='Hostname, fully qualified name or IP address',
                    default=os.environ.get('POSTGRES_HOST', default='localhost'))
parser.add_argument('--port',
                    type=str,
                    help='Listen port',
                    default=os.environ.get('POSTGRES_PORT', default=5432))
parser.add_argument('--username',
                    type=str,
                    help='Database user login name',
                    default=os.environ.get('POSTGRES_USER', default=None))
parser.add_argument('--password',
                    type=str,
                    help='Database user login password',
                    default=os.environ.get('POSTGRES_PASSWORD', default=None))
parser.add_argument('--database',
                    type=str,
                    help='Name of the database',
                    default=os.environ.get('POSTGRES_DB', default='fakenames'))
args, unknown = parser.parse_known_args()

# Initialize logging
from app.logging import init_logger
init_logger(args)
# Initialize telemetry
from app.telemetry import init_tracer
init_tracer(args)

from sqlalchemy.engine import URL

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_NABLED = True
    SITE_NAME = 'mvc-flask-dash'
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = URL.create(drivername = 'postgresql+psycopg2',
                                         username = args.username,
                                         password = args.password,
                                         host = args.host,
                                         port = args.port,
                                         database = args.database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True