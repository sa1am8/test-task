import datetime
import sqlite3
import time

# commands start with -
dbname = 'main.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
print('---running---')
cur.execute("""SELECT * FROM records""")

while True:
    input_value = str(input(':/'))

    if '-delete' in input_value:  # delete value='food'
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
                    """DELETE FROM records WHERE object_name='{condition}';""".format(condition=object_name))
            elif object_name is None:
                cur.execute(
                    """DELETE FROM records WHERE date='{condition}';""".format(condition=date))
            else:
                cur.execute(
                    """DELETE FROM records WHERE object_name='{object_name}' AND date='{date}';""".format(
                        object_name=object_name,
                        date=date))

            print(f'deleted records about {values}')
        else:
            cur.execute("""DELETE FROM records;""")
            print('successfully deleted')
        conn.commit()

    elif '-statistic' in input_value:  # -statistic food 12.12.2020
        values = input_value.split(' ')[1:]
        if len(values) > 0:

            date = None
            object_name = None

            for i in values:
                if '.' in i:
                    date = int(time.mktime(datetime.datetime.strptime(i, "%d.%m.%Y").timetuple()))
                else:
                    object_name = i
            if date is None:
                cur.execute(
                    """SELECT date, value FROM records WHERE object_name='{condition}'""".format(condition=object_name))
            elif object_name is None:
                cur.execute("""SELECT object_name ,value FROM records WHERE date='{date}'""".format(date=date))
            else:
                cur.execute(
                    """SELECT value FROM records WHERE object_name='{condition}' AND date='{date}'""".format(
                        condition=object_name, date=date))
        else:
            cur.execute("""SELECT * FROM records""")

        all_results = cur.fetchall()
        # datetime.fromtimestamp(timestamp)
        print(all_results)

    elif input_value == '-today':
        date = str(datetime.date.today())
        timestamp = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
        cur.execute(
            """SELECT date, object_name, value FROM records WHERE date={timestamp}""".format(timestamp=timestamp))

        all_results = cur.fetchall()
        print(all_results)

    elif input_value == 'exit()':
        exit()

    else:
        values = input_value.split(' ')
        date = str(datetime.date.today()).replace('-', '.')
        date = int(time.mktime(datetime.datetime.strptime(date, "%Y.%m.%d").timetuple()))
        if '.' in values[0]:
            date = int(time.mktime(datetime.datetime.strptime(values[0], "%d.%m.%Y").timetuple()))
            values = values[1:]
        object_name = values[0]
        value = values[2]  # есть ['-'] если записывать 12.12.2012 Еда - 250
        cur.execute(f"""INSERT INTO records(date, object_name, value) VALUES ({date}, '{object_name}', '{value}');""")
        conn.commit()
