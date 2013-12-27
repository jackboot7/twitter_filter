import datetime
import re
from celery._state import current_task
from celery import current_app as app
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
            current_task.apply_async(eta)
            pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def can_execute_now(self):
        return True

    def calculate_eta(self):
        eta = datetime.datetime.now()
        return eta


def get_active_tasks():
    i = app.control.inspect()
    return i.active()


def channel_is_streaming(screen_name, exclude_id=None):
    active_tasks = get_active_tasks()
    regex = re.compile("(u'(?P<name>\w+)',)")
    if active_tasks is not None:
        for worker_id in active_tasks:
            if active_tasks[worker_id] is not None:
                for task in active_tasks[worker_id]:
                    if task['name'] == "apps.filtering.tasks.stream_channel":
                        print task['id']
                        r = regex.search(task['args'])
                        if r is not None and r.group('name') == screen_name and task['id'] != exclude_id:
                            return True
    return False


def get_streaming_task_id(screen_name, exclude_id=None):
    active_tasks = get_active_tasks()
    regex = re.compile("(u'(?P<name>\w+)',)")
    if active_tasks is not None:
        for worker_id in active_tasks:
            if active_tasks[worker_id] is not None:
                for task in active_tasks[worker_id]:
                    if task['name'] == "apps.filtering.tasks.stream_channel":
                        r = regex.search(task['args'])
                        if r is not None and r.group('name') == screen_name and task['id'] != exclude_id:
                            return task['id']
    return None
