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

    papeis = atualizar_precos_dev()
    
    dados = {
        'papeis': papeis
    }

    return render(request, 'papel/papeis.html', dados)

def atualizar_precos_dev(papeis=''):
    if papeis == '':
        papeis = Papel.objects.all()

    for papel in papeis:
        papel = atualizar_preco_dev(papel=papel)
    
    return papeis

def atualizar_preco_dev(codigo_acao='', papel=''):
    if codigo_acao != '':
        papel = Papel.objects.get(codigo_acao=codigo_acao)
    papel.preco_atual = pega_preco_atual(papel.codigo_acao)
    papel.data_atualizacao = datetime.now()
    papel.save()
    return papel


def pega_preco_atual(codigo, tentativa=0):
    page = requests.get(f'https://finance.yahoo.com/quote/{codigo}.SA?p={codigo}.SA&.tsrc=fin-srch')
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(page.content)
    price = soup.find('div', {'class':'D(ib)','data-reactid':'31'})
    print(price)
    if price == None:
        if tentativa == 5:
            return None
        tentativa += 1
        return pega_preco_atual(codigo)
    price = price.find('span', {'data-reactid': '32'}).get_text()
    return float(price)
