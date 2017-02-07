from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core import serializers
from django.http import JsonResponse
from .models import account,staff,branch,bill,tarefe,ATM
import random


def admin_is_login(request):
    if request.user.is_authenticated:
        return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"you are not loged in"}), content_type='application/json')


def admin_login(request):
    if request.method == "GET":
        users=User.objects.filter(username=request.GET["username"])
        if(len(users)>0):
            user=users[0]
            user2 = authenticate(username=user.username, password=request.GET["password"])
            if user2 is not None:
                if user2.is_active and user2.is_superuser:
                    login(request,user2)
                    return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"your account is locked"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such user"}), content_type='application/json')

    return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def admin_logout(request):
    if request.method == "GET":
        logout(request)
        return HttpResponse(json.dumps({'response': True,'message':"you are loged out now"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"error on logout"}), content_type='application/json')



def branch_create(request):
    if request.user.is_authenticated and request.user.is_superuser:
        bol=False
        acc_id=0
        acc_id_shaba=0
        while (not bol):
            acc_id=create_account_id()
            acc_id_shaba=create_account_id_shaba()
            acc=account.objects.filter(account_id=acc_id,account_id_shaba=acc_id_shaba)
            if len(acc)==0:
                bol=True
        acc2=account.objects.create(account_id=acc_id,account_id_shaba=acc_id_shaba,lock=False)
        acc2.save()

        bn=request.GET["branch_name"]
        bs=request.GET["branch_state"]
        bc=request.GET["branch_city"]
        bl=request.GET["branch_address"]

        new_branch=branch.objects.create(name=bn,state=bs,city=bc,location=bl,account_id=acc2)
        new_branch.save()
        return HttpResponse(json.dumps({'response': True,'message':"branch created successfully",'branch_account_id':acc2.account_id,'branch_name':new_branch.name}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def create_account_id_shaba():
    return random.randint(100000000000,999999999999)



def create_account_id():
    return 6054*1000000000000+random.randint(100000000000,999999999999)



def branch_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        branches=branch.objects.all().order_by("pk")
        result=[]
        for i in range(len(branches)):
            rs={}
            rs['id']=branches[i].pk
            rs['name']=branches[i].name
            rs['state']=branches[i].state
            rs['city']=branches[i].city
            rs['location']=branches[i].location
            rs['account_id']=branches[i].account_id
            s=branches[i].manager_id
            if s is not None:
                rs['manager_id']=s.first_name+ " "+ s.last_name
            result.append(rs)

        return HttpResponse(result, content_type='application/json')


def employee_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        e=staff.objects.all().order_by("pk")
        result=[]
        for i in range(len(e)):
            rs={}
            rs['id']=e[i].pk
            rs['first_name']=e[i].first_name
            rs['last_name']=e[i].last_name
            rs['father_name']=e[i].father_name
            rs['nation_ID']=e[i].nation_ID
            rs['sex']=e[i].sex
            rs['cellphone']=e[i].cellphone_number
            rs['tellphone']=e[i].tellphone_number
            rs['address']=e[i].address
            rs['type']=e[i].employee_type
            b=branch.objects.filter(id=e[i].branch_in)[0]
            rs['branch_name']=b.name
            result.append(rs)
        return HttpResponse(result, content_type='application/json')


def branch_search(request):
    if request.user.is_authenticated and request.user.is_superuser:
        b1=branch.objects.filter(pk=request.GET["id"])
        result=[]
        rs={}
        if len(b1)>0:
            b=b1[0]
            rs['id']=b.pk
            rs['name']=b.name
            rs['state']=b.state
            rs['city']=b.city
            rs['location']=b.location
            rs['account_id']=b.account_id
            if b.manager_id is not None:
                rs['manager_id']=b.manager_id.pk
            result.append(rs)
            return HttpResponse(result, content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such branch"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def branch_delete(request):
    if request.user.is_authenticated and request.user.is_superuser:
        b=branch.objects.filter(pk=request.GET["id"])
        if(len(b)>0):
            b2=b[0].delete()
            return HttpResponse(json.dumps({'response': True,'message':"branch deleted successfully"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such branch"}), content_type='application/json')



def branch_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        b=branch.objects.filter(pk=request.GET["id"])
        if(len(b)>0):
            b2=b[0]
            b2.name=request.GET["name"]
            b2.state=request.GET["state"]
            b2.city=request.GET["city"]
            b2.location=request.GET["location"]
            if b2.manager_id is not None and request.GET["manager_id"] != b2.manager_id.id:
                manager=staff.objects.filter(pk=request.GET["manager_id"])
                if len(manager)>0 and manager[0].employee_type=="manager":
                    manager2=manager[0]
                    b2.manager_id=manager2
                    b2.save()
                    return HttpResponse(json.dumps({'response': True,'message':"branch edited successfully"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"no such manager"}), content_type='application/json')
            else:
                b2.save()
                return HttpResponse(json.dumps({'response': True,'message':"branch edited successfully"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such branch"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def employee_create(request):
    bot=False
    st2=staff.objects.filter(user=request.user)
    if len(st2)>0 and st2[0].employee_type=="manager":
        bol=True
    if (request.user.is_superuser or bol) and request.user.is_authenticated:
        fn=request.GET["first_name"]
        ln=request.GET["last_name"]
        fan=request.GET["father_name"]
        nid=request.GET["nation_ID"]
        s=request.GET["sex"]
        cf=request.GET["cellphone"]
        tf=request.GET["tellphone"]
        a=request.GET["address"]
        et=request.GET["employee_type"]
        b_int=request.GET["branch_id"]
        usr=User.objects.create_user(username=nid,password="h"+cf)
        usr.save()
        personnel=staff.objects.create(user=usr,first_name=fn,branch_in=b_int,last_name=ln,father_name=fan,nation_ID=nid,sex=s,cellphone_number=cf,tellphone_number=tf,address=a,employee_type=et)
        personnel.save()
        return HttpResponse(json.dumps({'response': True,'message':"employee created successfully"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def employee_delete(request):
    if request.user.is_authenticated and request.user.is_superuser:
        b=staff.objects.filter(pk=request.GET["id"])
        if(len(b)>0):
            b2=b[0].delete()
            return HttpResponse(json.dumps({'response': True,'message':"employee deleted successfully"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such employee"}), content_type='application/json')


def employee_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        b=staff.objects.filter(pk=request.GET["id"])
        if(len(b)>0):
            b2=b[0]
            b2.first_name=request.GET["first_name"]
            b2.last_name=request.GET["last_name"]
            b2.father_name=request.GET["father_name"]
            b2.nation_ID=request.GET["nation_ID"]
            b2.sex=request.GET["sex"]
            b2.cellphone_number=request.GET["cellphone"]
            b2.tellphone_number=request.GET["tellphone"]
            b2.address=request.GET["address"]
            b2.employee_type=request.GET["employee_type"]
            b2.branch_in=request.GET["branch_id"]
            b2.save()
            return HttpResponse(json.dumps({'response': True,'message':"emloyee edited successfully"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such branch"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def employee_search(request):
    if request.user.is_authenticated and request.user.is_superuser:
        b1=staff.objects.filter(pk=request.GET["id"])
        result=[]
        rs={}
        if len(b1)>0:
            b=b1[0]
            rs['id']=b.pk
            rs['first_name']=b.first_name
            rs['last_name']=b.last_name
            rs['father_name']=b.father_name
            rs['sex']=b.sex
            rs['cellphone']=b.cellphone_number
            rs['tellphone']=b.tellphone_number
            rs['address']=b.address
            rs['nation_ID']=b.nation_ID
            rs['employee_type']=b.employee_type
            result.append(rs)
            return HttpResponse(result, content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such employee"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def branch_employee(request):
    if request.user.is_authenticated and request.user.is_superuser:
        mnger=staff.objects.filter(nation_ID=request.GET["manager_id"])
        if len(mnger)<1:
            return HttpResponse(json.dumps({'response': False,'message':"no such manager"}), content_type='application/json')
        else:
            mn1=mnger[0]
            branches=branch.objects.filter(id=request.GET["branch_id"])
            if len(branches)<1:
                return HttpResponse(json.dumps({'response': False,'message':"no such branch"}), content_type='application/json')
            else:
                b=branches[0]
                b.manager_id=mn1
                b.save()
                mn1.branch_in=b.id
                mn1.save()
                return HttpResponse(json.dumps({'response': True,'message':"branch manager changed succesully"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def branch_gain(request):
    if request.user.is_authenticated and request.user.is_superuser:
        bs=branch.objects.filter(id=request.GET["branch_id"])
        if len(bs)<1:
            return HttpResponse(json.dumps({'response': False,'message':"no such branch"}), content_type='application/json')
        else:
            b=bs[0]
            b.sood=request.GET["gain"]
            b.save()
            return HttpResponse(json.dumps({'response': True,'message':"gain changed succesfully"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')
        


def bill_set(request):
    if request.user.is_authenticated and request.user.is_superuser:
        t=request.GET["type"]
        bs=bill.objects.filter(name=t)
        if len(bs)>0:
            b=bs[0]
            return HttpResponse(json.dumps({'response': True,'account_id':b.account_id.account_id,'remained':b.account_id.remain}), content_type='application/json')
        else:
            bol=False
            acc_id=0
            acc_id_shaba=0
            while (not bol):
                acc_id=create_account_id()
                acc_id_shaba=create_account_id_shaba()
                acc=account.objects.filter(account_id=acc_id,account_id_shaba=acc_id_shaba)
                if len(acc)==0:
                    bol=True
            acc2=account.objects.create(account_id=acc_id,account_id_shaba=acc_id_shaba,lock=False)
            acc2.save()
            b=bill.objects.create(name=t,account_id=acc2)
            b.save()
            return HttpResponse(json.dumps({'response': True,'account_id':acc2.account_id,'remained':acc2.remain}), content_type='application/json')   
    else:
        return HttpResponse(json.dumps({'response': False,'message':"you are not loged in"}), content_type='application/json')



def tarefe_set(request):
    if request.user.is_authenticated and request.user.is_superuser:
        t=request.GET["name"]
        bs=tarefe.objects.filter(name=t)
        if len(bs)>0:
            b=bs[0]
            b.pay=int(request.GET["pay"])
            b.name=request.GET["name"]
            b.save()
            return HttpResponse(json.dumps({'response': True,'name':b.name,'tarefe':b.pay}), content_type='application/json')
        else:
            b=tarefe.objects.create(name=t,pay=int(request.GET["pay"]))
            b.save()
            return HttpResponse(json.dumps({'response': True,'name':b.name,'tarefe':b.pay}), content_type='application/json')   
    else:
        return HttpResponse(json.dumps({'response': False,'message':"you are not loged in"}), content_type='application/json')


