from datetime import datetime

try:
    from croniter import croniter
except ImportError:
    croniter = None


class _Scheduler:

    def __init__(self):
        self.cron_pattern = None

    def every_hour(self) -> '_Scheduler':
        self.cron_pattern = '0 * * * *'
        return self

    def every_day(self) -> '_Scheduler':
        self.cron_pattern = '0 0 * * *'
        return self

    def every_minute(self) -> '_Scheduler':
        self.cron_pattern = '* * * * *'
        return self

    def cron(self, cron_pattern: str) -> '_Scheduler':
        self.cron_pattern = cron_pattern
        return self

    def is_due(self, now: datetime) -> bool:
        if croniter is None:
            raise ImportError('You need to install croniter to use scheduler')
        if self.cron_pattern is None:
            return False
        return croniter.match(self.cron_pattern, now)


class SchedulerMeta(type):
    def __getattr__(cls, name):
        def method_wrapper(*args, **kwargs):
            scheduler_instance = _Scheduler()
            getattr(scheduler_instance, name)(*args, **kwargs)
            return scheduler_instance

        return method_wrapper


class Scheduler(metaclass=SchedulerMeta):
    every_hour: _Scheduler.every_hour
    every_day: _Scheduler.every_day
    every_minute: _Scheduler.every_minute
    cron: _Scheduler.cron
