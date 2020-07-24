from django.db import models
from django.contrib.auth.models import User

from papel.models import Papel
from compra.models import Compra

# Create your models here.

class Negociacoes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    papel = models.ForeignKey(Papel, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_medio_unitario = models.FloatField()
    preco_medio_total = models.FloatField()
    ultima_data_compra = models.DateField()
    resultado_porcentagem = models.FloatField()
    resultado  = models.FloatField()

    def __str__(self):
        return f'{self.usuario}, {self.compra}, {self.quantidade}, {self.preco_medio}, {self.ultima_data_compra}'
