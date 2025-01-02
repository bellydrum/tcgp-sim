from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path("", views.index, name="index"),
    # path("/register", views.register, name="register"),
    # path("/user/<int:account_id>", views.account_details, name="account_details")
]