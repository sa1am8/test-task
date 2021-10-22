import datetime
import sqlite3
import time

# commands start with -

db_name = 'main.db'
conn = sqlite3.connect(db_name)
cur = conn.cursor()
user_id = 1


def exception_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print('error, try again')

    return wrapper


def create_user(user_name):
    user_name = user_name.split(' ')[1:]
    user_name = ' '.join(user_name)
    cur.execute("""SELECT * FROM users WHERE name='{name}';""".format(name=user_name))
    if cur.fetchall():
        print("This name is already used, please try again")
        return False
    cur.execute(f"""INSERT INTO users (name) VALUES ('{user_name}')""".format(user_name=user_name))
    conn.commit()


@exception_catcher
def chose_user(user_name, users_list):
    if user_name.isdigit():
        user_name = users_list[int(user_name)][0]

    cur.execute("""SELECT id FROM users WHERE name='{name}';""".format(name=user_name))
    user_id = cur.fetchone()[0]
    return user_id


@exception_catcher
def show_statistic(input_value):
    values = input_value.split(' ')[1:]
    if len(values) > 0:

        timestamp = None
        object_name = None
        comparison = 0
        double_compare = ''

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
                    double_compare = "AND date<{}".format(date_compare_timestamp)
                timestamp = int(time.mktime(datetime.datetime.strptime(date, "%d.%m.%Y").timetuple()))
            else:
                object_name = i
        if timestamp is None:
            cur.execute(
                """SELECT date, value, description FROM records WHERE object_name='{condition}' AND user_id={user_id}""".format(
                    condition=object_name, user_id=user_id))
        elif object_name is None:
            sign = ">" if comparison else "="
            cur.execute(
                """SELECT object_name ,value, description FROM records WHERE date{sign}'{date}' {double_compare} AND user_id={user_id};""".format(
                    date=timestamp, sign=sign, double_compare=double_compare, user_id=user_id))
        else:
            sign = ">" if comparison else "="
            cur.execute(
                """SELECT value, description FROM records WHERE object_name='{condition}' AND date{sign}'{date}' AND user_id={user_id}""".format(
                    condition=object_name, sign=sign, date=timestamp, user_id=user_id))
    else:
        cur.execute(f"""SELECT * FROM records WHERE user_id={user_id}""")

    all_results = cur.fetchall()
    # datetime.fromtimestamp(timestamp)
    print(all_results)
    return all_results


@exception_catcher
def get_today_stats():
    date = str(datetime.date.today())
    timestamp = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
    cur.execute(
        """SELECT date, object_name, value, description FROM records WHERE date={timestamp} AND user_id={user_id}""".format(
            timestamp=timestamp, user_id=user_id))

    all_results = cur.fetchall()
    print(all_results)
    return all_results


@exception_catcher
def delete_records(input_value):
    values = input_value.split(' ')[1:]
    print(values)
    if len(values) > 0:

        date = None
        object_name = None

        for i in values:
            if '.' in i:
                date = int(time.mktime(datetime.datetime.strptime(i, "%d.%m.%Y").timetuple()))
            else:
                object_name = i
        print(date, object_name)
        if date is None:
            cur.execute(
                """DELETE FROM records WHERE object_name='{condition}' AND user_id={user_id}};""".format(
                    condition=object_name, user_id=user_id))
        elif object_name is None:
            cur.execute(
                """DELETE FROM records WHERE date='{condition}' AND user_id={user_id};""".format(condition=date,
                                                                                                 user_id=user_id))
        else:
            cur.execute(
                """DELETE FROM records WHERE object_name='{object_name}' AND date='{date}' AND user_id={user_id};""".format(
                    object_name=object_name,
                    date=date, user_id=user_id))

        print(f'deleted records about {values}')
    else:
        cur.execute(f"""DELETE FROM records WHERE user_id={user_id};""")
        print('successfully deleted')
    conn.commit()


@exception_catcher
def add_new_record(input_value):
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
    description = ' '.join(values) if len(values) > 1 else values[0]
    cur.execute(
        f"""INSERT INTO records(date, object_name, value, user_id, description) VALUES ({date}, '{object_name}', '{value}', {user_id}, '{description}');""")
    conn.commit()


if __name__ == '__main__':
    print('---running---', end='\n')
    cur.execute("""SELECT name FROM users""")
    users_list = cur.fetchall()
    print('chose one of them or create new:', ', '.join([i[0] for i in users_list]),
          end='\n')  # username must not be digit
    user_name = str(input(':/'))
    if '-create' in user_name:
        _ = create_user(user_name)
        while not _:
            print('this name is already used, try another one')
            user_name = str(input(':/'))
            _ = create_user(user_name)

    chose_user(user_name, users_list)
    print('Welcome back,', user_name)

    while True:

        input_value = str(input(':/'))

        if '-delete' in input_value:  # -delete food
            delete_records(input_value)

        elif '-statistic' in input_value:  # -statistic food 12.12.2020
            show_statistic(input_value)

        elif input_value == '-today':
            get_today_stats()

        elif input_value == '-change_user' or input_value == '-change user':
            cur.execute("""SELECT name FROM users""")
            users_list = cur.fetchall()
            print('chose one of them or create new: ', users_list, end='\n')  # username must not be digit
            user_name = str(input(':/'))

            if '-create' in user_name:
                create_user(user_name)
                _ = create_user(user_name)
                while not _:
                    print('this name is already used, try another one')
                    user_name = str(input(':/'))
                    create_user(user_name)

            chose_user(user_name, users_list)

        elif input_value == 'exit()':
            exit()

        else:
            add_new_record(input_value)
