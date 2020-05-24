# Reference for running standalone Django scripts
# https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
# This is so that django models get loaded.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynomonitor.settings')

application = get_wsgi_application()

from utils.rule_helper import build_rules

build_rules()


def blank():
    """
    Dummy function to prevent `imported but unsed` warnings in files where this is imported
    Function does nothing
    """
    pass
