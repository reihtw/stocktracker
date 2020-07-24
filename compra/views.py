from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from datetime import date

from .models import Compra
from corretora.models import Corretora
from papel.models import Papel
from negociacoes.models import Negociacoes
from venda.models import Venda

from papel.views import atualizar_preco_dev
from negociacoes.taxas import Taxas

# Create your views here.

def registrar_compra(request):
    if request.method == 'POST':
        codigo_acao = request.POST['codigo_acao']
        nome_corretora = request.POST['nome_corretora']
        try:
            quantidade = int(request.POST['quantidade'])
        except:
            messages.error(request, 'Quantidade inválida!')
            return redirect('registrar_compra_papel', codigo_acao)
        data_compra = date.fromisoformat(request.POST['data_compra'])
        try:
            preco_unitario = float(request.POST['preco_unitario'])
        except:
            messages.error(request, 'Preço inválido!')
            return redirect('registrar_compra_papel', codigo_acao)    
        
        preco_total = quantidade * preco_unitario

        usuario = User.objects.get(pk=request.user.id)
        papel = atualizar_preco_dev(codigo_acao=codigo_acao)

        taxas = Taxas.calcula_taxas(preco_total, papel, nome_corretora, quantidade)
        preco_total += taxas

        compra = Compra.objects.create(
            usuario=usuario,
            papel=papel,
            quantidade=quantidade,
            data_compra=data_compra,
            preco_unitario=preco_unitario,
            taxas=taxas,
            preco_total=preco_total
        )
        compra.save()

        if Negociacoes.objects.filter(papel=papel, usuario=usuario):
            negociacao = Negociacoes.objects.get(papel=papel, usuario=usuario)
            compras = Compra.objects.filter(papel=papel, usuario=usuario)
            
            preco = 0
            taxas = 0
            for compra in compras:
                preco += compra.preco_unitario
                taxas += compra.taxas

            negociacao.quantidade += quantidade
            negociacao.preco_medio_unitario = preco/len(compras)
            negociacao.preco_medio_total =  negociacao.preco_medio_unitario * negociacao.quantidade + taxas
            if data_compra > negociacao.ultima_data_compra:
                negociacao.ultima_data_compra = data_compra
            negociacao.resultado = papel.preco_atual * negociacao.quantidade - negociacao.preco_medio_total
            negociacao.resultado_porcentagem = negociacao.resultado / negociacao.preco_medio_total * 100

            negociacao.save()
        else:
            resultado = papel.preco_atual * quantidade - preco_total
            resultado_porcentagem = resultado / preco_total * 100
            negociacao = Negociacoes.objects.create(
                usuario=usuario,
                papel=papel,
                quantidade=quantidade,
                preco_medio_unitario=preco_unitario,
                preco_medio_total=preco_total,
                ultima_data_compra=data_compra,
                resultado_porcentagem=resultado_porcentagem,
                resultado=resultado
            )

            negociacao.save()
        
        return redirect('visualizar_negociacoes')
    
    corretoras = Corretora.objects.all()
    papeis = Papel.objects.all()

    dados = {
        'corretoras': corretoras,
        'papeis' : papeis,
        'data' : date.today().strftime("%Y-%m-%d"),
        'codigo_acao' : ''
    }

    return render(request, 'compra/registrar_compra.html', dados)

def registrar_compra_papel(request, codigo_acao):
    corretoras = Corretora.objects.all()
    papeis = Papel.objects.all()

    dados = {
        'corretoras': corretoras,
        'papeis' : papeis,
        'data' : date.today().strftime("%Y-%m-%d"),
        'codigo_acao' : codigo_acao
    }

    return render(request, 'compra/registrar_compra.html', dados)

def excluir_compra(request, compra_id):
    usuario = User.objects.get(pk=request.user.id)
    compra = Compra.objects.get(pk=compra_id, usuario=usuario)
    vendas = Venda.objects.order_by('-data_venda').filter(papel=compra.papel, usuario=usuario)
    if vendas:
        if vendas[0].data_venda > compra.data_compra:
            messages.error(request, 'Para excluir essa compra, é necessário excluir as vendas feitas depois dela.')
            return redirect('negociacoes_papel', compra.papel.codigo_acao)
    
    compra.delete()

    papel = Papel.objects.get(codigo_acao=compra.papel.codigo_acao)
    negociacao = Negociacoes.objects.get(usuario=usuario, papel=papel)
    compras = Compra.objects.order_by('-data_compra').filter(papel=papel, usuario=usuario)

    if not compras:
        negociacao.delete()
        return redirect('visualizar_negociacoes')
    
    negociacao.quantidade -= compra.quantidade
    if compra.data_compra > compras[0].data_compra:
        negociacao.ultima_data_compra = compras[0].data_compra
    
    preco = 0
    taxas = 0
    for compra in compras:
        preco += compra.preco_unitario
        taxas += compra.taxas
    negociacao.preco_medio_unitario = preco/len(compras)
    negociacao.preco_medio_total =  negociacao.preco_medio_unitario * negociacao.quantidade + taxas
    negociacao.resultado = papel.preco_atual * negociacao.quantidade - negociacao.preco_medio_total
    negociacao.resultado_porcentagem = negociacao.resultado / negociacao.preco_medio_total * 100

    negociacao.save()
    return redirect('negociacoes_papel', compra.papel.codigo_acao)