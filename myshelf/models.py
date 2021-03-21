from django.db import models
from django import forms


class Shelf(models.Model):

    name = models.CharField(max_length=30)
    qty = models.IntegerField()

    class Meta:
        db_table = "SHELF"


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = [
            'name',
            'qty'
        ]
