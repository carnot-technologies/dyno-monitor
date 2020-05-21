import sys
import logging
import threading
import traceback
import settings

from utils.heroku import HerokuInterface


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def sentinal():
    logging.info("Sentinal thread running...")
    logging.debug(threading.enumerate())
    threading.Timer(settings.SENTINAL_THREAD_PERIOD, sentinal).start()


if __name__ == '__main__':

    logging.info("Starting Dyno Monitor " + settings.ENVIRONMENT)
    threading.Timer(settings.SENTINAL_THREAD_PERIOD, sentinal).start()

    try:
        while True:
            # Main Loop
            try:
                for line in HerokuInterface().stream_log(app_name="traclytics", source="heroku", dyno="router", timeout=10):
                    # TODO: Search for the required keywords in this line
                    logging.debug(line.decode('utf-8'))

            except Exception:
                print(traceback.format_exc())
            # break

    except KeyboardInterrupt:
        eprint('\nExiting by user request.\n')
    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)
