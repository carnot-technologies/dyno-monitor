import os
import sys
import logging

ENABLE_EMAILS = bool(int(os.environ.get('ENABLE_EMAILS', 1)))
MAIL_PREFIX = '[DYNO-MON]'

# Logging
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
LOGGING_LEVEL_OPTIONS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
LOGGING_FORMAT = '%(levelname)s: %(message)s'

if LOGGING_LEVEL not in LOGGING_LEVEL_OPTIONS:
    LOGGING_LEVEL = 'DEBUG'

logging.basicConfig(
    level=LOGGING_LEVEL,
    format=LOGGING_FORMAT,
    stream=sys.stdout
)

# Threading Settings
SENTINAL_THREAD_PERIOD = 15.0

# Heroku API
# TODO: Remove hardcoded fallback key
HEROKU_API_KEY = str(os.environ.get('HEROKU_API_KEY', '***REMOVED***'))
HEROKU_APP_NAME = str(os.environ.get('HEROKU_APP_NAME', 'dyno-monitor'))

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'live')
