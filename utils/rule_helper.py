import logging
from django.conf import settings
from rules.models import HError
from rules.models import RError


def build_rules():
    """
    This function is run once at startup to construct the RULES dictionary in settings
    It specifies:
    1. Which log filter to source data from (using app name, log source and log dyno name)
    2. Which rules to apply for a particular log filter
    3. Properties of each rule
    """
    logging.warning("Building Rules.")
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
