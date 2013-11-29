from celery import task
from django.core.mail import send_mail


@task(queue="notifications", ignore_result=True)
def send_mail_notification(notif, subject, extra):
    send_mail(subject, "%s\n%s" % (notif.description, extra), 'traffic.testing24@gmail.com',
        ['traffic.testing24@gmail.com'], fail_silently=False)