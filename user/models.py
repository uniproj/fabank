from django.db import models
from django.contrib.auth.models import User
from main_admin.models import account

class user_account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name=models.CharField(max_length=100)
	father_name=models.CharField(max_length=50)
	sex=models.CharField(max_length=50)
	cellphone_number=models.CharField(max_length=50)
	tellphone_number=models.CharField(max_length=50)
	address=models.TextField()
	nation_ID=models.IntegerField(default=111111111111)
	account_id=models.OneToOneField(account,blank=True)

