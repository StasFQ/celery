import datetime

from celery import shared_task
from django.core.mail import send_mail as django_send_mail

from celery_hm.celery import app


@shared_task()
def send_mail(time, message, email):
        django_send_mail(time, email, 'admin@example.com', [message])
