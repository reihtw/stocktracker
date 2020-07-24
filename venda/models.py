from django.db import models
from django.contrib.auth.models import User

from papel.models import Papel

# Create your models here.

class Venda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    papel = models.ForeignKey(Papel, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_venda = models.DateField()
    preco_unitario = models.FloatField()
    taxas = models.FloatField()
    preco_total = models.FloatField()
    lucro = models.FloatField()