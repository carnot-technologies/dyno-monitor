"""
WSGI config for dynomonitor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
import subprocess

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynomonitor.settings')

application = get_wsgi_application()

from scheduler import start
start()

if bool(int(os.environ.get('RUN_WITHIN_WEB', 0))):
    subprocess.Popen([sys.executable, 'monitor.py'])
