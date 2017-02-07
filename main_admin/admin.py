from django.contrib import admin
from .models import account,staff,branch,transaction,bill,tarefe,ATM

admin.site.register(account)
admin.site.register(staff)
admin.site.register(branch)
admin.site.register(transaction)
admin.site.register(bill)
admin.site.register(tarefe)

admin.site.register(ATM)

