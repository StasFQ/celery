from django.urls import path
from .views import contact_form

app_name = 'core'
urlpatterns = [
    path('', contact_form, name='contact_form')
]
