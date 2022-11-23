import datetime
import requests
from celery import shared_task
from django.core.mail import send_mail as django_send_mail
from bs4 import BeautifulSoup

from celery_hm.celery import app
from core.models import Author, Quote


@shared_task()
def send_mail(time, message, email):
    django_send_mail(time, email, 'admin@example.com', [message])


@shared_task()
def parser():
    flag = True
    url = 'https://quotes.toscrape.com'
    suffix = ''
    while flag:
        responce = requests.get(url + suffix)
        soup = BeautifulSoup(responce.text, 'html.parser')
        quote_l = soup.find_all('span', {'class': 'text'})
        q_count = 0
        for i in range(len(quote_l)):
            quote = soup.find_all('span', {'class': 'text'})[i]
            if not Quote.objects.filter(quote=quote.string).exists():
                if q_count >= 5:
                    flag = False
                    break
                author = soup.find_all('small', {'class': 'author'})[i]
                if not Author.objects.filter(name=author.string).exists():
                    a = Author.objects.create(name=author.string)
                    Quote.objects.create(quote=quote.string, author_id=a.id)
                    q_count += 1
                else:
                    a = Author.objects.get(name=author.string)
                    Quote.objects.create(quote=quote.string, author_id=a.id)
                    q_count += 1
                if q_count >= 5:
                    flag = False
                    break

        next_page = soup.find('li', {'class': 'next'})
        if not next_page:
            flag = False
            break
        suffix = next_page.a['href']
