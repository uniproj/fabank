from django.db import models
from django.contrib.auth.models import User


class account(models.Model):
	account_id=models.IntegerField(default=1111111111111111)
	account_id_shaba=models.IntegerField(default=111111111111)
	remain=models.IntegerField(default=100000)
	lock=models.BooleanField(default=False)

	def __str__(self):
		return str(self.account_id)

class bill(models.Model):
	name=models.CharField(max_length=100)
	account_id=models.ForeignKey(account,blank=True,null=True)

	def __str__(self):
		return self.name



class tarefe(models.Model):
	name=models.CharField(max_length=100)
	pay=models.IntegerField(default=0)

	def __str__(self):
		return self.name


class staff(models.Model):
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	father_name=models.CharField(max_length=50)
	nation_ID=models.IntegerField(default=111111111111)
	sex=models.CharField(max_length=8)
	cellphone_number=models.CharField(max_length=50)
	tellphone_number=models.CharField(max_length=50)
	address=models.TextField()
	employee_type=models.CharField(max_length=50)
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	branch_in=models.IntegerField(default=0,null=True)

	def __str__(self):
		return str(self.nation_ID) +" : " +self.employee_type


class branch(models.Model):
	name=models.CharField(max_length=50)
	state=models.CharField(max_length=50,default="tehran")
	city=models.CharField(max_length=50,default="tehran")
	location=models.TextField()
	account_id=models.ForeignKey(account,null=True)
	manager_id=models.ForeignKey(staff,null=True)
	sood=models.IntegerField(default=10,blank=True)

	def __str__(self):
		return self.name


class transaction(models.Model):
	t_type=models.CharField(max_length=200)
	t_branch=models.ForeignKey(branch,null=True)
	t_staff=models.ForeignKey(staff,null=True)
	t_account=models.ForeignKey(account,null=True)
	t_date=models.DateField(auto_now_add=True, blank=True,null=True)
	t_time=models.TimeField(auto_now_add=True, blank=True,null=True)
	t_message=models.TextField(max_length=400)
	t_money=models.IntegerField(default=0)

	def __str__(self):
		return self.t_type+" "+str(self.t_account.account_id)



class ATM(models.Model):
	bch=models.ForeignKey(branch,null=True)
	acc=models.ForeignKey(account,null=True)
	a_10000=models.IntegerField(default=0)
	a_20000=models.IntegerField(default=0)
	a_50000=models.IntegerField(default=0)
	a_100000=models.IntegerField(default=0)
	a_500000=models.IntegerField(default=0)

	def __str__(self):
		return str(self.id)
