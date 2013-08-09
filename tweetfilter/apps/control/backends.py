from celery._state import current_task
from celery.task.base import Task
import datetime

class DelayedTask(Task):
    """
    Defines a type of task that can only be executed if can_execute_now() returns True for some given condition
    Subclasses should implement their own conditions, as well as the method calculate_eta that returns the datetime
    until next execution.
    """
    class Meta:
        abstract = True

    def __call__(self, *args, **kwargs):

        if self.can_execute_now():
            return self.run(*args, **kwargs)
        else:
            # calculates nearest ETA and delay self
            eta = self.calculate_eta()
            current_task.apply_async(eta)
            pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print "DelayedTask %s ended with status %s" % (task_id, status)
        pass

    def can_execute_now(self):
        return True

    def calculate_eta(self):
        eta = datetime.datetime.now()
        return eta

