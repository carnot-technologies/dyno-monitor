from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import post_delete


class RulesConfig(AppConfig):
    name = 'rules'

    def ready(self):

        from utils.rule_helper import fetch_rules
        fetch_rules()

        from .signals import pre_rule_save
        from .signals import post_rule_save
        from .signals import post_rule_delete

        pre_save.connect(pre_rule_save, sender=self.get_model('HError'), weak=False, dispatch_uid="pre_hrule_save")
        pre_save.connect(pre_rule_save, sender=self.get_model('RError'), weak=False, dispatch_uid="pre_rrule_save")

        post_save.connect(post_rule_save, sender=self.get_model('HError'), weak=False, dispatch_uid="post_hrule_save")
        post_save.connect(post_rule_save, sender=self.get_model('RError'), weak=False, dispatch_uid="post_rrule_save")

        post_delete.connect(post_rule_delete, sender=self.get_model('HError'), weak=False, dispatch_uid="post_hrule_delete")
        post_delete.connect(post_rule_delete, sender=self.get_model('RError'), weak=False, dispatch_uid="post_rrule_delete")
