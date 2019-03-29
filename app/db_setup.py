# db_setup.py

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_INSTANCE=os.getenv('DB_INSTANCE')

DB_URL= "mysql+pymysql://%s:%s@%s:%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_INSTANCE)

#engine = create_engine('sqlite:///envreq.db', convert_unicode=True)
#engine = create_engine('mysql+pymysql://envreq:envreq@localhost:3306/envreqdb', convert_unicode=True)
engine = create_engine(DB_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False,bind=engine))

#def fk_pragma_on_connect(dbapi_con, con_record):
#    dbapi_con.execute('pragma foreign_keys=ON')

#event.listen(engine,'connect', fk_pragma_on_connect)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)