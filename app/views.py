import random
from django.utils import timezone
from django.shortcuts import render, redirect
from .templatetags.myfilters import datetime_persian
from .forms import (BillForm,
                    HomeSuppliantForm,
                    HomeSuppliantEditForm,
                    HomeClientForm,
                    PaymentForm,
                    LoginForm,
                    AddressForm,
                    SearchForm)
from projectOne.settings import (HOME_CLIENT_URL,
                                 HOME_SUPPLIANT_URL,
                                 BILL_URL,
                                 PAYMENT_URL)
from .CLASSES import (HomeSuppliantClass,
                      HomeCliantClass,
                      BillsClass,
                      PaidClass
)
from .utils import (delete_suppliant,
                    edit_suppliant,
                    interval,
                    counting_bills,
                    search)

def index(request):
    form = SearchForm()
    result= None
    suppliant_list = []
    client_list = []
    boolean = None  
    if request.method == 'POST':
        form = SearchForm(request.POST)
        print('request is post ')
        if form.is_valid():
            text = form.cleaned_data['text']
            result = search(text)
            print('Fuckin form submitted ')
            print(result)
            for res in result:
                if res.get('code') == 1:
                    ob1 = HomeSuppliantClass()

                    ob1.first_name = res.get('results')[0]
                    ob1.last_name = res.get('results')[1]
                    ob1.national_code = res.get('results')[2]
                    ob1.postal_code = res.get('results')[3]
                    ob1.phone_number = res.get('results')[4]
                    ob1.units = res.get('results')[5]

                    suppliant_list.append(ob1)

                if res.get('code') == 2:
                    ob2 = HomeCliantClass()

                    ob2.subscription_number = res.get('results')[0]
                    ob2.first_name = res.get('results')[1]
                    ob2.last_name = res.get('results')[2]
                    ob2.national_code = res.get('results')[3]
                    ob2.address = res.get('results')[4]
                    ob2.phone_number = res.get('results')[5]
                    ob2.date = res.get('results')[6]
                    ob2.units = res.get('results')[7]

                    client_list.append(ob2)
    if result!= None:
        if len(result) > 0:
            boolean = True
    if len(client_list) != 0 or len(suppliant_list) != 0:
        boolean = False
   
    print('BOOLEAN EQUALS TO ' + str(boolean))
    print('clinent  = = = = ' + str(client_list))
    print('suppliant = = = = ' + str(suppliant_list))

    
    context = {'form': form,
                'results': result,
                'boolean': boolean,
                'clients': client_list,
                'suppliants': suppliant_list          
               }
    return render(request,
                  'app/index.html',
                  context)
    
def login(request):
    my_form = LoginForm()
    context ={
        'my_form': my_form,
    }
    return render(request, 'registration/login.html', context)
    
def sending_request(request):
    my_form = HomeSuppliantForm()
    if request.method == 'POST':
        my_form = HomeSuppliantForm(request.POST)
        if my_form.is_valid():
            first_name = my_form.cleaned_data['first_name']
            last_name = my_form.cleaned_data['last_name']
            national_code = my_form.cleaned_data['national_code']
            postal_code = my_form.cleaned_data['postal_code']
            phone_number = my_form.cleaned_data['phone_number']
            units = my_form.cleaned_data['units']

            entry_list = [first_name,
                         last_name,
                         str(national_code),
                         str(postal_code),
                         str(phone_number),
                         str(units)]
            new_entry = ','.join(entry_list)
            new_entry += '\n'

            with open(str(HOME_SUPPLIANT_URL), 'a') as file:
                file.write(new_entry)

            print(new_entry)
    return render(request,
                  'app/step1.html',
                  {'my_form': my_form})

def request_table(request):
    with open(str(HOME_SUPPLIANT_URL), 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        my_list = []
            
        for line in lines:
            string = line.split(',')
            
            new_object = HomeSuppliantClass()
            new_object.first_name = string[0]
            new_object.last_name = string[1]
            new_object.national_code = string[2]
            new_object.postal_code = string[3]
            new_object.phone_number = string[4]
            new_object.units = string[5]

            my_list.append(new_object)
            
    return render(request,
                  'app/request_table.html',
                   {'list': my_list})

def confirm_request_step1(request, national_code):
    with open(HOME_SUPPLIANT_URL, 'r') as file:
        all_lines = file.readlines()

    new_entry = 'NOT FUCKIN ASSIGNED'
    goal = 'this is goal line'
    
    for line in all_lines:
        if str(national_code) in line:
            goal = line
    
    if request.method == 'POST':
        my_form = AddressForm(request.POST)
        if my_form.is_valid():
            address = my_form.cleaned_data['address']
            while(True):
                repetative = False
                while(True):
                    random_number = ''.join(random.sample('0123456789', 5))
                    if int(random_number) > 10000:
                        break
                for line in all_lines:
                    if str(random_number) in line[0:6]:
                        repetative = True
                        break
                if not repetative:
                    break
            date = datetime_persian(timezone.now())
            delete_suppliant(national_code)
            goal = goal.strip()
            my_str = goal.split(',')
            new_list = [str(random_number),
                             my_str[0],
                             my_str[1],
                             my_str[2],
                             address,
                             date,
                             my_str[4],
                             my_str[5],
                    ]
            new_entry = ','.join(new_list)
            new_entry += '\n'
            with open(str(HOME_CLIENT_URL), 'a') as file:
                file.write(new_entry)            
        else:
            print('NOT VALID FORM')                       
        return redirect('app:confirmed_table')
    else:
        my_form = AddressForm()
    return render(request, 'app/confirm_step1.html', {'my_form': my_form}) 

def confirmed_table(request):
    with open(HOME_CLIENT_URL, 'r') as file:
        lines = file.readlines()
    
    lines = [line.strip() for line in lines]
    my_list = []

    for line in lines:
        string = line.split(',')
        new_object = HomeCliantClass()

        new_object.subscription_number = string[0]
        new_object.first_name = string[1]
        new_object.last_name = string[2]
        new_object.national_code = string[3]
        new_object.address = string[4]
        new_object.phone_number = string[5]
        new_object.date = string[6]
        new_object.units = string[7]

        my_list.append(new_object)    
    
    return render(request,
                  'app/confirmed_table.html',
                  {'list': my_list}
    )
        
def edit_request(request, national_code):
    with open(HOME_SUPPLIANT_URL, 'r') as file:
        lines = file.readlines()
    goal = ''
    for line in lines:
        if str(national_code) in line:
            goal = line
    goal = goal.strip()
    my_list = goal.split(',')

    line = HomeSuppliantClass()
    line.first_name = my_list[0]
    line.last_name = my_list[1]
    line.national_code = my_list[2]
    line.postal_code = my_list[3]
    line.phone_number = my_list[4]
    line.units = my_list[5]
   
    if request.method == 'POST':
        my_form = HomeSuppliantEditForm(request.POST)
        if my_form.is_valid():
            if len(my_form.cleaned_data['first_name']) >= 1:
                first_name = my_form.cleaned_data['first_name']
            else:
                first_name = line.first_name
      
            if my_form.cleaned_data['last_name']:
                last_name = my_form.cleaned_data['last_name']
            else:
                last_name = line.last_name

            if my_form.cleaned_data['national_code']:
                national_code = my_form.cleaned_data['national_code']
            else:
                national_code = line.national_code

            if my_form.cleaned_data['postal_code']:
                postal_code = my_form.cleaned_data['postal_code']
            else:
                postal_code = line.postal_code

            if my_form.cleaned_data['phone_number']:
                phone_number = my_form.cleaned_data['phone_number']
            else:
                phone_number = line.phone_number

            if my_form.cleaned_data['units']:
                units = my_form.cleaned_data['units']
            else:
                units = line.units


            entry_list = [first_name,
                         last_name,
                         str(national_code),
                         str(postal_code),
                         str(phone_number),
                         str(units)]
            new_entry = ','.join(entry_list)
            new_entry += '\n'

            edit_suppliant(national_code, new_entry)

        return redirect('app:request_table')
    else:
        my_form = HomeSuppliantEditForm()
    
    return render(request,
                  'app/step1_edit.html',
                  {'my_form': my_form,
                   'line': line})

def delete_request(request, national_code):
    with open(HOME_SUPPLIANT_URL, 'r') as file:
        lines = file.readlines()


    with open(HOME_SUPPLIANT_URL, 'w') as file:
        for line in lines:
            if str(national_code) not in line:
                file.write(line)  
    return redirect('app:request_table')

def all_bills(request):
    with open(BILL_URL, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    my_list = []
    for line in lines:
        ob = BillsClass()
        string = line.split(',')

        ob.subscription_number = string[0]    
        ob.bill_ID = string[1]
        ob.previous_date = string[2]
        ob.current_date = string[3]
        ob.previous_num = string[4]
        ob.current_num = string[5]
        ob.deadline = string[6]
        ob.paid = string[7]


        my_list.append(ob) 

    counting_bills()

    return render(request,
                  'app/all_bills.html',
                  {'list': my_list})

def bill(requset, subscription_number):
    with open(HOME_CLIENT_URL, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        line = line.split(',')
        if str(subscription_number) in line[0]:
            goal = line
    goal_ob = HomeCliantClass()
    
    goal_ob.subscription_number = goal[0]
    goal_ob.first_name = goal[1]
    goal_ob.last_name = goal[2]
    goal_ob.national_code = goal[3]
    goal_ob.address = goal[4]
    goal_ob.phone_number = goal[6]
    goal_ob.date = goal[5]
    goal_ob.units = goal[7]
    

    counting_bills()

    with open(BILL_URL , 'r') as file:
        lines = file.readlines()
  
    lines = [line.strip() for line in lines]
    my_list =[]

    for line in lines:
        string = line.split(',')
        if str(subscription_number) in string[0]:
            ob = BillsClass()

            ob.subscription_number = string[0]    
            ob.bill_ID = string[1]
            ob.previous_date = string[2]
            ob.current_date = string[3]
            ob.previous_num = string[4]
            ob.current_num = string[5]
            ob.deadline = string[6]
            ob.paid = string[7]

            my_list.append(ob) 
    pay_list = []
  
    with open(PAYMENT_URL, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    for line in lines:
        line = line.split(',')
        if str(subscription_number) == line[3]:
        
            pay_ob = PaidClass()
            pay_ob.bill_ID = line[0]
            pay_ob.fee = line[1]
            pay_ob.date = line[2]
            pay_ob.ID =subscription_number

            pay_list.append(pay_ob)
        
    
    ob = my_list[len(my_list) - 1]
    diff = int(ob.current_num) - int(ob.previous_num)
    # last_bill = pay_list[len(pay_list) - 1]
    num = len(pay_list)

    return render(requset,
                  'app/bill.html',
                  {'list': my_list,
                  'my_user': goal_ob,
                  'ob': ob,
                  'diff': diff,
                  'plist': pay_list,
                  
                  'num': num}
                  )

def pay(request, subscription_number, ID):
    with open(BILL_URL, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    for line in lines:
        string = line.split(',')
        if str(ID) in string[1]:
            goal = string
    
    if goal[7] == 'False':
        goal[7] = 'True'

    with open(BILL_URL, 'w') as file:
        for line in lines:
            if str(ID) not in line:
                
                line += '\n'
                file.write(line)
            else:
                line = ','.join(goal) 
                line += '\n'
                file.write(line) 
    interval = int(goal[5]) - int(goal[4])

    ob = PaidClass()

    ob.bill_ID = goal[1]
    ob.fee = str((interval * 500) + (interval * 0.05 * 500))
    ob.date = datetime_persian(timezone.now())
    ob.ID = subscription_number

    ooo = ','.join([ob.bill_ID, ob.fee , ob.date, ob.ID])
    ooo += '\n'

    with open(PAYMENT_URL, 'a') as file:
        file.write(ooo)

    return redirect('app:bill', subscription_number)

