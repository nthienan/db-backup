from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger


class Scheduler:
    def __init__(self):
        self._scheduler = BackgroundScheduler()

    def schedule(self, worker, triggers):
        for trigger_type, expr in triggers.items():
            trigger = None
            name = '%s#%s' % (trigger_type, worker.name)
            if trigger_type == 'cron':
                trigger = CronTrigger.from_crontab(expr)
            elif trigger_type == 'once':
                trigger = DateTrigger(expr)

            if trigger:
                self._scheduler.add_job(func=worker.work, trigger=trigger, name=name)

    def start(self):
        self._scheduler.start()

    def is_running(self):
        return self._scheduler.running

    def shutdown(self):
        self._scheduler.shutdown()
