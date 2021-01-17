from django.db import models


class Shelf(models.Model):

    name = models.CharField(max_length=30)
    qty = models.IntegerField()

    class Meta:
        db_table = "SHELF"
