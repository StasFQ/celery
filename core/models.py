from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)


class Quote(models.Model):
    quote = models.CharField(max_length=254)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
