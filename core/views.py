import datetime

from django.shortcuts import render, redirect
from .forms import MainForm
from . import tasks


def contact_form(request):
    form = MainForm()
    if request.method == "POST":
        form = MainForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['time']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            tasks.send_mail.apply_async((time, email, message), eta=time)
            return redirect('core:contact_form')
    return render(request, 'contact.html', {'form': form})
