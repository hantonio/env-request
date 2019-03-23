# db_setup.py

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///envreq.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False,bind=engine))

def fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

event.listen(engine,'connect', fk_pragma_on_connect)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)