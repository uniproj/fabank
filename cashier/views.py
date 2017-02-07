from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core import serializers
from django.http import JsonResponse
from main_admin.models import account,staff,branch,transaction,ATM
from user.models import user_account,check,vam
import random
import datetime
from django.utils import timezone



def cashier_is_login(request):
    if request.user.is_authenticated:
        return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"you are not loged in"}), content_type='application/json')



def cashier_login(request):
    if request.method=="GET":
        users=User.objects.filter(username=request.GET["username"])
        if(len(users)>0):
            user=users[0]
            st2=staff.objects.filter(user=user)
            if len(st2)>0 and st2[0].employee_type=="cashier":
	            user2 = authenticate(username=user.username, password=request.GET["password"])
	            if user2 is not None:
	                if user2.is_active:
	                    login(request,user2)
	                    return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
	            else:
	                return HttpResponse(json.dumps({'response': False,'message':"your account is locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such cashier"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such user"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def cashier_logout(request):
    if request.method == "GET":
        logout(request)
        return HttpResponse(json.dumps({'response': True,'message':"you are loged out now"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"error on logout"}), content_type='application/json')


def cashier_new_user(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            us=User.objects.create_user(username=request.GET["nation_ID"],password="h"+request.GET["cellphone_number"])
            us.save()
            n=request.GET["name"]
            f_n=request.GET["father_name"]
            s=request.GET["sex"]
            c_n=request.GET["cellphone_number"]
            t_n=request.GET["tellphone_number"]
            a=request.GET["address"]
            nid=request.GET["nation_ID"]
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
            u=user_account.objects.create(user=us,name=n,father_name=f_n,sex=s,cellphone_number=c_n,tellphone_number=t_n,address=a,nation_ID=nid,account_id=acc2)
            u.save()

            bch=branch.objects.filter(id=st2.branch_in)[0]
            if bch is not None:
                acc=bch.account_id
                if acc is not None:
                    acc.remain =acc.remain + 100000
                    acc.save()
                    t=transaction.objects.create(t_type="create user",t_branch=bch,t_staff=st2,t_account=acc2,t_message="create a user")
                    t.save()
                    return  HttpResponse(json.dumps({'response': True,'message':"user "+request.GET["name"] +" created successfully"}), content_type='application/json')
                else:
                    return  HttpResponse(json.dumps({'response': True,'message':"user "+request.GET["name"] +" created successfully"}), content_type='application/json')
            else:
                return  HttpResponse(json.dumps({'response': True,'message':"user "+request.GET["name"] +" created successfully"}), content_type='application/json')
        else:
             return HttpResponse(json.dumps({'response': False,'message':"no access"}), content_type='application/json')
    else:
         return HttpResponse(json.dumps({'response': False,'message':"no access"}), content_type='application/json')


def create_account_id_shaba():
    return random.randint(100000000000,999999999999)



def create_account_id():
    return 6054*1000000000000+random.randint(100000000000,999999999999)

def cashier_withdraw(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            pay=request.GET["pay"]
            us=request.GET["account_id"]
            acc=account.objects.filter(account_id=us)
            if len(acc)>0:
                acc2=acc[0]
                usr=user_account.objects.filter(account_id=acc2)[0]
                if not acc2.lock and usr.is_active:
                    if int(pay) <= acc2.remain-100000:
                        acc2.remain=acc2.remain-int(pay)
                        acc2.save()
                        bch=branch.objects.filter(id=st2.branch_in)[0]
                        t=transaction.objects.create(t_money=int(pay),t_type="withdraw",t_branch=bch,t_staff=st2,t_account=acc2,t_message="")
                        t.save()
                        return HttpResponse(json.dumps({'response': True,'message':"widthraw successfully"}), content_type='application/json')
                    else:
                        return HttpResponse(json.dumps({'response': False,'message':"low remain"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"you are locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such account"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def cashier_transport(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            pay=request.GET["pay"]
            us=request.GET["account_id1"]
            us2=request.GET["account_id2"]
            acc=account.objects.filter(account_id=us)
            acc2=account.objects.filter(account_id=us2)
            if len(acc)>0 and len(acc2)>0:
                ac=acc[0]
                ac2=acc2[0]
                usr=user_account.objects.filter(account_id=ac)[0]
                usr2=user_account.objects.filter(account_id=ac2)[0]
                if not ac.lock and usr.is_active and not ac2.lock:
                    if int(pay)<=ac.remain-100000:
                        ac.remain=ac.remain-int(pay)
                        ac.save()
                        ac2.remain=ac2.remain+int(pay)
                        ac2.save()
                        bch=branch.objects.filter(id=st2.branch_in)[0]
                        t=transaction.objects.create(t_money=int(pay),t_type="transport",t_branch=bch,t_staff=st2,t_account=ac,t_message="to account"+str(ac2.account_id))
                        t.save()
                        return HttpResponse(json.dumps({'response': True,'message':"transport successfully"}), content_type='application/json')
                    else:
                        return HttpResponse(json.dumps({'response': False,'message':"low remain"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"you are locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such account"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def cashier_pay(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            pay=request.GET["pay"]
            us=request.GET["account_id"]
            acc=account.objects.filter(account_id=us)
            if len(acc)>0:
                ac=acc[0]
                usr=user_account.objects.filter(account_id=ac)[0]
                if not ac.lock and usr.is_active:
                    if True:
                        ac.remain=ac.remain+int(pay)
                        ac.save()
                        bch=branch.objects.filter(id=st2.branch_in)[0]
                        t=transaction.objects.create(t_money=int(pay),t_type="pay",t_branch=bch,t_staff=st2,t_account=ac,t_message="")
                        t.save()
                        return HttpResponse(json.dumps({'response': True,'message':"pay successfully"}), content_type='application/json')
                    else:
                        return HttpResponse(json.dumps({'response': False,'message':"low remain"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"you are locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such account"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def cashier_check_request(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            result=[]
            rs={}
            a=request.GET["account_id"]
            acc=account.objects.filter(account_id=a)
            if len(acc)>0:
                acc2=acc[0]
            else:
                return HttpResponse(json.dumps({'response':False,'message':"no such account id"}),content_type='application/json')
            usr=user_account.objects.filter(account_id=acc[0])[0]
            if usr.is_active and not acc2.lock:
                for i in range(10):
                    b=check.objects.create(user=usr,user_acc=acc[0],is_used=False)
                    b.save()
                    rs['number'+str(i+1)]=b.id
                    rs['response']=True
                    rs['message']="check created successfully"
                    result.append(rs)
                bch=branch.objects.filter(id=st2.branch_in)[0]
                t=transaction.objects.create(t_type="check request",t_branch=bch,t_staff=st2,t_account=acc[0],t_message="")
                t.save()
                return HttpResponse(result,content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response':False,'message':"you are locked"}),content_type='application/json')
       	else:
       		return HttpResponse(json.dumps({'response':False,'message':"you are not cashier"}),content_type='application/json')
    else:
    	return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')


def cashier_check_pay(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            a=request.GET["check_id"]
            chck=check.objects.filter(id=a)
            if len(chck)>0:
                chck2=chck[0]
            else:
                return HttpResponse(json.dumps({'response':False,'message':"no such check id"}),content_type='application/json')
            usr=chck[0].user_acc
            if not usr.lock:
                if int(request.GET["pay"]) < usr.remain:
                    usr.remain=usr.remain-int(request.GET["pay"])
                    usr.save()
                    chck[0].pay=int(request.GET["pay"])
                    chck[0].dar_vajh=request.GET["for"]
                    chck[0].is_used=True
                    chck[0].save()
                    bch=branch.objects.filter(id=st2.branch_in)[0]
                    t=transaction.objects.create(t_money=int(request.GET["pay"]),t_type="check pay",t_branch=bch,t_staff=st2,t_account=usr,t_message="payed to "+request.GET["for"])
                    t.save()
                    return HttpResponse(json.dumps({'response':True,'message':"check checked successfully"}),content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response':False,'message':"not enough money"}),content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response':False,'message':"you are locked"}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not cashier"}),content_type='application/json')
    else:
    	return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')



def expert_login(request):
    if request.method=="GET":
        users=User.objects.filter(username=request.GET["username"])
        if(len(users)>0):
            user=users[0]
            st2=staff.objects.filter(user=user)
            if len(st2)>0 and st2[0].employee_type=="expert":
	            user2 = authenticate(username=user.username, password=request.GET["password"])
	            if user2 is not None:
	                if user2.is_active:
	                    login(request,user2)
	                    return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
	            else:
	                return HttpResponse(json.dumps({'response': False,'message':"your account is locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such cashier"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such user"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def expert_users_get(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="expert":
        	us=user_account.objects.filter(is_active=False)
        	result=[]
        	for i in range(len(us)):
	            rs={}
	            rs['id']=us[i].pk
	            rs['name']=us[i].name
	            rs['father_name']=us[i].father_name
	            rs['sex']=us[i].sex
	            rs['cellphone_number']=us[i].cellphone_number
	            rs['tellphone_number']=us[i].tellphone_number
	            rs['address']=us[i].address
	            rs['nation_ID']=us[i].nation_ID
	            rs['account_id']=us[i].account_id.account_id
	            result.append(rs)

        	return HttpResponse(result, content_type='application/json')
       	else:
       		return HttpResponse(json.dumps({'response':False,'message':"you are not expert"}),content_type='application/json')
    else:
    	return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')



def expert_user_confirm(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="expert":
            us=user_account.objects.filter(nation_ID=request.GET["nation_ID"])[0]
            us.is_active=True
            us.save()
            bch=branch.objects.filter(id=st2.branch_in)[0]
            t=transaction.objects.create(t_type="confirm account",t_branch=bch,t_staff=st2,t_account=us.account_id,t_message="")
            t.save()
            return HttpResponse(json.dumps({'response':True,'message':"user confirmed"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not expert"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')


def expert_user_lock(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="expert":
            us=user_account.objects.filter(nation_ID=request.GET["nation_ID"])[0]
            us.is_active=False
            us.save()
            bch=branch.objects.filter(id=st2.branch_in)[0]
            t=transaction.objects.create(t_type="lock user",t_branch=bch,t_staff=st2,t_account=us.account_id,t_message="")
            t.save()
            return HttpResponse(json.dumps({'response':True,'message':"user confirmed"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not expert"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')


def ts_user_10(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            acc=account.objects.filter(account_id=request.GET["account_id"])[0]
            tss=transaction.objects.filter(t_account=acc).order_by("-t_date")
            if len(tss)>10:
                tss=tss[0:10]
            result=[]
            rs={}
            for i in range(len(tss)):
                rs["type"]=tss[i].t_type
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                result.append(rs)
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')

def ts_user_2time(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            acc=account.objects.filter(account_id=request.GET["account_id"])[0]
            tss=transaction.objects.filter(t_account=acc,t_date__range=[request.GET["begin"],request.GET["end"]])
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["type"]=tss[i].t_type
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                result.append(rs)
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def ts_branch_2time_withdraw(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superuser:
            bch=branch.objects.filter(id=request.GET["branch_id"])[0]
            tss=transaction.objects.filter(t_branch=bch,t_type="withdraw",t_date__range=[request.GET["begin"],request.GET["end"]])
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                result.append(rs)
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not admin"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def ts_branch_2time_pay(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superuser:
            bch=branch.objects.filter(id=request.GET["branch_id"])[0]
            tss=transaction.objects.filter(t_branch=bch,t_type="pay",t_date__range=[request.GET["begin"],request.GET["end"]])
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                result.append(rs)
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def ts_branches_pay(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superuser:
            tss=transaction.objects.filter(t_type="pay")
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                rs["branch"]=tss[i].t_branch.name
                rs["account"]=tss[i].t_account.account_id
                result.append(rs)

            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def ts_branches_withdraw(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superuser:
            tss=transaction.objects.filter(t_type="withdraw")
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                rs["branch"]=tss[i].t_branch.name
                rs["account"]=tss[i].t_account.account_id
                result.append(rs)
                
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def ts_branch_number(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superuser:
            bch=branch.objects.filter(id=request.GET["branch_id"])[0]
            tss=transaction.objects.filter(t_type=request.GET["type"],t_branch=bch).order_by("-t_date")
            if len(tss)>int(request.GET["number"]):
                tss=tss[0:int(request.GET["number"])]
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                rs["branch"]=tss[i].t_branch.name
                rs["account"]=tss[i].t_account.account_id
                result.append(rs)
                
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not admin"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def accountant_login(request):
    if request.method=="GET":
        users=User.objects.filter(username=request.GET["username"])
        if(len(users)>0):
            user=users[0]
            st2=staff.objects.filter(user=user)
            if len(st2)>0 and st2[0].employee_type=="accountant":
                user2 = authenticate(username=user.username, password=request.GET["password"])
                if user2 is not None:
                    if user2.is_active:
                        login(request,user2)
                        return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"your account is locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such accountant"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such user"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def accountant_logout(request):
    if request.method == "GET":
        logout(request)
        return HttpResponse(json.dumps({'response': True,'message':"you are loged out now"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"error on logout"}), content_type='application/json')




def ts_user_2time_pay(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="accountant":
            acc=account.objects.filter(account_id=request.GET["account_id"])[0]
            tss=transaction.objects.filter(t_account=acc,t_date__range=[request.GET["begin"],request.GET["end"]],t_type="pay")
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["type"]=tss[i].t_type
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                result.append(rs)
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not accountant"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')




def ts_user_2time_withdraw(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="accountant":
            acc=account.objects.filter(account_id=request.GET["account_id"])[0]
            tss=transaction.objects.filter(t_account=acc,t_date__range=[request.GET["begin"],request.GET["end"]],t_type="withdraw")
            result=[]
            rs={}
            if len(tss)<1:
                return HttpResponse(json.dumps({'response': False,'message':"not any transaction"}), content_type='application/json')
            for i in range(len(tss)):
                rs["type"]=tss[i].t_type
                rs["date"]=tss[i].t_date
                rs["time"]=tss[i].t_time
                rs["money"]=tss[i].t_money
                result.append(rs)
            return HttpResponse(result,content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not accountant"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def ts_accountant_remain(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="accountant":
            bch=branch.objects.filter(id=st2.branch_in)[0]
            acc=bch.account_id
            r=acc.remain
            return HttpResponse(json.dumps({'response': True,'message':"remained "+str(r)}), content_type='application/json')    
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not accountant"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def manager_login(request):
    if request.method=="GET":
        users=User.objects.filter(username=request.GET["username"])
        if(len(users)>0):
            user=users[0]
            st2=staff.objects.filter(user=user)
            if len(st2)>0 and st2[0].employee_type=="manager":
                user2 = authenticate(username=user.username, password=request.GET["password"])
                if user2 is not None:
                    if user2.is_active:
                        login(request,user2)
                        return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"your account is locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such manager"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such user"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')



def manager_logout(request):
    if request.method == "GET":
        logout(request)
        return HttpResponse(json.dumps({'response': True,'message':"you are loged out now"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"error on logout"}), content_type='application/json')




def manager_atm_create(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="manager":
            bch=branch.objects.filter(id=st2.branch_in)[0]
            bol=False
            acc_id=0
            acc_id_shaba=0
            while (not bol):
                acc_id=create_account_id()
                acc_id_shaba=create_account_id_shaba()
                acc=account.objects.filter(account_id=acc_id,account_id_shaba=acc_id_shaba)
                if len(acc)==0:
                    bol=True
            acc2=account.objects.create(account_id=acc_id,account_id_shaba=acc_id_shaba,lock=False,remain=0)
            acc2.save()
            a=ATM.objects.create(bch=bch,acc=acc2)
            a.save()
            return HttpResponse(json.dumps({'response': True,'message':"ATM created successfully",'account_id':acc2.account_id,'ATM_id':a.id}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not accountant"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def manager_atm_money(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="manager":
            a=ATM.objects.filter(id=request.GET["atm_id"])[0]
            a.a_1000=int(request.GET["a_10000"])
            a.a_2000=int(request.GET["a_20000"])
            a.a_5000=int(request.GET["a_50000"])
            a.a_10000=int(request.GET["a_100000"])
            a.a_50000=int(request.GET["a_500000"])
            a.save()
            acc=a.acc
            acc.remain=a.a_10000*10000+a.a_20000*20000+a.a_50000*50000+a.a_100000*100000+a.a_500000*500000
            acc.save()
            return HttpResponse(json.dumps({'response': True,'message':"ATM remained money is : "+str(acc.remain)}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not accountant"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')




def atm_login(request):
    if request.method=="GET":
        users=User.objects.filter(username=request.GET["username"])
        if(len(users)>0):
            user=users[0]
            st2=user_account.objects.filter(user=user)
            if len(st2)>0:
                st3=st2[0]
                user2 = authenticate(username=user.username, password=request.GET["password"])
                if user2 is not None:
                    if user2.is_active:
                        login(request,user2)
                        return HttpResponse(json.dumps({'response': True,'message':"you are loged in now"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"your account is locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such users"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"no such user"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')


def atm_withdraw(request):
    if request.user.is_authenticated:
        user=request.user
        st2=user_account.objects.filter(user=user)[0]
        acc2=st2.account_id
        money=int(request.GET["money"])
        if money > acc2.remain-100000:
            return HttpResponse(json.dumps({'response': False,'message':"you have not enough money"}), content_type='application/json')
        a=ATM.objects.filter(id=request.GET["atm_id"])[0]
        if money > a.acc.remain:
            return HttpResponse(json.dumps({'response': False,'message':"The ATM has not enough money"}), content_type='application/json')
        a_500000=0
        a_100000=0
        a_50000=0
        a_20000=0
        a_10000=0
        acc2.remain=acc2.remain-money
        acc2.save()
        bol=True
        if money>500000 and a.a_500000>0:
            bol=True
        while(bol):
            a_500000 = a_500000+1
            a.a_500000=a.a_500000-1
            a.save()
            money=money-500000
            if money>500000 and a.a_500000>0:
                bol=True
            else:
                bol=False
        bol=True
        if money>100000 and a.a_100000>0:
            bol=True
        while(bol):
            a_100000 = a_100000+1
            a.a_100000=a.a_100000-1
            a.save()
            money=money-100000
            if money>100000 and a.a_100000>0:
                bol=True
            else:
                bol=False
        bol=True
        if money>50000 and a.a_50000>0:
            bol=True
        while(bol):
            a_50000 = a_50000+1
            a.a_50000=a.a_50000-1
            a.save()
            money=money-50000
            if money>50000 and a.a_50000>0:
                bol=True
            else:
                bol=False
        bol=True
        if money>20000 and a.a_20000>0:
            bol=True
        while(bol):
            a_20000 = a_20000+1
            a.a_20000=a.a_20000-1
            a.save()
            money=money-20000
            if money>20000 and a.a_20000>0:
                bol=True
            else:
                bol=False
        bol=True
        if money>10000 and a.a_10000>0:
            bol=True
        while(bol):
            a_10000 = a_10000+1
            a.a_10000=a.a_10000-1
            a.save()
            money=money-10000
            if money>10000 and a.a_10000>0:
                bol=True
            else:
                bol=False
        a.save()
        
        acc=a.acc
        acc.remain=a.a_10000*10000+a.a_20000*20000+a.a_50000*50000+a.a_100000*100000+a.a_500000*500000
        acc.save()
        return HttpResponse(json.dumps({'response': True,'message':""}), content_type='application/json')
        
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')




def atm_transport(request):
    if request.user.is_authenticated:
        user=request.user
        us=user_account.objects.filter(user=user)[0]
        acc4=us.account_id
        if True:
            pay=request.GET["pay"]
            us=acc4.account_id
            us2=request.GET["account_id2"]
            acc=account.objects.filter(account_id=us)
            acc2=account.objects.filter(account_id=us2)
            if len(acc)>0 and len(acc2)>0:
                ac=acc[0]
                ac2=acc2[0]
                usr=user_account.objects.filter(account_id=ac)[0]
                usr2=user_account.objects.filter(account_id=ac2)[0]
                if not ac.lock and usr.is_active and not ac2.lock:
                    if int(pay)<=ac.remain-100000:
                        ac.remain=ac.remain-int(pay)
                        ac.save()
                        ac2.remain=ac2.remain+int(pay)
                        ac2.save()
                        bch=branch.objects.filter(id=st2.branch_in)[0]
                        t=transaction.objects.create(t_money=int(pay),t_type="transport",t_branch=bch,t_staff=st2,t_account=ac,t_message="to account"+str(ac2.account_id))
                        t.save()
                        return HttpResponse(json.dumps({'response': True,'message':"transport successfully"}), content_type='application/json')
                    else:
                        return HttpResponse(json.dumps({'response': False,'message':"low remain"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'response': False,'message':"you are locked"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'response': False,'message':"no such account"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response': False,'message':"you are not cashier"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response': False,'message':"wrong request"}), content_type='application/json')




def vam_request(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            us=user_account.objects.filter(nation_ID=request.GET["nation_ID"])
            if len(us)==0:
                return HttpResponse(json.dumps({'response':False,'message':"nos uch user"}),content_type='application/json')

            money=int(request.GET["money"])
            monthes=int(request.GET["monthes"])
            v=vam.objects.create(user=us[0],money=money,monthes=monthes,payed=0,payback=money*1.14)
            v.save()
            bch=branch.objects.filter(id=st2.branch_in)[0]
            acc=bch.account_id
            acc.remain=acc.remain-money
            acc.save()
            acc=us[0].account_id
            acc.remain=acc.remain+money
            acc.save()
            t=transaction.objects.create(t_type="vam request",t_branch=bch,t_staff=st2,t_account=acc,t_message="",t_money=money)
            t.save()
            return HttpResponse(json.dumps({'response':True,'message':"vam requested successfully"}),content_type='application/json')      

        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not cashier"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')




def vam_pay(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="cashier":
            us=user_account.objects.filter(nation_ID=request.GET["nation_ID"])
            if len(us)==0:
                return HttpResponse(json.dumps({'response':False,'message':"nos uch user"}),content_type='application/json')

            money=int(request.GET["vam_id"])
            v=vam.objects.filter(id=money)
            v.payed=v.payed+1
            v.save()
            bch=branch.objects.filter(id=st2.branch_in)[0]
            acc=bch.account_id
            acc.remain=acc.remain+int(v.payback/v.monthes)
            acc.save()
            t=transaction.objects.create(t_type="vam pay",t_branch=bch,t_staff=st2,t_account=acc,t_message="",t_money=int(v.payback/v.monthes))
            t.save()
            return HttpResponse(json.dumps({'response':True,'message':"vam requested successfully"}),content_type='application/json')      

        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not cashier"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')





def expert_vams_get(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="expert":
            us=vam.objects.filter(is_confirmed=False)
            result=[]
            for i in range(len(us)):
                rs={}
                rs['id']=us[i].pk
                rs['name']=us[i].user.name
                rs['nation_ID']=us[i].user.nation_ID
                rs['account_id']=us[i].user.account_id.account_id
                rs['money']=us[i].money
                rs['monthes']=us[i].monthes
                result.append(rs)

            return HttpResponse(result, content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not expert"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')




def expert_vam_confirm(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="expert":
            us=vam.objects.filter(id=request.GET["vam_id"])[0]
            us.is_confirmed=True
            us.save()
            return HttpResponse(json.dumps({'response':True,'message':"vam confirmed"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not expert"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')



def accountant_vams_get(request):
    if request.user.is_authenticated:
        user=request.user
        st2=staff.objects.filter(user=user)[0]
        if st2.employee_type=="accountant":
            us=vam.objects.all()
            result=[]
            for i in range(len(us)):
                rs={}
                rs['id']=us[i].pk
                rs['name']=us[i].user.name
                rs['nation_ID']=us[i].user.nation_ID
                rs['account_id']=us[i].user.account_id.account_id
                rs['money']=us[i].money
                rs['monthes']=us[i].monthes
                result.append(rs)

            return HttpResponse(result, content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':False,'message':"you are not expert"}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'response':False,'message':"you are not login"}),content_type='application/json')

