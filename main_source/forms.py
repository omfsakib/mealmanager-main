from django.forms import ModelForm, fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields =['email','first_name','last_name','password']

class CreateMessForm(ModelForm):

    class Meta:
        model = Mess
        fields = "name",

class AddMealForm(ModelForm):

    class Meta:
        model = Meals
        fields = "todays_meal",

class AmountSpendForm(ModelForm):
    
    class Meta:
        model = AmountSpend
        fields = ['spend_on','amount']

class BillsForm(ModelForm):

    class Meta:
        model = Bills
        fields = ['bill_on','amount']

class CashDepositForm(ModelForm):

    class Meta:
        model = CashDeposit
        fields = ['deposit_for','amount']