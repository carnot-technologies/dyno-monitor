from django.apps import AppConfig


class RulesConfig(AppConfig):
    name = 'rules'

    def ready(self):
        from utils.rule_helper import build_rules
        build_rules()
