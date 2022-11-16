import datetime

from django import forms


class MainForm(forms.Form):
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    time = forms.DateTimeField(initial=datetime.datetime.now())
