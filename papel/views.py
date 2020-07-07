import requests

from bs4 import BeautifulSoup
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import auth, messages

from . import tipo_papel
from .models import Papel

# Create your views here.


def cadastro_papel(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        codigo = request.POST['codigo']
        preco = pega_preco_atual(codigo)
        data_atualizacao = datetime.now()
        tipo = request.POST['tipo']

        if preco == None:
            messages.error(request, 'Código inválido!')
            return redirect('cadastro_papel')
        
        if Papel.objects.filter(codigo_acao=codigo).exists():
            messages.error(request, 'Papel já cadastrado')
            return redirect('cadastro_papel')

        papel = Papel(codigo_acao=codigo, data_atualizacao=data_atualizacao, preco_atual=preco, tipo=tipo)
        papel.save()
        messages.success(request, f'Papel cadastrado com sucesso!')
        return redirect('papeis')

    dados ={
        'tipos': tipo_papel.tipo
    }

    return render(request, 'papel/cadastro_papel.html', dados)


def papeis(request):
    if not request.user.is_authenticated:
        return redirect('home')

    papeis = Papel.objects.order_by('codigo_acao')

    dados = {
        'papeis' : papeis
    }

    return render(request, 'papel/papeis.html', dados)

def procurar_papeis(request):
    if not request.user.is_authenticated:
        return redirect('home')

    papeis = Papel.objects.order_by('codigo_acao')
    if request.method == 'POST':
        codigo_a_procurar = request.POST['data[search]']
        if codigo_a_procurar:
            papeis = papeis.filter(codigo_acao__icontains=codigo_a_procurar)
    
    dados = {
        'papeis': papeis
    }

    return render(request, 'papel/papeis.html', dados)

def atualizar_precos(request):
    if not request.user.is_authenticated:
        return redirect('home')

    papeis = Papel.objects.order_by('codigo_acao')

    for papel in papeis:
        codigo = papel.codigo_acao
        papel.preco_atual = pega_preco_atual(codigo)
        papel.data_atualizacao = datetime.now()
        papel.save()
    
    dados = {
        'papeis': papeis
    }

    return render(request, 'papel/papeis.html', dados)

def pega_preco_atual(codigo):
    pagina = requests.get(f'https://finance.yahoo.com/quote/{codigo}.SA')
    soup = BeautifulSoup(pagina.content, 'html.parser')
    preco = soup.find('span', {'class':'Trsdu(0.3s)','data-reactid':'31'})
    if preco == None:
        return None
    return float(preco.string.split(' ')[0])
