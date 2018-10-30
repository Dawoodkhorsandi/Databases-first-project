import random
from projectOne.settings import (HOME_SUPPLIANT_URL,
                                 HOME_CLIENT_URL,
                                 BILL_URL,
                                 PAYMENT_URL,
                                 bill_ID)
from django.utils import timezone
from .templatetags.myfilters import datetime_persian


def delete_suppliant(national_code):
    with open(HOME_SUPPLIANT_URL, 'r') as file:
        lines = file.readlines()
    with open(HOME_SUPPLIANT_URL, 'w') as file:
        for line in lines:
            if str(national_code) not in line:
                file.write(line)
     
def edit_suppliant(national_code, edited_line):
    with open(HOME_SUPPLIANT_URL, 'r') as file:
        lines = file.readlines()

    with open(HOME_SUPPLIANT_URL, 'w') as file:
        for line in lines:
            if str(national_code) not in line:
                file.write(line)
            else:
                file.write(edited_line)
     
def interval(date1, date2):
    date1 = date1.strip()
    date2 = date2.strip()

    date1_list = date1.split(' ')
    date2_list = date2.split(' ')

    month = {
        'فرودین':1,
        'اردیبهشت':2,
        'خرداد':3,
        'تیر':4,
        'مرداد':5,
        'شهریور':6,
        'مهر':7,
        'آبان':8,
        'آذر':9,
        'دی':10,
        'بهمن':11,
        'اسفند':12
    }

    interval_min = 0

    if int(date1_list[2]) == int(date2_list[2]):
        if month[date1_list[1]] == month[date2_list[1]]:
            if int(date1_list[0]) == int(date2_list[0]):
                hour1 = date1_list[4].split(':')
                hour2 = date2_list[4].split(':')

                if int(hour1[0]) == int(hour2[0]):
                    interval_min = (int(hour2[1]) - int(hour1[1]))
                else:
                    interval_min = 60 * (int(hour2[0]) - int(hour1[0]))
                    interval_min += int(hour2[1]) - int(hour1[1])
                    
            else:
                hour1 = date1_list[4].split(':')
                hour2 = date2_list[4].split(':')
                if int(date1_list[0]) < int(date2_list[0]):
                    if (int(date2_list[0]) - int(date1_list[0])) == 1:
                        interval_min = 60 * ((int(hour2[0]) - 0) - (24 - int(hour1[0]))) 
                        interval_min += (int(hour2[1]) + int(hour1[1]))
                    else:
                        interval_min = ((int(date2_list[0]) - int(date1_list[0])) - 1) * 24 * 60
                        interval_min += 60 * ((int(hour2[0]) - 0) - (24 - int(hour1[0]))) 
                        interval_min += (int(hour2[1]) + int(hour1[1])) 
        

    return interval_min

def bill_id():
    with open(BILL_URL, 'r') as file:
        all_lines = file.readlines()

    while(True):
        repetative = False
        while(True):
            random_number = ''.join(random.sample('0123456789', 6))
            if int(random_number) > 10000:
                break
        for line in all_lines:
            if str(random_number) in line[4:11]:
                repetative = True
                break
        if not repetative:
            break
    return random_number


def deadline(date):
    date = date.split(' ')
    month = [
            'فرودین',
            'اردیبهشت',
            'خرداد',
            'تیر',
            'مرداد',
            'شهریور',
            'مهر',
            'آبان',
            'آذر',
            'دی',
            'بهمن',
            'اسفند'
          ]

    index = month.index(date[1])
    date[1] = month[index + 2]
    new = ' '.join(date)
    return new
    
def counting_bills():
    date = datetime_persian(timezone.now())
    with open(HOME_CLIENT_URL, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        ls = line.split(',')
        string = 'nothin' 
        with open(BILL_URL, 'r') as file:
            all_lines = file.readlines()
        for l in all_lines:
            if ls[0] in l[0:6]:
                string = l

        if string == 'nothin':
            new = ''
            my_list = [
                ls[0],
                str(bill_id()),
                datetime_persian(timezone.now()),
                datetime_persian(timezone.now()),
                str(0),
                str(0),
                deadline(datetime_persian(timezone.now())),
                'False'
                ]
            new = ','.join(my_list)
            new += '\n'
            with open(BILL_URL, 'a') as file:
                file.write(new)
        
        else:
            string = string.strip()
            string = string.split(',')
            if interval(string[3], datetime_persian(timezone.now())) >= 5:
       
                new = ''
                my_list = [
                    ls[0],
                    str(bill_id()),
                    string[3],
                    datetime_persian(timezone.now()),
                    string[5],
                    str(interval(string[3], datetime_persian(timezone.now())) + int(string[5])),
                    deadline(datetime_persian(timezone.now())),
                    'False'
                ]       
                new = ','.join(my_list)
                new += '\n'
                with open(BILL_URL, 'a') as file:
                    file.write(new)
             



def search(text):
    with open(HOME_SUPPLIANT_URL, 'r') as file:
        lines = file.readlines()    
    lines = [line.strip() for line in lines]
    my_list = []
    for line in lines:
        line = line.split(',')
        name = [line[0],
                line[1]]
        name = ' '.join(name)
        if text in  name:
            goal = line
          
            my_list.append({'code': 1,
                            'results': goal})

    with open(HOME_CLIENT_URL, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    
    for line in lines:
        line = line.split(',')
        name = [line[1],
                line[2]]
        name =' '.join(name)

        if text in name or text == line[0]:
            goal = line
            my_list.append({
                'code': 2,
                'results': goal
            })
    if len(my_list) == 0 :
        my_list.append({'code': 3,
        'results':'nothing'})
        
    return my_list