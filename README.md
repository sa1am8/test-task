# Installation

```bash
git clone https://github.com/sa1am8/test-task.git
pip install -r requirements.txt
```

##Usage:
```
python run.py 
```
all commands starts with "-", like how "-create Username"

commands:

* -today | shows statistics for today
* -statistic par1 par2 |  Shows records. par1, par2 - optional parameters.
One of them can be a date, 
the second one must be object_name. Date may be d.m.Y or m.Y(Y) then shows records 
by mentioned date or month(year). Shows all records if none of them designated.
* -delete par1 par2 | similarly to -statistic par1 par2. Removes records.
One of them can be a date, 
the second one must be object_name. Date may be d.m.Y or m.Y(Y) then removes records 
by mentioned date or month(year). Removes all records of this user.
* -today | shows today`s records
* -exit or exit() | stops the program
* -change user or -change_user | Transit to chose user stage
* param0 param1 - param2 param3 | creates new record, where
  * param0 - optional parameter | date of record. Default - today`s date
  * param1 - required parameter | object name
  * param2 - required parameter | numerical value
  * param3 - optional parameter | description, mark, note
  
Example of usage:
```bash
C:\Users\Toshka\PycharmProjects\test-task>python run.py

chose one of them or create new: Anton, Toshka, Ilya, test, Petya Ivanov
:/Anton
Welcome back, Anton
:/food - 100 tasty hamburger
added 2021-10-24 | food - 100, with description - 'tasty hamburger'
:/23.10.2021 food - 50 coca-cola
added 2021-10-23 | food - 50, with description - 'coca-cola'
:/15.09.2021 clothes - 1000 beautiful jacket
added 2021-09-15 | clothes - 1000, with description - 'beautiful jacket'
:/24.10.2020 laptop - 10000
added 2020-10-24 | laptop - 10000, with description - ''
:/-today
2021-10-24 | food - 1000, with description - ''
2021-10-24 | food - 100, with description - 'tasty hamburger'
:/-statistic
2021-10-24 | food - 100, with description - 'tasty hamburger'
2021-10-23 | food - 50, with description - 'coca-cola'
2021-09-15 | clothes - 1000, with description - 'beautiful jacket'
2020-10-24 | laptop - 10000, with description - ''
:/-statistic 2021
2021-10-24 | food - 100, with description - 'tasty hamburger'
2021-10-23 | food - 50, with description - 'coca-cola'
2021-09-15 | clothes - 1000, with description - 'beautiful jacket'
:/-statistic 2020
2020-10-24 | laptop - 10000, with description - ''
:/-statistic food
2021-10-24 | food - 100, with description - 'tasty hamburger'
2021-10-23 | food - 50, with description - 'coca-cola'
:/-statistic food 24.10.2021
2021-10-24 | food - 100, with description - 'tasty hamburger'
:/-delete food 24.10.2021
deleted records about ['food', '24.10.2021'] if they were
:/-statistic food 24.10.2021
no data
:/-delete food
deleted records about ['food'] if they were
:/-statistic food
no data
:/-delete
all successfully deleted
:/-statistic
no data
:/-change user
chose one of them or create new: Anton, Toshka, Ilya, test, Petya Ivanov
:/Ilya
Welcome back, Ilya
:/-statistic
2021-10-24 | food - 100, with description - ''
2021-10-22 | food - 5, with description - ''
:/-change_user
chose one of them or create new: Anton, Toshka, Ilya, test, Petya Ivanov
:/-create Julia
Welcome back, Julia
:/exit()
```