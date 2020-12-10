from subgraph_bot.db import engine, Base
from subgraph_bot.models import *
from sqlalchemy_utils.functions import database_exists, create_database


def init_db():

    db_url = engine.url
    if not database_exists(db_url):
        create_database(db_url)

    if not engine.table_names():
        Base.metadata.create_all()