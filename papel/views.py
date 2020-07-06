import requests

from bs4 import BeautifulSoup
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import auth, messages

from .models import Papel

# Create your views here.


def cadastro_papel(request):
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

        messages.success(request, f'Papel cadastrado com sucesso! {codigo} {preco} {data_atualizacao} {tipo}')
        return redirect('cadastro_papel')
    return render(request, 'papel/cadastro_papel.html')




def pega_preco_atual(codigo):
    pagina = requests.get(f'https://finance.yahoo.com/quote/{codigo}.SA?p={codigo}.SA&.tsrc=fin-srch')
    soup = BeautifulSoup(pagina.content, 'html.parser')
    preco = soup.find('span', {'class':'Trsdu(0.3s)','data-reactid':'31'})
    if preco == None:
        return None
    return float(preco.string.split(' ')[0])