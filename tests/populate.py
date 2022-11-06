import sys
sys.path.append('.')
sys.path.append('./src/')

from dotenv import load_dotenv
load_dotenv()

import logging, pkg_resources, itertools, csv

from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DevelopmentConfig
from app.models.mysql import Fakenames, Base

logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger.setLevel('DEBUG')

logger.info(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

dataset = pkg_resources.resource_filename(__name__,
                                          'integration/fakenames.csv')

engine = create_engine(url=DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
                       echo=False,
                       future=True)
connection = engine.connect()
# begin the nested transaction
transaction = connection.begin()
# use the connection with the already started transaction
Base.metadata.bind = connection
Base.metadata.schema = 'public'
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def lower_first(iterator):
    return itertools.chain([next(iterator).lower()], iterator)


with Session.begin() as session:
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        for row in reader:
            data = Fakenames(**row)
            session.add(data)
