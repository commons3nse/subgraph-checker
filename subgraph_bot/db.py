import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(f"postgres://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_SERVICE_NAME']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}",
                       pool_size=int(os.environ['DATABASE_CONNECTION_COUNT']),
                       max_overflow=int(os.environ['DATABASE_OVERFLOW_COUNT']),
                       echo=False)
Base = declarative_base(bind=engine)


def get_session():
    """Get a new db session."""
    session = scoped_session(sessionmaker(bind=engine))
    return session
