from datetime import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from sqlalchemy_utils import database_exists, create_database

engine = create_engine('sqlite:///main.db')
if not database_exists(engine.url):
    create_database(engine.url)


def create_table():
    metadata = MetaData()
    users_table = Table('User', metadata,
                        Column('id', Integer, autoincrement=True, unique=True, primary_key=True, nullable=False),
                        Column('name', String, unique=True),
                        )
    records_table = Table('records', metadata,
                          Column('id', Integer, primary_key=True, unique=True, nullable=False, autoincrement=True),
                          Column('user_id', Integer, nullable=False),
                          Column('value', Integer),
                          Column('object_name', String),
                          Column('date', String),
                          Column('description', String),
                          )

    metadata.create_all(engine)
    return users_table, records_table


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    name = Column('name', String, unique=True)

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.id)


class Record(object):
    def __init__(self, user_id, value, object_name, date, description):
        self.user_id = user_id
        self.value = value
        self.object_name = object_name
        self.date = date
        self.description = description

    def __repr__(self):
        return "%s | %s - %s, with description - '%s'" % (
            datetime.fromtimestamp(int(self.date)).date(), self.object_name, self.value, self.description)


tables = create_table()
# mapper(User, tables[0])
mapper(Record, tables[1])
