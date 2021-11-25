from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mess(models.Model):
    name = models.CharField(max_length=100,blank = True, null=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Member(models.Model):
    mess = models.ForeignKey(Mess, null = True,blank=True ,on_delete=models.CASCADE)
    user = models.OneToOneField(User, null = True,blank=True ,on_delete=models.CASCADE)
    phone = models.DecimalField(decimal_places=15,max_digits=15,blank=True,null=True)
    profile_pic = models.ImageField(default="profile.png",null = True,blank = True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)

class Meals(models.Model):
    user = models.OneToOneField(User, null = True,blank=True ,on_delete=models.CASCADE)
    todays_meal = models.IntegerField(default=0,blank=True,null=True)
    total_meal = models.IntegerField(default=0,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)

class AmountSpend(models.Model):
    mess = models.ForeignKey(Mess, null = True,blank=True ,on_delete=models.CASCADE)
    user = models.OneToOneField(User, null = True,blank=True ,on_delete=models.CASCADE)
    spend_on = models.CharField(max_length= 250,blank=True,null=True)
    amount = models.IntegerField(default=0,blank=True,null=True)
    person_spend = models.FloatField(default=0,blank=True,null=True)
    spend_total = models.FloatField(default=0,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)

class Bills(models.Model):
    mess = models.ForeignKey(Mess, null = True,blank=True ,on_delete=models.CASCADE)
    bill_on = models.CharField(max_length= 250,blank=True,null=True)
    amount = models.IntegerField(default=0,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.mess)

class CashDeposit(models.Model):
    mess = models.ForeignKey(Mess, null = True,blank=True ,on_delete=models.CASCADE)
    user = models.OneToOneField(User, null = True,blank=True ,on_delete=models.CASCADE)
    deposit_for = models.CharField(max_length= 250,blank=True,null=True)
    amount = models.IntegerField(default=0,blank=True,null=True)
    balance = models.FloatField(default=0,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        print('Profile created')


def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.UserProfile.save()
        print('Profile Updated')