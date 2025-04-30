from common_imports import *

def first_time_check(self):
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    delay = (next_minute - now).total_seconds()

    Clock.schedule_once(lambda dt: self.start_minute_interval(), delay)

def start_minute_interval(self):
    self.check_reminders(0)
    Clock.schedule_interval(self.check_reminders, 60)