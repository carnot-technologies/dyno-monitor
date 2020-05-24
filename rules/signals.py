from .models import HError
from .models import RError
from utils.rule_helper import update_rule
from utils.rule_helper import delete_rule


def pre_rule_save(sender, instance, **kwargs):

    if sender == HError:
        # The following settings are required, but they are present in the instance by default.
        # instance.log_source = 'heroku' # present by default
        # instance.log_dyno = 'router' # present by default
        # Nothing to be done
        pass

    elif sender == RError:
        # instance.log_source = 'heroku' # present by default
        instance.log_dyno = instance.dyno_fk.name


def post_rule_save(sender, instance, **kwargs):
    update_rule(instance)


def post_rule_delete(sender, instance, **kwargs):
    delete_rule(instance)
