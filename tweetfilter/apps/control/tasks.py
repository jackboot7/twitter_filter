from celery._state import current_task, current_app
#from celery.task.base import Task
#from celery import Task
import datetime
from celery.app.task import Task

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
            current_task.apply_async(eta)   # retry?
            pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def can_execute_now(self):
        return True

    def calculate_eta(self):
        eta = datetime.datetime.now()
        return eta

# task(periodic,interval,blah)
def monitor_streaming_tasks():

    inspect = current_app.control.inspect()
    active_tasks = inspect.active()
    # para cada tarea de streaming de cada canal activo
        # tarea existe en active_tasks?
            #todobien
        # no?
            #activar streaming
    pass