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
from home import views as home_view

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
    path('hazard_report/', gardens_view.view_hazard_report, name='view_hazard_report'),
    path('report_on_hazard/', gardens_view.report_on_hazard, name='report_on_hazard'),
    path('all_hazard_report/', gardens_view.all_hazard_report, name='all_hazard_report'),
    path('view_all_hazard_report/', gardens_view.view_all_hazard_report, name='view_all_hazard_report'),
    path('dogsitter_service_coordination/', dogsitterService_view.view_dogsitter_service_coordination, name='view_dogsitter_service_coordination'),
    path('dogsitter_add_service_request/', dogsitterService_view.add_service_request, name='add_service_request'),
    path('cancel_service_request/', dogsitterService_view.cancel_service_request, name='cancel_service_request'),
    path('view_service_requests/', dogsitterService_view.view_service_requests, name='view_service_requests'),
    path('meeting_approval/', dogsitterService_view.meeting_approval, name='meeting_approval'),
    path('meeting_rejected/', dogsitterService_view.meeting_rejected, name='meeting_rejected'),
    path('my_meetings_d_o/', dogsitterService_view.view_my_meetings_dog_owner, name='view_my_meetings_dog_owner'),
    path('cancel_meeting/', dogsitterService_view.cancel_meeting, name='cancel_meeting'),
    path('my_meetings_d_s/', dogsitterService_view.view_my_meetings_dogsitter, name='view_my_meetings_dogsitter'),
    path('update_meeting', dogsitterService_view.update_meeting, name='update_meeting'),
    path('garden_admin_add_announcement', home_view.garden_admin_add_announcement, name='garden_admin_add_announcement'),
    path('view_reports', gardens_view.admin_view_reports, name='admin_view_reports'),
    path('view_reports_requests', gardens_view.admin_view_user_hazard_report_to_approve, name='view_reports_requests'),
    path('approve_hazard_report', gardens_view.admin_approve_hazard_report, name='approve_hazard_report'),
    path('reject_hazard_report', gardens_view.admin_reject_hazard_report, name='reject_hazard_report'),
    path('update_hazard_report_status', gardens_view.update_hazard_report_status, name='update_hazard_report_status'),
    path('edit_announcement_board', home_view.garden_admin_edit_announcement_board, name='edit_announcement_board'),
    path('delete_announcement', home_view.garden_admin_delete_announcement, name='delete_announcement'),
    path('view_users', home_view.admin_view_all_users, name='view_users'),
    path('view_dogsitter_usres', home_view.admin_view_dogsitter_users, name='view_dogsitter_usres'),
    path('view_dogowner_users', home_view.admin_view_dog_owner_users, name='view_dogowner_users'),
    path('delete_activity_time', dogsitterService_view.delete_activity_time, name='delete_activity_time'),
    path('delete_user', home_view.admin_delete_user, name='delete_user'),

]
