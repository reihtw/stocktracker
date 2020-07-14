from django.db import models

# Create your models here.

class Papel(models.Model):
    codigo_acao = models.CharField(max_length=8)
    data_atualizacao = models.DateTimeField()
    preco_atual = models.FloatField()
    tipo = models.CharField(max_length=5)
    historico_completo = models.BooleanField(default=False)

    def __str__(self):
        return self.codigo_acao