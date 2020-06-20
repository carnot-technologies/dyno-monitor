import sys
import time
import logging
import threading
import traceback
import load_django
from django.conf import settings

from utils.heroku import HerokuInterface
from utils.parser import parse
from utils.rule_helper import fetch_rules


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def sentinal():
    fetch_rules()

    logging.info("Sentinal thread run. Total thread count: {}".format(threading.active_count()))
    logging.debug(threading.enumerate())

    # Get all currently active threads. This will include all the logging threads
    # and two additional threads:
    # - Main Thread in stopped state,
    # - and this (sentinal) Timer Thread in running state
    active_threads = [th.name for th in threading.enumerate()]

    for logsrc in list(settings.RULES.keys()):
        if logsrc not in active_threads:
            # Log source not present from the thread list
            # Creating the missing thread
            start_thread(logsrc)

    threading.Timer(settings.SENTINAL_THREAD_PERIOD, sentinal).start()


def stream_logs(app_name, source, dyno):
    while True:
        # Main Thread Loop
        try:
            for line in HerokuInterface().stream_log(app_name=app_name, source=source, dyno=dyno, timeout=100):
                # Search for the required keywords in this line
                logging.debug(line.decode('utf-8'))
                exit = parse(line.decode('utf-8'), app_name, source, dyno)

                if exit:
                    break

            root = app_name + settings.SEPERATOR + source + settings.SEPERATOR + dyno
            exit = True if root not in settings.RULES else False

            if exit:
                break

        except Exception:
            logging.error(traceback.format_exc())
            # TODO: Handle specific exceptions here
            # Cooling period in case of errors
            time.sleep(1)

    logging.info("Stopping log thread: {}:{}:{}".format(app_name, source, dyno))


def start_thread(logsrc):
    parts = logsrc.split(settings.SEPERATOR)

    if len(parts) != 3:
        logging.error("Invalid Rule: {}".format(logsrc))
        return

    t = threading.Thread(target=stream_logs, args=(parts[0], parts[1], parts[2]), name=logsrc)
    t.start()
    logging.info("Started log thread: {}".format(logsrc))


if __name__ == '__main__':

    logging.info("Starting Dyno Monitor " + settings.ENVIRONMENT)
    threading.Timer(settings.SENTINAL_THREAD_PERIOD, sentinal).start()

    if not settings.HEROKU_API_KEY:
        logging.error("Please specify HEROKU_API_KEY in the environment. Exiting Dyno Monitor")
        sys.exit(0)

    try:
        # List all seperate log sources and create a thread for each
        for logsrc in list(settings.RULES.keys()):
            start_thread(logsrc)

    except KeyboardInterrupt:
        eprint('\nExiting by user request.\n')
    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)
