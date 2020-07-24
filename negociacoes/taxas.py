from corretora.models import Corretora
from papel.models import Papel

class Taxas:
    TAXA_NEGOCIACAO = 0.004972/100
    TAXA_LIQUIDACAO = 0.0275/100

    @staticmethod
    def calcula_taxas(preco_total, papel, nome_corretora, quantidade):
        taxas = Taxas.TAXA_LIQUIDACAO * preco_total + Taxas.TAXA_NEGOCIACAO * preco_total
        corretora = Corretora.objects.get(nome=nome_corretora)
        if papel.tipo == 'Ação':
            if int(quantidade) % 100 != 0 or papel.codigo_acao[:-1] == 'F':
                taxas += corretora.taxa_acoes_fracionario
            else:
                taxas += corretora.taxa_acoes
        elif papel.tipo == 'FII':
            taxas += corretora.taxa_fiis
        elif papel.tipo == 'ETF':
            taxas += corretora.taxa_etfs
        return taxas