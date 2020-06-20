import os
import sys
import logging

# Email settings
ENABLE_EMAILS = bool(int(os.environ.get('ENABLE_EMAILS', 1)))
EMAIL_PREFIX = os.environ.get('EMAIL_PREFIX', '[DYNO-MON]')

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = bool(int(os.environ.get('EMAIL_USE_TLS', 1)))
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
RECIPIENTS = os.environ.get('RECIPIENTS').split(',') if os.environ.get('RECIPIENTS') else []


# Django email recipient settings
ADMINS = tuple(('admin:' + str(RECIPIENTS.index(i)), i) for i in RECIPIENTS)
MANAGERS = ADMINS


EMAIL_COOLING_PERIOD_PER_TOPIC = int(os.environ.get('EMAIL_COOLING_PERIOD_PER_TOPIC', 300))
APP_RESTART_COOLING_PERIOD = int(os.environ.get('APP_RESTART_COOLING_PERIOD', 300))
DYNO_RESTART_COOLING_PERIOD = int(os.environ.get('DYNO_RESTART_COOLING_PERIOD', 300))
TEMPORARY_LOG_RETENTION_HOURS = int(os.environ.get('TEMPORARY_LOG_RETENTION_HOURS', 24))


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

# Redis Settings
CACHE_REDIS_URL = os.environ.get('REDIS_URL')

# Heroku API
HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY')

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'live')
