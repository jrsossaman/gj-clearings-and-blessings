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
    path("admin_create_user/", app.views.admin_user_creation, name='admin_create_user'),

    # Password Reset Flow:
    path("reset_password/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("reset_password/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # End Password Reset Flow.

    path("profile/", app.views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("admin/", admin.site.urls),
]
