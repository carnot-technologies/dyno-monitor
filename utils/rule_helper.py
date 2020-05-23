import logging
from django.conf import settings
from rules.models import HError
from rules.models import RError
from dynos.models import App
from dynos.models import Dyno
from utils.heroku import HerokuInterface


def db_table_exists(table_name):
    from django.db import connection
    return table_name in connection.introspection.table_names()


def build_rules():
    """
    This function is run once at startup to construct the RULES dictionary in settings
    It specifies:
    1. Which log filter to source data from (using app name, log source and log dyno name)
    2. Which rules to apply for a particular log filter
    3. Properties of each rule
    """
    if not db_table_exists(HError._meta.db_table):
        return

    logging.warning("Building Rules")
    hrules = HError.objects.all()
    for hrule in hrules:
        root = hrule.dyno_fk.app_fk.name + settings.SEPERATOR + hrule.log_source + settings.SEPERATOR + hrule.log_dyno
        if root not in settings.RULES:
            settings.RULES[root] = {}

        settings.RULES[root][hrule.category] = hrule.export_dict()

    rrules = RError.objects.all()
    for rrule in rrules:
        root = rrule.dyno_fk.app_fk.name + settings.SEPERATOR + rrule.log_source + settings.SEPERATOR + rrule.log_dyno
        if root not in settings.RULES:
            settings.RULES[root] = {}

        settings.RULES[root][rrule.category] = rrule.export_dict()


def auto_detect_heroku_apps():
    if not settings.HEROKU_API_KEY:
        logging.error("Please specify HEROKU_API_KEY in the environment. Cannot auto detect apps")
        return

    for app in HerokuInterface().get_apps():
        logging.info("Found app: {}".format(app.name))
        a, created = App.objects.update_or_create(name=app.name, defaults={'url': app.web_url})
        for dyno in HerokuInterface().get_dynos_list(app.name):
            logging.info("Found dyno: {}:{}".format(app.name, dyno))
            cnt = HerokuInterface().get_current_dyno_count(app.name, dyno)
            d, created = Dyno.objects.update_or_create(app_fk=a, name=dyno, defaults={'cnt': cnt})
