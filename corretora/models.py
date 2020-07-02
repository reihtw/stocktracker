from django.db import models

# Create your models here.

class Corretora(models.Model):
    nome = models.CharField(max_length=100)
    taxa_acoes = models.FloatField()
    taxa_fiis = models.FloatField()
    taxa_etfs = models.FloatField()

    def __str__(self):
        return self.nome