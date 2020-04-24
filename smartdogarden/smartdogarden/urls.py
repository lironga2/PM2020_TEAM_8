"""smartdogarden URL Configuration

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
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from gardens import views as gardens_view
from dogsitterService import views as dogsitterService_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('d_o/profile/', user_views.d_o_profile, name='d_o_profile'),
    path('d_s/profile/', user_views.d_s_profile, name='d_s_profile'),
    path('d_g_a/profile/', user_views.d_g_a_profile, name='d_g_a_profile'),
    path('go_to_profile/', user_views.go_to_profile, name='go_to_profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('home.urls')),
    path('register_dog_owner/', user_views.register_as_dog_owner, name='register_D_O'),
    path('register_dog_sitter/', user_views.register_as_dog_sitter, name='register_D_S'),
    path('view_gardens/', gardens_view.view_gardens, name='view_gardens'),
    path('view_arrive_or_leave/', gardens_view.view_arrive_or_leave, name='view_arrive_or_leave'),
    path('view_test/', gardens_view.view_test, name='view_test'),
    path('view_who_in_garden/', gardens_view.view_who_in_garden, name='view_who_in_garden'),
    path('view_users_in_garden/', gardens_view.view_users_in_garden, name='view_users_in_garden'),
    path('view_dog_sitters/', user_views.view_dog_sitters, name='view_dog_sitters'),
    path('activity_time/', dogsitterService_view.activity_time, name='activity_time'),
    path('add_activity_time/', dogsitterService_view.add_activity_time, name='add_activity_time'),

]
