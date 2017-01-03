from django.db import models


class account(models.Model):
	account_id=models.IntegerField(default=1111111111111111)
	account_id_shaba=models.IntegerField(default=111111111111)
	remain=models.IntegerField(default=100000)
	lock=models.BooleanField(default=False)


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


class branch(models.Model):
	name=models.CharField(max_length=50)
	state=models.CharField(max_length=50,default="tehran")
	city=models.CharField(max_length=50,default="tehran")
	location=models.TextField()
	account_id=models.ManyToManyField(account,blank=True)
	manager_id=models.ManyToManyField(staff,blank=True)

