"""unlimited_studies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.conf import settings

from django.contrib import admin
from django.urls import include, path
from account import views
from django.contrib.auth import views as auth_views
from .views import home_screen_view

urlpatterns = [
    path("", home_screen_view, name="home"),
    path("studies/", include('studies.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    path("admin/", admin.site.urls, name="admin"),
    path("register/", views.registration_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("account/", views.account_view, name="account"),
    path("reset_password/", auth_views.PasswordResetView.as_view(
        template_name="account/password_reset.html"),
        name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_sent.html"),
        name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password_reset_form.html"),
         name="password_reset_confirm"),
    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password_reset_done.html"),
         name="password_reset_complete"),

]
