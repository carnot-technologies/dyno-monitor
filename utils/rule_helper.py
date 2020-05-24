import logging
from django.conf import settings
from rules.models import HError
from rules.models import RError
from dynos.models import App
from dynos.models import Dyno
from utils.heroku import HerokuInterface
from utils.cacher import Cacher


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
    settings.RULES.clear()

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


def fetch_rules():
    logging.info("Fetching Rules")
    settings.RULES = Cacher().get_rules()
    if not settings.RULES:
        # If no rules found in cache, try rebuilding from the database
        build_rules()
        Cacher().set_rules(settings.RULES)


def update_rule(rule):
    """
    `rule` is an instance of HError or RError rule objects
    Update the local rules dictionary in settings and then update in redis
    """
    root = rule.dyno_fk.app_fk.name + settings.SEPERATOR + rule.log_source + settings.SEPERATOR + rule.log_dyno
    logging.warning("Reloading Rule: {}:{}".format(root, rule.category))

    if root not in settings.RULES:
        settings.RULES[root] = {}
    settings.RULES[root][rule.category] = rule.export_dict()

    Cacher().set_rules(settings.RULES)


def delete_rule(rule):
    """
    `rule` is an instance of HError or RError rule objects
    Delete the rule from local rules dictionary in settings
    Then update it in redis
    """
    root = rule.dyno_fk.app_fk.name + settings.SEPERATOR + rule.log_source + settings.SEPERATOR + rule.log_dyno
    if root in settings.RULES:
        if rule.category in settings.RULES[root]:
            del settings.RULES[root][rule.category]
            if not settings.RULES[root]:
                del settings.RULES[root]
            Cacher().set_rules(settings.RULES)


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
