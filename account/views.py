from django.http import HttpResponse
from django.shortcuts import render

from account.models import *
from cards.models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponse(content="ayyyy heres ur account!")
    else:
        return render(request, "user_account.html")