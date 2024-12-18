from django.urls import path

from . import views

urlpatterns = [
    path("reset_db", views.reset_db, name="reset_db"),
]