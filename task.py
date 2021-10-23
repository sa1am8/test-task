from api import *

# commands start with -

if __name__ == '__main__':
    print('---running---', end='\n')
    user_id = change_user()
    while True:
        input_value = str(input(':/'))

        if '-delete' in input_value:  # -delete food
            delete_records(input_value, user_id)

        elif '-statistic' in input_value:  # -statistic food 12.12.2020
            show_statistic(input_value, user_id)

        elif input_value == '-today':
            get_today_stats(user_id)

        elif input_value == '-change_user' or input_value == '-change user':
            change_user()

        elif input_value == 'exit()':
            exit()

        else:
            add_new_record(input_value, user_id)
