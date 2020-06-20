import logging
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from logs.models import ErrorLog
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()


def db_table_exists(table_name):
    from django.db import connection
    return table_name in connection.introspection.table_names()


@scheduler.scheduled_job('cron', minute='45')
def cleanup_logs():
    """
    This function will run every hour and delete all logs older than 24 hours
    """
    logging.warning("Cleaning up logs older than {} hours".format(settings.TEMPORARY_LOG_RETENTION_HOURS))
    count, dct = ErrorLog.objects.filter(time_stamp__lte=now() - timedelta(hours=settings.TEMPORARY_LOG_RETENTION_HOURS)).delete()
    logging.warning("Count of logs deleted: {}".format(count))


def start():
    """
    Starts the scheduler to run in the background
    This method is called in `wsgi.py` file and starts the scheduler when the server starts
    """
    if not db_table_exists(ErrorLog._meta.db_table):
        return

    if not scheduler.running:
        logging.warning("Starting the background main scheduler")
        scheduler.start()
