import os
import sys
import time


DATABASE_NAME = "tcgpsim"

def alert(message):
    print(f"\n{message}\n")
    time.sleep(1)

os.system(f"dropdb {DATABASE_NAME}")
os.system(f"createdb {DATABASE_NAME}")

alert(f"Deleted and recreated database {DATABASE_NAME}.")

os.system("rm -r cards/migrations/00*")
os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")

alert(f"Reset all migrations and applied latest model structure.")

alert(f"Starting data import...")

os.system("python3 runscript.py import")

alert(f"Imported the latest data from data/imports.")