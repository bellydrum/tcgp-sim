import asyncio
import inspect
import os
import sys
import time


def restart():
    os.system("clear")
    os.system("python3 manage.py collectstatic --no-input")
    os.system("python3 manage.py runserver")

if __name__ == "django.core.management.commands.shell":
    restart()