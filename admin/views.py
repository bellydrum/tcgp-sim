import asyncio
import inspect
import threading
from django.http import HttpResponse
from django.shortcuts import render

from scripts.reset_db import reset


async def reset_db(request):
    secondary_loop = asyncio.new_event_loop()

    secondary_thread = threading.Thread(
        target=secondary_loop.run_forever,
        name="Reset Database Loop"
    )

    secondary_thread.start()

    asyncio.run_coroutine_threadsafe(reset(), secondary_loop)

    return HttpResponse("Initiated database reset.")