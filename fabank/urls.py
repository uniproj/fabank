"""uni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main_admin import views as admin_views
from user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_login/', admin_views.admin_login),
    url(r'^is_login/', admin_views.is_login),
    url(r'^admin_logout/', admin_views.logout_func),
    url(r'^branch/create/', admin_views.branch_create),
    url(r'^branch/list/', admin_views.branch_list),
    url(r'^branch/search/', admin_views.branch_search),
    url(r'^branch/delete/', admin_views.branch_delete),
    url(r'^branch/edit/', admin_views.branch_edit),
    url(r'^employee/search/', admin_views.employee_search),
    url(r'^employee/list/', admin_views.employee_list),
    url(r'^employee/create/', admin_views.employee_create),
    url(r'^employee/delete/', admin_views.employee_delete),
    url(r'^employee/edit/', admin_views.employee_edit),
    url(r'^$', user_views.base),
    url(r'^home/', user_views.base),
    url(r'^users/is_login/', user_views.is_login2,name="user_login"),
    url(r'^users/logout/', user_views.logout_user),
    url(r'^users/about/', user_views.about_us),
    url(r'^users/contact/', user_views.contact_us),
    url(r'^users/profile/', user_views.profile),
    url(r'^users/change_pw/', user_views.change_pw),
    url(r'^users/login/', user_views.login_user),
    url(r'^users/transport/', user_views.users_transport),
    url(r'^users/shaba/', user_views.users_shaba),
    url(r'^users/remained/', user_views.users_remained),

    ]
