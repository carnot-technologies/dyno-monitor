import logging
from django.conf import settings


def parse(line, app_name, source, dyno):

    # Validate if the line matches the source and dyno
    if source not in line or dyno not in line:
        return

    root = app_name + settings.SEPERATOR + source + settings.SEPERATOR + dyno
    if root not in settings.RULES:
        return

    # Find all rule filters to be applied
    for rule, rule_properties in settings.RULES[root].items():
        if rule_properties['search_key'] in line:

            # Detected.
            logging.warning("Detected: {}".format(rule_properties['search_key']))

            # TODO: Log in the raw log DB

            alarm = False
            # TODO: Query DB and check if count and timestamp condition match.
            # If it matches, set the alarm

            if alarm and rule_properties['email_alert']:
                # Check last email sent time and send condition
                pass

            if alarm and rule_properties['action']:
                # Check last action performed time and action condition
                pass
