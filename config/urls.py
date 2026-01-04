"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
import app.views

urlpatterns = [
    path("", app.views.handle_login, name='login'),
    path("admin_dashboard/", app.views.admin_dashboard, name='admin_dashboard'),
    path("reset-client-selection/", app.views.reset_client_selection, name='reset_client_selection'),
    path("admin_client_overview/", app.views.admin_client_overview, name='admin_client_overview'),
    path("admin_new_session_sheet", app.views.create_session_sheet, name='admin_new_session_sheet'),
    path("admin_prev_client_sessions", app.views.view_prevs_as_admin, name='admin_prev_client_sessions'),
    path("admin_update_client_account", app.views.update_client_account, name='admin_update_client_account'),
    path("admin_delete_user_profile", app.views.delete_user_profile, name='admin_delete_user_profile'),
    path("admin_create_user/", app.views.admin_user_creation, name='admin_create_user'),
    path("create_admin_user", app.views.create_admin_user, name='create_admin_user'),

    # Password Reset Flow:
    path("reset_password/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("reset_password/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # End Password Reset Flow.

    path("profile/", app.views.profile_view, name='profile'),
    path("user_overview/", app.views.user_overview, name='user_overview'),
    path("user_prev_sessions/", app.views.user_prev_sessions, name='user_prev_sessions'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("admin/", admin.site.urls),
]
