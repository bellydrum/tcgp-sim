from django.urls import path

from admin import views as admin_views
from account import views as account_views

urlpatterns = [
    path("", account_views.index, name="index"),
    path("reset_db", admin_views.reset_db, name="reset_db"),
]