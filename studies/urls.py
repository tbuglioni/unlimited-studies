from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.personal_home_view, name="personal_home"),
]
