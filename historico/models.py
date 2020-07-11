from django.db import models

from papel.models import Papel

# Create your models here.

class Historico(models.Model):
    codigo_acao = models.ForeignKey(Papel, on_delete=models.CASCADE)
    dia = models.DateField()
    abertura = models.FloatField()
    fechamento = models.FloatField()
    maximo = models.FloatField()
    minimo = models.FloatField()
    media = models.FloatField()

    def __str__(self):
        return f'{self.codigo_acao}, {self.dia}, {self.abertura}, {self.fechamento}, {self.maximo}, {self.minimo}, {self.media}'