from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path("", views.index, name="index"),
    path("log_out", views.log_out, name="log_out"),
    path("logout_success", views.logout_success, name="logout_success"),
    path("register", views.register, name="register"),
    path("user/", views.account_details, name="account_details"),
    path("user/<int:account_id>", views.account_details, name="account_details"),
]