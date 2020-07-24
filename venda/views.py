from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from datetime import date

from .models import Venda
from compra.models import Compra
from corretora.models import Corretora
from papel.models import Papel
from negociacoes.models import Negociacoes

from papel.views import atualizar_preco_dev
from negociacoes.taxas import Taxas


# Create your views here.

def registrar_venda(request, codigo_acao):
    if request.method == 'POST':
        nome_corretora = request.POST['nome_corretora']
        try:
            quantidade = int(request.POST['quantidade'])
        except:
            messages.error(request, 'Quantidade inválida!')
            return redirect('registrar_venda', codigo_acao)
        data_venda = date.fromisoformat(request.POST['data_venda'])
        try:
            preco_unitario = float(request.POST['preco_unitario'].replace(',','.'))
        except:
            messages.error(request, 'Preço inválido!')
            return redirect('registrar_venda', codigo_acao)
        
        usuario = User.objects.get(pk=request.user.id)
        papel = atualizar_preco_dev(codigo_acao=codigo_acao)
        negociacao = Negociacoes.objects.get(papel=papel, usuario=usuario)
        
        negociacao_quantidade = negociacao.quantidade
        if data_venda < date.today():
            negociacao_quantidade = 0
            compras = Compra.objects.filter(papel=papel, usuario=usuario)
            for compra in compras:
                if compra.data_compra > data_venda:
                    break
                negociacao_quantidade += compra.quantidade


        if quantidade > negociacao_quantidade:
            messages.error(request, 'Quantidade de venda é maior que a quantidade comprada até a data escolhida')
            return redirect('registrar_venda', codigo_acao)

        preco_total = quantidade * preco_unitario
        taxas = Taxas.calcula_taxas(preco_total, papel, nome_corretora, quantidade)
        preco_total += taxas

        lucro = ((papel.preco_atual - negociacao.preco_medio_unitario) * quantidade) - taxas

        venda = Venda.objects.create(
            usuario=usuario,
            papel=papel,
            quantidade=quantidade,
            data_venda=data_venda,
            preco_unitario=preco_unitario,
            taxas=taxas,
            preco_total=preco_total,
            lucro=lucro
        )

        venda.save()

        compras = Compra.objects.filter(papel=papel, usuario=usuario)

        taxas = 0
        for compra in compras:
            taxas += compra.taxas

        negociacao.quantidade -= venda.quantidade
        if negociacao.quantidade == 0:
            negociacao.preco_medio_unitario = 0
            negociacao.preco_medio_total = 0
        else:
            negociacao.preco_medio_total = negociacao.preco_medio_unitario * negociacao.quantidade + taxas
        negociacao.save()

        return redirect('negociacoes_papel', codigo_acao)
    
    corretoras = Corretora.objects.all()
    papel = Papel.objects.get(codigo_acao=codigo_acao)

    dados = {
        'corretoras': corretoras,
        'papel' : papel,
        'data' : date.today().strftime("%Y-%m-%d"),
    }

    return render(request, 'venda/registrar_venda.html', dados)

def excluir_venda(request, venda_id):
    usuario = User.objects.get(pk=request.user.id)
    venda = Venda.objects.get(pk=venda_id, usuario=usuario)
    negociacao = Negociacoes.objects.get(papel=venda.papel, usuario=usuario)

    compras = Compra.objects.filter(papel=venda.papel, usuario=usuario)
    preco_total_compra = 0
    for compra in compras:
        preco_total_compra += compra.preco_total

    negociacao.quantidade += venda.quantidade
    negociacao.preco_medio_total = preco_total_compra
    negociacao.save()
    venda.delete()
    return redirect('negociacoes_papel', negociacao.papel.codigo_acao)