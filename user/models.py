from django.db import models
from django.contrib.auth.models import User
from main_admin.models import account

class user_account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name=models.CharField(max_length=100)
	father_name=models.CharField(max_length=50)
	sex=models.CharField(max_length=50)
	cellphone_number=models.CharField(max_length=50)
	tellphone_number=models.CharField(max_length=50)
	address=models.TextField()
	nation_ID=models.IntegerField(default=111111111111)
	account_id=models.ForeignKey(account,blank=True)
	is_active=models.BooleanField(default=False)

	def __str__(self):
		return str(self.nation_ID)


class check(models.Model):
	user=models.ForeignKey(user_account,blank=True,null=True)
	user_acc=models.ForeignKey(account,blank=True)
	pay=models.IntegerField(null=True)
	dar_vajh=models.CharField(max_length=200,null=True)
	is_used=models.BooleanField(default=False)

	def __str__(self):
		return str(self.user_acc.account_id)


class vam(models.Model):
	user=models.ForeignKey(user_account,null=True)
	money=models.IntegerField(default=0)
	monthes=models.IntegerField(default=0)
	payed=models.IntegerField(default=0)
	payback=models.IntegerField(default=0)
	is_confirmed=models.BooleanField(default=False)

	def __str__(self):
		return self.user.name +"  "+ str(self.money)