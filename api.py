import datetime
import time

from sqlalchemy.orm import sessionmaker

from models import User, Record, engine

Session = sessionmaker(bind=engine)
session = Session()


def exception_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(e)
    return wrapper


def create_user(user_name):
    user_name = user_name.split(' ')[1:]
    user_name = ' '.join(user_name)
    try:
        user = User(name=' '.join(user_name))
    except Exception as e:
        print(e)
        return False
    session.add(user)
    session.commit()


@exception_catcher
def chose_user(user_name, users_list):
    if user_name.isdigit():
        user_name = users_list[int(user_name)][0]
    user = session.query(User).filter_by(name=user_name).first()
    return user.id


@exception_catcher
def change_user():
    users_list = [i.name for i in session.query(User).all()]
    print('chose one of them or create new:', ', '.join([i for i in users_list]),
          end='\n')  # username must not be digit

    user_name = str(input(':/'))
    if '-create' in user_name:
        _ = create_user(user_name)
        while not _:
            print('this name is already used, try another one')
            user_name = str(input(':/'))
            _ = create_user(user_name)

    user_id = chose_user(user_name, users_list)
    if not user_id:
        print('wrong name', end='\n')
        return change_user()
    print('Welcome back,', user_name)
    return user_id


@exception_catcher
def show_statistic(input_value, user_id):  # -statistic 21.10.2021 food
    values = input_value.split(' ')[1:]
    if len(values) > 0:

        timestamp = None
        object_name = None
        comparison = None

        for i in values:
            if i.split('.')[0].isdigit():
                comparison = '1.' * (3 - len(i.split('.')))
                date = comparison + i
                date_compare = i.split('.')
                if len(date_compare) != 3:  # ['6', '2020']
                    date_compare[0] = str(int(date_compare[0]) + 1)
                    date_compare = '1.' * (3 - len(i.split('.'))) + '.'.join(date_compare)
                    date_compare_timestamp = int(
                        time.mktime(datetime.datetime.strptime(date_compare, "%d.%m.%Y").timetuple()))
                timestamp = int(time.mktime(datetime.datetime.strptime(date, "%d.%m.%Y").timetuple()))
            else:
                object_name = i
        if timestamp is None:
            result = session.query(Record).filter_by(object_name=object_name, user_id=user_id)
        elif object_name is None:
            if comparison:
                result = session.query(Record).filter(Record.date > timestamp, Record.date < date_compare_timestamp,
                                                      Record.user_id == user_id)
            else:
                result = session.query(Record).filter(Record.date == timestamp, Record.user_id == user_id)
        else:
            if comparison:
                result = session.query(Record).filter(Record.date > timestamp, Record.date < date_compare_timestamp,
                                                      Record.user_id == user_id, Record.object_name == object_name)
            else:
                result = session.query(Record).filter(Record.date == timestamp, Record.user_id == user_id,
                                                      Record.object_name == object_name)
    else:
        result = session.query(Record).filter_by(user_id=user_id)
    for i in result.all():
        print(i, end='\n')
    if not result.all():
        print('no data')
    return result.all()


@exception_catcher
def get_today_stats(user_id):
    date = str(datetime.date.today())
    timestamp = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
    result = session.query(Record).filter_by(date=timestamp, user_id=user_id)

    for i in result.all():
        print(i, end='\n')
    if not result.all():
        print('no data')
    return result.all()


@exception_catcher
def delete_records(input_value, user_id):
    values = input_value.split(' ')[1:]
    print(values)
    if len(values) > 0:

        timestamp = None
        object_name = None

        for i in values:
            if '.' in i:
                timestamp = int(time.mktime(datetime.datetime.strptime(i, "%d.%m.%Y").timetuple()))
            else:
                object_name = i
        print(timestamp, object_name)
        if timestamp is None:
            session.query(Record).filter(Record.object_name == object_name, Record.user_id == user_id).delete()
        elif object_name is None:
            session.query(Record).filter(Record.date == timestamp, Record.user_id == user_id).delete()
        else:
            session.query(Record).filter(Record.object_name == object_name, Record.date == timestamp,
                                         Record.user_id == user_id).delete()

        print(f'deleted records about {values}')
    else:
        session.query(Record).filter(Record.user_id == user_id).delete()
        print('successfully deleted')
    session.commit()


@exception_catcher
def add_new_record(input_value, user_id):
    description = ''
    values = input_value.split(' ')
    date = str(datetime.date.today()).replace('-', '.')
    date = int(time.mktime(datetime.datetime.strptime(date, "%Y.%m.%d").timetuple()))
    if '.' in values[0]:
        date = int(time.mktime(datetime.datetime.strptime(values[0], "%d.%m.%Y").timetuple()))
        values = values[1:]
    object_name = values[0]
    value = values[2]  # есть ['-'] если записывать 12.12.2012 Еда - 250
    values = values[2:]
    values.pop(0)
    if values:
        description = ' '.join(values) if len(values) > 1 else values[0]
    record = Record(date=date, object_name=object_name, value=value, user_id=user_id, description=description)
    print('added', record)
    session.add(record)
    session.commit()

