from django.conf import settings
from django.db import models

class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    preis = models.DecimalField(max_digits=6, decimal_places=2)
    beschreibung = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "produkte"
        verbose_name = "Produkt"
        verbose_name_plural = "Produkte"

    def __str__(self):
        return self.name

