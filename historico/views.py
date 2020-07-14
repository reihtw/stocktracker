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

def atualizar_tudo(request):
    papeis = Papel.objects.all()

    for papel in papeis:
        if papel.historico_completo:
            pega_historico(codigo_acao=papel.codigo_acao, completo=True)
        else:
            pega_historico(codigo_acao=papel.codigo_acao)
    
    return redirect('home')

def atualizar_historico(request, codigo_acao):
    papel = Papel.objects.get(codigo_acao=codigo_acao)
    
    if papel.historico_completo:
        pega_historico(codigo_acao=papel.codigo_acao, completo=True)
    else:
        pega_historico(codigo_acao=papel.codigo_acao)

    return redirect('visualizar_historico', papel.codigo_acao)

            

def carregar_historico(request, codigo_acao):
    if request.method == 'GET':
        pega_historico(codigo_acao)

    return redirect(visualizar_historico, codigo_acao)

def pega_historico(codigo_acao, completo=False):  
    hoje = date.today()
    dia = hoje.day
    mes = hoje.month
    ano = hoje.year

    
    # verifica se apesar do histórico não estar completo, existem registros incompletos do papel
    # se sim, ele começa a pegar os registros restantes a partir da data que ele parou a última vez
    if completo == False:
        try:
            papel = Papel.objects.get(codigo_acao=codigo_acao)
            historico = Historico.objects.order_by('dia').filter(codigo_acao_id=papel.id)
            ultima_data = historico[0].dia
            dia = ultima_data.day
            mes = ultima_data.month
            ano = ultima_data.year
        except:
            pass
    
    erros = 0
    acabou = 0

    # loop para pegar o histórico até os erros (dias inválidos) forem maior que 30, ou o valor da variável acabou mudar para 1
    # no caso do registro estar incompleto, ele só irá parar até bater 30 dias inválidos
    # caso esteja completo, ele vai parar ao encontrar uma data já existente registrada no banco
    while erros < 30 and acabou == 0:
        pagina = requests.get(f'https://bovespa.nihey.org/api/quote/{codigo_acao}/{ano}-{mes}-{dia}')
        x = pagina.content
        dados_acao = json.loads(x)

        try:
            acabou = registra_dados_no_historico(dados_acao, date(ano, mes, dia))
            print(acabou)
            # se o histórico não está completo, ele só vai parar quando não encontrar mais registros (30 dias inválidos)
            if not completo:
                acabou = 0
            print(acabou)
            print('Resetando erros')
            erros = 0
        except (KeyError, ValueError):
            print('adicionando erro')
            erros += 1
        finally:
            # se for primeiro de janeiro, ele vai subtrair o ano
            if mes == 1 and dia == 1:
                ano -= 1

            # se for primeiro de janeiro, ele vai resetar o mês para 12 (Dezembro)
            if mes == 1 and dia == 1:
                mes = 12
            # caso não for janeiro, mas for dia 1, ele subtrai o mês também
            elif dia == 1:
                mes -= 1
            
            # se for dia 1 e o mês não for fevereiro, ele reseta o valor do dia para 31
            if dia == 1 and mes != 2:
                dia = 31
            # caso fevereiro ele reseta para 29
            elif dia == 1 and mes == 2:
                dia = 29
            # caso contrário ele só subtrai o dia
            else:
                dia -= 1

    # ao terminar o loop, ele seta o histórico como completo
    if erros == 30:
        papel = Papel.objects.get(codigo_acao=codigo_acao)
        papel.historico_completo = True
        papel.save()

def registra_dados_no_historico(dados_acao, data):
    abertura = float(dados_acao['preabe'])
    fechamento = float(dados_acao['preult'])
    maximo = float(dados_acao['premax'])
    minimo = float(dados_acao['premin'])
    media = float(dados_acao['premed'])
    codigo_acao = dados_acao['codneg']

    papel = Papel.objects.get(codigo_acao=codigo_acao)

    # verifica se ele acha algum registro dessa data, para que ele possa mandar o sinal de que acabou
    try:
        if Historico.objects.get(dia=data, codigo_acao_id=papel.id):
            return 1
    except:
        pass

    print(papel.id)

    # caso não exista registro da data, ele cria um objeto do histórico e o salva
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
    return 0

