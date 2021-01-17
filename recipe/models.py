from django.db import models


class Recipes(models.Model):

    name = models.CharField(max_length=30)
    path = models.CharField(max_length=30)
    ingr = models.CharField(max_length=200)

    class Meta:
        db_table = "RECIPES"
