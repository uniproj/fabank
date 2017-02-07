from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core import serializers
from django.http import JsonResponse
from main_admin.models import account
from .models import user_account


def is_login2(request):
    if request.method=="GET" and request.user is not None:
        if request.user.is_authenticated:
            return HttpResponse(json.dumps({'response': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False}), content_type='application/json')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse(json.dumps({'response': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False}), content_type='application/json')


def change_pw(request):
    if request.method=="POST":
        if request.POST.get('password1')==request.POST.get('password2'):
            us=request.user
            us.set_password(request.POST.get('password1'))
            us.save()
            return HttpResponse(json.dumps({'response': True}), content_type='application/json')
            return render(request,"user/index.html",{})
        else:
            return HttpResponse(json.dumps({'response': False}), content_type='application/json')
            return render(request,"user/index.html",{})
    return HttpResponse(json.dumps({'response': False}), content_type='application/json')
    return render(request,"user/index.html",{})


def login_user(request):
    if request.method == "POST":
        users=User.objects.filter(username=request.POST.get("username"))
        if(len(users)>0):
            user=users[0]
            user2 = authenticate(username=user.username, password=request.POST.get("password"))
            if user2 is not None:
                if user2.is_active:
                    login(request,user2)
                    return HttpResponse(json.dumps({'response': True}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"response": False}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False}), content_type='application/json')


def users_transport(request):
    if request.method=="POST" and request.user is not None and request.user.is_authenticated:
        number1=int(request.POST.get("number1"));
        number2=int(request.POST.get("number2"));
        password=request.POST.get("password");
        money=int(request.POST.get("money"));
        us_acc1=account.objects.filter(account_id=number1)
        us_acc2=account.objects.filter(account_id=number2)
        if len(us_acc1)>0:
            acc1=us_acc1[0]
            if len(us_acc2)>0:
                acc2=us_acc2[0]
                user1=user_account.objects.filter(account_id=acc1)[0]
                user2=user_account.objects.filter(account_id=acc2)[0]
                if user1.user==request.user:
                    if money<acc1.remain:
                        acc1.remain=acc1.remain-money
                        acc2.remain=acc2.remain+money
                        acc1.save()
                        acc2.save()
                        return HttpResponse(json.dumps({'response': True,'message':"مبلغ "+str(money)+" به حساب "+str(number2)+" با موفقیت انتقال یافت"}), content_type='application/json')
                    else:
                        return HttpResponse(json.dumps({'response': False,'message':"موجودی شما کافی نیست"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"این حساب متعلق به شما نیست"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"همچین شماره حسابی مقصدی وجود ندارد"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"همچین شماره حسابی وجود ندارد"}), content_type='application/json')

    return HttpResponse(json.dumps({'response': False,'message':"خطا در انتقال حساب مجددا امتحان کنید"}), content_type='application/json')


def users_shaba(request):
    if request.method=="POST" and request.user is not None and request.user.is_authenticated:
        us=user_account.objects.filter(user=request.user)[0]
        number1=us.account_id.account_id
        number2=us.account_id.account_id_shaba
        return HttpResponse(json.dumps({'response': True,'number1':number1,'number2':number2}), content_type='application/json')


def users_remained(request):
    if request.method=="POST" and request.user is not None and request.user.is_authenticated:
        us=user_account.objects.filter(user=request.user)[0]
        remained=us.account_id.remain
        return HttpResponse(json.dumps({'response': True,'remained':remained}), content_type='application/json')


