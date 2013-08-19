from celery.task.base import task

@task(queue="scheduling")
def schedule_tweet(chan_id):
    print "ola %s ke ase?" % chan_id