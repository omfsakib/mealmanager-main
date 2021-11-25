from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Mess)
admin.site.register(Meals)
admin.site.register(Bills)
admin.site.register(CashDeposit)
admin.site.register(AmountSpend)
admin.site.register(Member)
admin.site.register(UserProfile)