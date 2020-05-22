import sys
import time
import logging
import threading
import traceback
import load_django
from django.conf import settings

from utils.heroku import HerokuInterface
from utils.parser import parse


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def sentinal():
    logging.info("Sentinal thread run. Total thread count: {}".format(len(threading.enumerate())))
    logging.debug(threading.enumerate())
    threading.Timer(settings.SENTINAL_THREAD_PERIOD, sentinal).start()


def stream_logs(app_name, source, dyno):
    while True:
        # Main Thread Loop
        try:
            for line in HerokuInterface().stream_log(app_name=app_name, source=source, dyno=dyno, timeout=100):
                # Search for the required keywords in this line
                # logging.debug(line.decode('utf-8'))
                parse(line.decode('utf-8'), app_name, source, dyno)

        except Exception:
            logging.error(traceback.format_exc())
            # TODO: Handle specific exceptions here
            # Cooling period in case of errors
            time.sleep(1)


if __name__ == '__main__':

    logging.info("Starting Dyno Monitor " + settings.ENVIRONMENT)
    threading.Timer(settings.SENTINAL_THREAD_PERIOD, sentinal).start()

    try:
        # List all seperate log sources and create a thread for each
        for logsrc in list(settings.RULES.keys()):
            parts = logsrc.split(settings.SEPERATOR)

            if len(parts) != 3:
                logging.error("Invalid Rule: {}".format(logsrc))
                continue

            t = threading.Thread(target=stream_logs, args=(parts[0], parts[1], parts[2]))
            t.start()
            logging.info("Started log thread: {}".format(logsrc))

    except KeyboardInterrupt:
        eprint('\nExiting by user request.\n')
    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)
