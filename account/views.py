from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from account.models import *
from account.utils import validate_password
from cards.models import *


def index(request, account_id=None):
    return redirect("account:account_details", permanent=True)


@login_required
def account_details(request, account_id=None):
    # if not request.user.is_authenticated:
    #     print(f"\naccount_details | authenticated.\n")

    #     return redirect("account:register")
    # else:
    #     print(f"\naccount_details | not authenticated.\n")
    
    user_data = {
        "account_info": {
            "username": request.session.get("username"),
            "email": request.session.get("email")
        }
    }

    return render(request, "user-account.html", context=user_data)


@csrf_protect
def register(request):
    print(f"\n{request.method}\n")

    if request.method == "POST":
        if not validate_password(request.POST.get("password"), request.POST.get("password-verify")):
            pass

        validated_username = request.POST.get("username")
        validated_email = request.POST.get("email")
        validated_password = request.POST.get("password")

        new_user = User.objects.create_user(
            username=validated_username,
            email=validated_email,
            password=validated_password
        )

        new_user.save()

        user = authenticate(
            request,
            username=validated_username,
            password=validated_password
        )

        if user is not None:
            login(request, user)

        request.session["username"] = validated_username
        request.session["email"] = validated_email
        request.session["user_id"] = new_user.id

        print(f"\nREDIRECTING TO ACCOUNT_DETAILS....\n")

        print(f"account_id: {new_user.id}")

        return redirect("account:account_details", account_id=new_user.id)

    if not request.user.is_authenticated:
        return render(request, "register.html")
    
    user_data = {
        "account_info": {
            "username": request.session.get("username"),
            "email": request.session.get("email")
        }
    }

    return redirect("account:account_details", permanent=True, context=user_data)


@csrf_protect
def log_out(request):
    if not request.user.is_authenticated:
        return render(request, "register.html")

    logout(request)

    return redirect("account:logout_success")


def logout_success(request):
    return render(request, "logout_success.html")