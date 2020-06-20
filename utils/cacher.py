import time
import json
import redis
import logging
import settings


class Cacher(object):
    """
    Cache schema:
    Hash Maps

    <app_name>
        "restart-app": 102938550

    <app_name>:<dyno_name>
        "restart-dyno": 120938102

    <app_name>:<dyno_name>:<error_cat>
        "last-email": 1982309888
    """

    instance = None
    SEPERATOR = ':'

    def __init__(self):
        if Cacher.instance is not None:
            return

        Cacher.instance = redis.from_url(settings.CACHE_REDIS_URL, decode_responses=True)
        logging.warning("Redis cache connection initiated ...")
        return

    def get_instance(self):
        if Cacher.instance is None:
            Cacher()

        return Cacher.instance

    def get_last_action_time(self, action, app_name, dyno_name=None):
        topic = app_name
        topic += (self.SEPERATOR + dyno_name) if dyno_name else ""
        val = self.get_instance().hget(topic, action)
        return int(val) if val else 0

    def set_last_action_time(self, action, app_name, dyno_name=None):
        topic = app_name
        topic += (self.SEPERATOR + dyno_name) if dyno_name else ""
        return self.get_instance().hset(topic, action, int(time.time()))

    def get_last_email_time(self, app_name, dyno_name, category):
        topic = app_name + self.SEPERATOR + dyno_name + self.SEPERATOR + category
        val = self.get_instance().hget(topic, 'last-email')
        return int(val) if val else 0

    def set_last_email_time(self, app_name, dyno_name, category):
        topic = app_name + self.SEPERATOR + dyno_name + self.SEPERATOR + category
        return self.get_instance().hset(topic, 'last-email', int(time.time()))

    def get_rules(self):
        rules = self.get_instance().get('rules')
        return json.loads(rules) if rules else {}

    def set_rules(self, rules):
        return self.get_instance().set('rules', json.dumps(rules))
