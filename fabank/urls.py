
from django.conf.urls import url
from django.contrib import admin
from main_admin import views as admin_views
from user import views as user_views
from cashier import views as cashier_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^madmin/login/', admin_views.admin_login),
    url(r'^madmin/is_login/', admin_views.admin_is_login),
    url(r'^madmin/logout/', admin_views.admin_logout),

    url(r'^bill/set/', admin_views.bill_set),
    url(r'^tarefe/set/', admin_views.tarefe_set),



    url(r'^branch/create/', admin_views.branch_create),
    url(r'^branch/list/', admin_views.branch_list),
    url(r'^branch/search/', admin_views.branch_search),
    url(r'^branch/delete/', admin_views.branch_delete),
    url(r'^branch/edit/', admin_views.branch_edit),
    url(r'^branch/gain/', admin_views.branch_gain),
    url(r'^branch/employee/', admin_views.branch_employee),
    
    url(r'^employee/search/', admin_views.employee_search),
    url(r'^employee/list/', admin_views.employee_list),
    url(r'^employee/create/', admin_views.employee_create),
    url(r'^employee/delete/', admin_views.employee_delete),
    url(r'^employee/edit/', admin_views.employee_edit),
    
    url(r'^user/is_login/', user_views.is_login2,name="user_login"),
    url(r'^user/logout/', user_views.logout_user),
    url(r'^user/change_pw/', user_views.change_pw),
    url(r'^user/login/', user_views.login_user),
    url(r'^user/transport/', user_views.users_transport),
    url(r'^user/shaba/', user_views.users_shaba),
    url(r'^user/remained/', user_views.users_remained),
    
    url(r'^cashier/is_login/', cashier_views.cashier_is_login),
    url(r'^cashier/login/', cashier_views.cashier_login),
    url(r'^cashier/logout/', cashier_views.cashier_logout),
    url(r'^cashier/new_user/', cashier_views.cashier_new_user),
    url(r'^cashier/withdraw/', cashier_views.cashier_withdraw),
    url(r'^cashier/pay/', cashier_views.cashier_pay),
    url(r'^cashier/transport/', cashier_views.cashier_transport),
    url(r'^cashier/check/request/', cashier_views.cashier_check_request),
    url(r'^cashier/check/pay/', cashier_views.cashier_check_pay),
    
    url(r'^expert/login/', cashier_views.expert_login),
    url(r'^expert/users/get/', cashier_views.expert_users_get),
    url(r'^expert/user/confirm/', cashier_views.expert_user_confirm),
    url(r'^expert/user/lock/', cashier_views.expert_user_lock),
    url(r'^expert/user/unlock/', cashier_views.expert_user_confirm),
    url(r'^expert/vams/get/', cashier_views.expert_vams_get),
    url(r'^expert/vam/confirm/', cashier_views.expert_vam_confirm),

    url(r'^accountant/login/', cashier_views.accountant_login),
    url(r'^accountant/logout/', cashier_views.accountant_logout),
    url(r'^accountant/vams/get/', cashier_views.accountant_vams_get),


    url(r'^manager/login/', cashier_views.manager_login),
    url(r'^manager/logout/', cashier_views.manager_logout),
    url(r'^manager/atm/create/', cashier_views.manager_atm_create),
    url(r'^manager/atm/money/', cashier_views.manager_atm_money),

    url(r'^transaction/user/10/', cashier_views.ts_user_10),
    url(r'^transaction/user/2time/', cashier_views.ts_user_2time),
    url(r'^transaction/branch/2time/withdraw/', cashier_views.ts_branch_2time_withdraw),
    url(r'^transaction/branch/2time/pay/', cashier_views.ts_branch_2time_pay),
    url(r'^transaction/branches/pay/', cashier_views.ts_branches_pay),
    url(r'^transaction/branches/withdraw/', cashier_views.ts_branches_withdraw),
    url(r'^transaction/branch/number/', cashier_views.ts_branch_number),
    url(r'^transaction/accountant/2time/pay/', cashier_views.ts_user_2time_pay),
    url(r'^transaction/accountant/2time/withdraw/', cashier_views.ts_user_2time_withdraw),
    url(r'^transaction/accountant/remain/', cashier_views.ts_accountant_remain),

    url(r'^atm/login/', cashier_views.atm_login),
    url(r'^atm/withdraw/', cashier_views.atm_withdraw),
    url(r'^atm/transport/', cashier_views.atm_transport),


    url(r'^vam/request/', cashier_views.vam_request),
    url(r'^vam/pay/', cashier_views.vam_pay),

    ]
