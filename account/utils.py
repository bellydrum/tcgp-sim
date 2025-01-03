from django.contrib.auth import authenticate, login


def validate_password(password1, password2):
    if password1 != password2:
        return False

    return True