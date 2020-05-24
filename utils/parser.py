import time
import logging
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from logs.models import ErrorLog
from utils.mail import send_email
from utils.cacher import Cacher
from utils.heroku import HerokuInterface


def parse(line, app_name, source, dyno):
    """
    return: exit: boolean. If true, we can stop this parser thread
    """

    # Validate if the line matches the source and dyno
    if source not in line or dyno not in line:
        return False

    root = app_name + settings.SEPERATOR + source + settings.SEPERATOR + dyno
    if root not in settings.RULES:
        return True

    # Find all rule filters to be applied
    for rule, rule_properties in settings.RULES[root].items():
        if rule_properties['search_key'] in line:

            # Detected.
            logging.warning("Detected: {}".format(rule_properties['search_key']))

            # Log in the raw log table
            el = ErrorLog(app_fk_id=rule_properties['app'],
                          dyno_fk_id=rule_properties['dyno_fk_id'],
                          category=rule_properties['category'],
                          source=root,
                          time_stamp=now())
            el.save()

            # Query DB and check if count and timestamp condition match.
            if rule_properties['least_count'] <= 1 \
                    or ErrorLog.objects.filter(time_stamp__gte=now() - timedelta(seconds=rule_properties['time_window'])).count() >= rule_properties['least_count']:
                performed = perform_actions(rule_properties)
                notify(rule_properties, action_taken=performed)

    return False


def perform_actions(rp):
    if rp['action']:

        # Check last action performed time and action condition
        if rp['action'] == 'restart-app':
            lat = Cacher().get_last_action_time(rp['action'], rp['app'])

            if int(time.time()) - lat > settings.APP_RESTART_COOLING_PERIOD:
                # All okay to perform app restart.
                HerokuInterface().restart_app(rp['app'])
                logging.warning("Performing action: {} on {}".format(rp['action'], rp['app']))
                Cacher().set_last_action_time(rp['action'], rp['app'])
                return True

        elif rp['action'] == 'restart-dyno':
            lart = Cacher().get_last_action_time(rp['action'], rp['app'], dyno_name=rp['dyno'])
            ldrt = Cacher().get_last_action_time(rp['action'], rp['app'], dyno_name=rp['dyno'])

            if int(time.time()) - max(lart, ldrt) > settings.DYNO_RESTART_COOLING_PERIOD:
                # All okay to perform dyno restart.
                HerokuInterface().restart_dynos(rp['app'], rp['dyno'])
                logging.warning("Performing action: {} on {}:{}".format(rp['action'], rp['app'], rp['dyno']))
                Cacher().set_last_action_time(rp['action'], rp['app'], dyno_name=rp['dyno'])
                return True

    return False


def notify(rp, action_taken=False):
    if rp['email_alert']:

        # Check last email sent time and send condition
        let = Cacher().get_last_email_time(rp['app'], rp['dyno'], rp['category'])
        if int(time.time()) - let > settings.EMAIL_COOLING_PERIOD_PER_TOPIC:
            # Send email
            logging.warning("Sending email. Topic: {}:{}:{}".format(rp['app'], rp['dyno'], rp['category']))
            sub = "{} Error Detected in {}:{}".format(rp['category'], rp['app'], rp['dyno'])
            msg = "Atleast {} error(s) of type {} detected in the last {} seconds".format(rp['least_count'], rp['category'], rp['time_window'])
            msg += "Action taken: {}".format(rp['action']) if action_taken else ""
            send_email(sub, msg)
            Cacher().set_last_email_time(rp['app'], rp['dyno'], rp['category'])
            return True

    return False
