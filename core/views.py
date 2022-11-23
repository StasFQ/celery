import datetime

from datetime import timedelta
from django.shortcuts import render, redirect
from .forms import MainForm
from . import tasks
from django.utils import timezone


def contact_form(request):
    form = MainForm()
    if request.method == "POST":
        form = MainForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['time']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            if time < (timezone.now() + datetime.timedelta(days=2)):
                tasks.send_mail.apply_async((time, email, message), eta=time)
            return redirect('core:contact_form')
    return render(request, 'contact.html', {'form': form})
