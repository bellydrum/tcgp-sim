import asyncio
import inspect
import os
import sys
import time


DATABASE_NAME = "tcgpsim"

def alert(message):
    print(f"\n{message}\n")
    time.sleep(1)

async def reset():
    try:
        if __name__ == "django.core.management.commands.shell":
            os.system(f"dropdb {DATABASE_NAME}")
            os.system(f"createdb {DATABASE_NAME}")

            alert(f"Deleted and recreated database {DATABASE_NAME}.")

            os.system("rm -r admin/migrations/0*")
            os.system("rm -r cards/migrations/0*")
            os.system("python3 manage.py makemigrations")
            os.system("python3 manage.py migrate")

            alert(f"Reset all migrations and applied latest model structure.")

            # sys.exit()

        alert(f"Starting data pull...")

        os.system("python3 runscript.py fetch")

        alert(f"Starting data import...")

        os.system("python3 runscript.py import")

        alert(f"Imported the latest data from data/imports.")
    except Exception as e:
        error_message = f"An error occurred during the database reset: {str(e)}"

        raise Exception(error_message)


if __name__ == "django.core.management.commands.shell":
    if inspect.iscoroutinefunction(reset):
        task = reset()

        result = asyncio.get_event_loop().run_until_complete(task)