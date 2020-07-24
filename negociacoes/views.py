from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Negociacoes
from compra.models import Compra
from papel.models import Papel
from venda.models import Venda

from papel.views import pega_preco_atual, atualizar_preco_dev, atualizar_precos_dev

# Create your views here.

def visualizar_negociacoes(request):
    negociacoes = Negociacoes.objects.all()

    dados = {
        'negociacoes' : negociacoes
    }

    return render(request, 'negociacoes/visualizar_negociacoes.html', dados)

def atualizar_resultados(request):
    negociacoes = Negociacoes.objects.all()
    papeis = [negociacao.papel for negociacao in negociacoes]
    atualizar_precos_dev(papeis)

    for negociacao in negociacoes:
        if negociacao.quantidade == 0:
            negociacao.resultado = 0
            negociacao.resultado_porcentagem = 0
        else:
            negociacao.resultado = negociacao.papel.preco_atual * negociacao.quantidade - negociacao.preco_medio_total
            negociacao.resultado_porcentagem = negociacao.resultado / negociacao.preco_medio_total * 100

        negociacao.save()
    
    return redirect('visualizar_negociacoes')

def atualizar_resultado(request, codigo_acao):
    usuario = User.objects.get(pk=request.user.id)
    papel = atualizar_preco_dev(codigo_acao)
    negociacao = Negociacoes.objects.get(papel=papel, usuario=usuario)
    if negociacao.quantidade == 0:
        negociacao.resultado = 0
        negociacao.resultado_porcentagem = 0
    else:
        negociacao.resultado = negociacao.papel.preco_atual * negociacao.quantidade - negociacao.preco_medio_total
        negociacao.resultado_porcentagem = negociacao.resultado / negociacao.preco_medio_total * 100
    negociacao.save()
    
    return redirect('negociacoes_papel', codigo_acao)

def negociacoes_papel(request, codigo_acao):
    usuario = User.objects.get(pk=request.user.id)
    papel = Papel.objects.get(codigo_acao=codigo_acao)
    negociacao = Negociacoes.objects.get(papel=papel, usuario=usuario)
    compras = Compra.objects.order_by('-data_compra').filter(papel=papel, usuario=usuario)
    vendas = Venda.objects.order_by('-data_venda').filter(papel=papel, usuario=usuario)

    dados = {
        'papel': papel,
        'negociacao': negociacao,
        'compras' : compras,
        'vendas' : vendas,
        'valor_atual' : negociacao.quantidade * papel.preco_atual
    }

    return render(request, 'negociacoes/negociacoes_papel.html', dados)
