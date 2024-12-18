#! /usr/bin/env python3

import django
import os
import sys
import threading
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproj.settings")
django.setup()

from admin.models import *


if __name__ != "__main__":
    print("\nPlease run this script directly.\n\t$ ./runscript.py <script_name>\n")
    sys.exit()


AVAILABLE_SCRIPTS = {}

# substrings used to match excluded directories when finding available scripts
EXCLUDE_DIRS = [
    "table_imports",
    "site_scrapers",
    "tools",
    "utils",
]

EXCLUDE_FILENAME_SUBSTRINGS = [
    "__init__",
    ".pyc",
    ".txt",
]

for dir_info in map(lambda dir_info: {dir_info[0]: dir_info[2]}, os.walk("scripts")):
    for dir_name, filenames in dir_info.items():
        if all([exclude_dir not in dir_name for exclude_dir in EXCLUDE_DIRS]):
            for filename in filenames:
                filename_without_extension = filename.split(".")[0]

                if all([i not in filename for i in EXCLUDE_FILENAME_SUBSTRINGS]):
                    AVAILABLE_SCRIPTS[filename_without_extension] = f"{dir_name}/{filename}"

script_name_param = sys.argv[-1]

if "runscript.py" in script_name_param:
    print(f"\nPlease provide a script name as a parameter.\n\t$ ./runscript.py <script_name>\n\nAvailable scripts: {[i for i in AVAILABLE_SCRIPTS]}\n")
    sys.exit()

if script_name_param.lower() not in AVAILABLE_SCRIPTS:
    print(f"""\nScript name "{script_name_param}" is invalid.\n\tAvailable scripts: {[i for i in AVAILABLE_SCRIPTS]}\n""")
    sys.exit()

script_filepath = AVAILABLE_SCRIPTS[script_name_param.lower()]

# if resetting the database, ensure there is a ScriptsActivity record in place
if script_filepath.endswith("reset_db.py"):
    if not ScriptsActivity.objects.all():
        ScriptsActivity.objects.create()

    scripts_activity = ScriptsActivity.objects.get(pk=1)
    database_reset_is_active = scripts_activity.database_reset_is_active

    connection.close()

command = f"python3 manage.py shell < {script_filepath}"

os.system(command)