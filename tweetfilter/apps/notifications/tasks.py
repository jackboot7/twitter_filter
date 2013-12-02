from celery import task
from django.conf import settings
from django.core.mail import send_mail


@task(queue="notifications", ignore_result=True)
def send_mail_notification(address, notif, subject, extra):
    send_mail(subject, "%s\n\n%s" % (notif.description, extra), settings.EMAIL_FROM,
        [address], fail_silently=False)