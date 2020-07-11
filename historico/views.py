import requests, json

from django.shortcuts import render, redirect

from datetime import date, datetime

from .models import Historico
from papel.models import Papel

# Create your views here.

def visualizar_historico(request, codigo_acao):
    papel = Papel.objects.get(codigo_acao=codigo_acao)
    historico = Historico.objects.order_by('-dia').filter(codigo_acao_id=papel.id)

    dados = {
        'historico' : historico,
        'papel' : papel
    }

    return render(request, 'historico/historico.html', dados)

def carregar_historico(request, codigo_acao):
    if request.method == 'GET':
        hoje = date.today()
        dia = hoje.day -1
        mes = hoje.month
        ano = hoje.year

        erros = 0

        while erros < 30:
            pagina = requests.get(f'https://bovespa.nihey.org/api/quote/{codigo_acao}/{ano}-{mes}-{dia}')
            x = pagina.content
            dados_acao = json.loads(x)

            try:
                registra_dados_no_historico(dados_acao, date(ano, mes, dia))
                print('Resetando erros')
                erros = 0
            except (KeyError, ValueError):
                print('adicionando erro')
                erros += 1
            finally:
                if mes == 1 and dia == 1:
                    ano -= 1

                if mes == 1 and dia == 1:
                    mes = 12
                elif dia == 1:
                    mes -= 1
                
                if dia == 1 and mes != 2:
                    dia = 31
                elif dia == 1 and mes == 2:
                    dia = 29
                else:
                    dia -= 1    
    return redirect(visualizar_historico, codigo_acao)

def registra_dados_no_historico(dados_acao, data):
    abertura = float(dados_acao['preabe'])
    fechamento = float(dados_acao['preult'])
    maximo = float(dados_acao['premax'])
    minimo = float(dados_acao['premin'])
    media = float(dados_acao['premed'])
    codigo_acao = dados_acao['codneg']

    papel = Papel.objects.get(codigo_acao=codigo_acao)

    try:
        if Historico.objects.get(dia=data, codigo_acao_id=papel.id):
            return 1
    except:
        pass

    print(papel.id)

    historico = Historico.objects.create(
        codigo_acao=papel,
        dia=data,
        abertura=abertura,
        fechamento=fechamento,
        maximo=maximo,
        minimo=minimo,
        media=media
    )
    

    historico.save()
    print(historico)
