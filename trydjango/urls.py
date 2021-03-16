"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user_views.redirect_view),
    
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('<int:myid>/profiledetail/', user_views.profiledetail, name='profiledetail'),
    path('<int:myid>/profileapprove/', user_views.profileapprove, name='profileapprove'),
    path('teacherapply/', user_views.teacherapply, name='teacherapply'),
    path('nonteacherapply/', user_views.nonteacherapply, name='nonteacherapply'),
    path('supervisorapply/', user_views.supervisorapply, name='supervisorapply'),
    path('applyforapply/', user_views.applyforapply, name='applyforapply'),
    path('applyforapply2/', user_views.applyforapply2, name='applyforapply2'),
    path('groupapplylistview', user_views.groupapplylistview, name='groupapplylistview'),
    path('<int:myid>/groupapplychangeview', user_views.groupapplychangeview, name='groupapplychangeview'),
    path('login_success/', user_views.login_success, name='login_success'),    
    path('success/', user_views.success, name='success'),
    path('successgroupapply/', user_views.successgroupapply, name='successgroupapply'),
    
    path('managerlistview/', user_views.managerlistview, name='managerlistview'),
    path('<int:myid>/managerapprove/', user_views.managerapprove, name='managerapprove'),
    path('vplistview/', user_views.vplistview, name='vplistview'),
    path('<int:myid>/vpapprove/', user_views.vpapprove, name='vpapprove'),
    path('secretarylistview/', user_views.secretarylistview, name='secretarylistview'),
    path('<int:myid>/secretaryapprove/', user_views.secretaryapprove, name='secretaryapprove'),
    path('plistview/', user_views.plistview, name='plistview'),
    path('<int:myid>/papprove/', user_views.papprove, name='papprove'),
    path('plistviewdecided/', user_views.plistviewdecided, name='plistviewdecided'),
    path('<int:myid>/papprovedecided/', user_views.papprovedecided, name='papprovedecided'),
    path('userlistview/', user_views.userlistview, name='userlistview'),
    path('<int:myid>/userdetailview/', user_views.userdetailview, name='userdetailview'),
    path('incrementallview/', user_views.incrementallview, name='incrementallview'),
    path('incrementlistview/', user_views.incrementlistview, name='incrementlistview'),
    path('prependinglistview/', user_views.prependinglistview, name='prependinglistview'),
    path('<int:myid>/prependingdetailview/', user_views.prependingdetailview, name='prependingdetailview'),
    path('alllistview/', user_views.alllistview, name='alllistview'),
    path('<int:myid>/alldetailview/', user_views.alldetailview, name='alldetailview'),
    path('documentlistview/', user_views.documentlistview, name='documentlistview'),
    path('<int:myid>/documentdetailview/', user_views.documentdetailview, name='documentdetailview'),
    path('calendarlistview/', user_views.calendarlistview, name='calendarlistview'),
    path('<int:myid>/calendardetailview/', user_views.calendardetailview, name='calendardetailview'),
    path('change_password/', user_views.change_password, name='change_password'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






