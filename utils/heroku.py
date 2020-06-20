import heroku3
import settings
import logging


class HerokuInterface(object):
    instance = None
    apps = None

    def __init__(self):
        if HerokuInterface.instance is not None:
            # raise ValueError("An instance already exists!")
            # print("Heroku interface already exists ...")
            return

        if not settings.HEROKU_API_KEY:
            logging.error("Please specify HEROKU_API_KEY in the environment")

        HerokuInterface.instance = heroku3.from_key(settings.HEROKU_API_KEY)
        HerokuInterface.apps = HerokuInterface.instance.apps(order_by='name')
        logging.warning("Heroku interface initiated ...")
        return

    def get_instance(self):
        if HerokuInterface.instance is None:
            HerokuInterface()
        return HerokuInterface.instance

    def get_apps(self):
        if HerokuInterface.instance is None:
            HerokuInterface()
        return HerokuInterface.apps

    def get_app(self, app_name):
        return self.get_apps()[app_name]

    def get_apps_list(self):
        return [app.name for app in self.get_apps()]

    def get_dynos_list(self, app_name):
        return [dyno.type for dyno in self.get_app(app_name).process_formation()]

    def get_current_dyno_count(self, app_name, dyno_type):
        dynos = self.get_apps()[app_name].dynos()
        return len(dynos[dyno_type]) if dyno_type in dynos else 0

    def scale_dynos(self, app_name, dyno_type, count):
        self.get_apps()[app_name].process_formation()[dyno_type].scale(count)
        return count

    def restart_app(self, app_name):
        self.get_apps()[app_name].restart()

    def restart_dynos(self, app_name, dyno_type):
        for dyno in self.get_apps()[app_name].dynos()[dyno_type]:
            dyno.restart()

    def stream_log(self, app_name, source, dyno, timeout):
        return self.get_app(app_name).stream_log(source=source, dyno=dyno, timeout=timeout)
