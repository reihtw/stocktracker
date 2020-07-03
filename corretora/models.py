from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Corretora(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    taxa_acoes = models.FloatField()
    taxa_acoes_fracionario = models.FloatField()
    taxa_fiis = models.FloatField()
    taxa_etfs = models.FloatField()

    def __str__(self):
        return self.nome