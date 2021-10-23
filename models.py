from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///main.db')


def create_table():
    metadata = MetaData()
    users_table = Table('users', metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
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


class User(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id

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
        return "%s | %s - %s, desc - '%s'" % (
        self.date, self.object_name, self.value, self.description)


tables = create_table()
mapper(User, tables[0])
mapper(Record, tables[1])
