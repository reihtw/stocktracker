from django.db import models
from django.contrib.auth.models import User

from papel.models import Papel

# Create your models here.

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_acao =  models.ForeignKey(Papel, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_compra = models.DateField()
    preco_unitario = models.FloatField()
    taxas = models.FloatField()
    preco_total = models.FloatField()

    def __str__(self):
        
        return f'{self.codigo_acao}, {self.quantidade}, {self.preco_unitario}, {self.data_compra}'