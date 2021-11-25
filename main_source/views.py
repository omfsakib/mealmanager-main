from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
from .forms import *
from .models import *
import datetime
from datetime import date
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django_pandas.io import read_frame
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticted_user, allowed_users

# Create your views here.
@login_required(login_url='login')
def home(request):
    now = datetime.datetime.now()
    year = date.today().year
    month = date.today().month
    member = request.user.member
    if request.user.groups.filter(name = 'member').exists() or request.user.groups.filter(name = 'manager').exists():
        form1 = AddMealForm()
        form2 = AmountSpendForm()
        form3 = BillsForm()
        form4 = CashDepositForm()
        mess_id = member.mess.id
        mess = Mess.objects.get(id=mess_id)
        users = mess.members.all()
        total_user = users.count()
        total_meals = 0
        for l in users:
            total_meals += l.meals.total_meal
        spend = AmountSpend.objects.filter(mess=mess,date_created__month__gte=month)
        bill = Bills.objects.filter(mess=mess)
        cashdeposit = CashDeposit.objects.filter(mess=mess,date_created__month__gte=month)
        total_deposit = 0
        for k in cashdeposit:
            total_deposit += k.amount
        total_bill = 0
        for j in bill:
            total_bill += j.amount
        total_spend = 0
        for i in spend:
            total_spend += i.amount
        if total_spend > 0:
            meal_rate = 0
            meal_rate = float(total_spend/total_meals)
        else:
            meal_rate = 0
        for m in users:
            person_spend = 0
            person_spend += float(m.meals.total_meal*meal_rate)
            m.amountspend.spend_total = float(person_spend+(total_bill/total_user))
            m.amountspend.person_spend = person_spend
            m.cashdeposit.balance = float(m.cashdeposit.amount-m.amountspend.spend_total)
            m.amountspend.save()
            m.cashdeposit.save()
        main_balance = 0
        main_balance = total_deposit - (total_bill+total_spend)
        
        
        if request.method == 'POST' and 'todays_meal' in request.POST:
            form1 = AddMealForm(request.POST)
            
            if form1.is_valid():
                user_id = request.POST.get('user_id')
                todays_meal = request.POST.get('todays_meal')
                meal = Meals.objects.get(user_id=user_id)
                meal.todays_meal = todays_meal
                total = meal.total_meal
                total += int(todays_meal)
                meal.total_meal = total
                meal.save()
                return redirect('/')
        else:
            form1 = AddMealForm(request.POST)

        if request.method == 'POST' and 'spend_on' in request.POST:
            form2 = AmountSpendForm(request.POST)

            if form2.is_valid():
                user_id = request.POST.get('user_id')
                amount = request.POST.get('amount')
                spend_on = request.POST.get('spend_on')
                user = User.objects.get(id=user_id)
                amountspend = AmountSpend.objects.get(mess=mess,user_id=user_id)
                spend_amount = amountspend.amount
                spend_amount += int(amount)
                amountspend.amount = spend_amount
                amountspend.spend_on = spend_on
                amountspend.save()
                return redirect('/')
        else:
            form2 = AmountSpendForm(request.POST)
        
        if request.method == 'POST' and 'bill_on' in request.POST:
            form3 = BillsForm(request.POST)

            if form3.is_valid():
                bill_on = request.POST.get('bill_on')
                amount = request.POST.get('amount')
                bills = Bills.objects.create(mess=mess)
                bills.bill_on = bill_on
                bills.amount = amount
                bills.save()
                return redirect('/')
        else:
            form3 = BillsForm(request.POST)
        
        if request.method == 'POST' and 'deposit_for' in request.POST:
            form4 = CashDepositForm(request.POST)

            if form4.is_valid():
                user_id = request.POST.get('user_id')
                amount = request.POST.get('amount')
                deposit_for = request.POST.get('deposit_for')
                cashdeposit = CashDeposit.objects.get(mess=mess,user_id=user_id)
                deposit_amount = cashdeposit.amount
                deposit_amount += int(amount)
                cashdeposit.amount = deposit_amount
                cashdeposit.deposit_for = deposit_for
                cashdeposit.save()
                return redirect('/')
        else:
            form4 = CashDepositForm(request.POST)

        context ={
        'now':now,
        'member':member,
        'total_meals':total_meals,
        'form1':form1,
        'form2':form2,
        'form3':form3,
        'form4':form4,
        'main_balance':main_balance,
        'meal_rate':meal_rate,
        'total_deposit':total_deposit,
        'bill':bill,
        'total_bill':total_bill,
        'total_spend':total_spend,
        'mess':mess,
    }
        return render(request,'section/home.html',context)

    else:
        context = {'now':now,
        'member':member}

    return render(request,'section/home.html',context)

@unauthenticted_user
def registerPage(request):
    form = CreateUserForm()
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    role = request.POST.get('role')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            elif User.objects.filter(email=email).first():
                messages.success(request, 'This Email is taken.')
                return redirect('/register')

            if form.is_valid():
                user_obj = User.objects.create(username =username,email=email)
                user_obj.set_password(password)
                user_obj.save()
                auth_token=str(uuid.uuid4())
                profile_obj = UserProfile.objects.create(user = user_obj,auth_token=auth_token)
                profile_obj.save()
                meal = Meals.objects.create(user=user_obj)
                meal.save()
                if role == "member":
                    group = Group.objects.get(name = 'member')
                    user_obj.groups.add(group)
                elif role == "manager":
                    group = Group.objects.get(name = 'manager')
                    user_obj.groups.add(group)
                Member.objects.create(
                    user = user_obj
                )
                send_mail_after_registration(email,auth_token)
                messages.success(request,'Account was created for ' + username)
                return redirect('/token')
        
        except Exception as e:
            print(e)

    context = {'form':form}
    return render(request,'accounts/signup.html',context)

def success(request):
    return render(request, 'accounts/success.html')

def token_send(request):
    return render(request, 'accounts/token_send.html')

def send_mail_after_registration(email,token):
    subject = 'Account activation for Meal Manager...'
    message = f'Hello there! Click this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_form,recipient_list)

def verify(request,auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'accounts/error.html')

@unauthenticted_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            if user.member.mess is not None:
                return redirect('home')
            else:
                if request.user.groups.filter(name = 'member').exists():
                    return redirect('join_mess')
                else: 
                    return redirect('create_mess')

        else:
            messages.info(request,'Username or Password is incorrect')
    context = {}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def joinMess(request):
    mess = Mess.objects.all()
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        mess_id = request.POST.get('mess_id')
        mess = Mess.objects.get(id=mess_id)
        user = User.objects.get(id=user_id)
        amountspend = AmountSpend.objects.create(mess=mess,user=user)
        amountspend.save()
        cashdeposit = CashDeposit.objects.create(mess=mess,user=user)
        cashdeposit.save()
        member = Member.objects.get(user=user)
        member.mess = mess
        member.save()
        mess.members.add(user)
        mess.save()
        return redirect('/')
        messages.info(request,'Joining Mess Successful...')

    context={'mess':mess}
    return render(request, 'accounts/joinmess.html',context)

@login_required(login_url='login')
def createMess(request):
    form = CreateMessForm()
    if request.method == "POST" and 'name' in request.POST:
        form = CreateMessForm(request.POST)
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        name = request.POST.get('name')
        if form.is_valid():
            mess_obj = Mess.objects.create(name=name)
            mess_obj.members.add(user)
            mess_obj.save()
            amountspend = AmountSpend.objects.create(mess=mess_obj,user=user)
            amountspend.save()
            cashdeposit = CashDeposit.objects.create(mess=mess_obj,user=user)
            cashdeposit.save()
            member = Member.objects.get(user=user)
            member.mess = mess_obj
            member.save()
            return redirect('/')

    context={"form":form}
    return render(request,'accounts/createmess.html',context)