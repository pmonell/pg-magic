from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

class ScopedSession(object):
    
    def __init__(self, bind=None):
        session_factory = sessionmaker(bind=bind)
        self.session = scoped_session(session_factory)
  
    def remove_session(self):
        self.session.remove()

class EngineManager(object):
    
    def __init__(self, CONNECTION, echo=False):
        self.engine = create_engine(CONNECTION, echo=echo)

class PgMagic(object):
    """Class used for accessing database tools for:
    
    -making tables
    -loading data
    -running queries
    -matching data files to tables
    -managing sessions
    -reflecting newly created tables
    """
    
    def __init__(self):
        engine = EngineManager(CONNECTION, echo=True)
        self.session = self._create_scoped_session(bind=engine.engine)
        self.engine = engine.engine
        self.metadata = MetaData(bind=self.engine)
        meta = MetaData()
        meta.reflect(bind=self.engine)
        self.reflection = meta

    def _create_scoped_session(self, bind=None):
        session = ScopedSession(bind=bind)
        return session
    
    def copy_from(self, file, table, sep=','):
        if self.session.dirty:
            self.session.remove_session()

        cursor = self.session.connection().connection.cursor()
        cursor.copy_from(file, table, sep=sep)
        self.session.commit()
        return 0
    
    def drop_table(self, table_name):
        if table_name not in self.reflection.tables:
            return "table not in database"
        table_to_drop = self.reflection.tables[table_name]
        table_to_drop.drop(self.engine)
