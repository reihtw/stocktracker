from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Corretora

# Create your views here.

def visualizar_corretoras(request):
    corretoras = Corretora.objects.all()

    dados = {
        'corretoras' : corretoras
    }

    return render(request, 'corretora/visualizar_corretoras.html', dados)

def cadastrar_corretora(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        taxa_acoes = request.POST['taxa_acoes']
        taxa_acoes_fracionario = request.POST['taxa_acoes_fracionario']
        taxa_fiis = request.POST['taxa_fiis']
        taxa_etfs = request.POST['taxa_etfs']

        user = get_object_or_404(User, pk=request.user.id)

        if Corretora.objects.filter(nome=nome):
            messages.error(request, 'Corretora já cadastrada!')
            return redirect('cadastrar_corretora')

        corretora = Corretora.objects.create(
            usuario=user,
            nome=nome,
            taxa_acoes=taxa_acoes,
            taxa_acoes_fracionario=taxa_acoes_fracionario,
            taxa_fiis=taxa_fiis,
            taxa_etfs=taxa_etfs
        )

        corretora.save()

        return redirect('visualizar_corretoras')
    dados = {
        'titulo': 'Cadastrar',
        'metodo': 'cadastrar_corretora'
    }
    return render(request, 'corretora/cadastrar_corretora.html', dados)

def editar_corretora(request, nome):
    corretora = Corretora.objects.get(nome=nome)
    
    corretora_a_editar = {
        'titulo': 'Editar',
        'corretora': corretora,
        'metodo': 'atualizar_corretora'
    }

    return render(request, 'corretora/cadastrar_corretora.html', corretora_a_editar)

def atualizar_corretora(request):
    if request.method == 'POST':
        corretora_id = request.POST['corretora_id']
        corretora = Corretora.objects.get(pk=corretora_id)
        corretora.nome = request.POST['nome']
        corretora.taxa_acoes = request.POST['taxa_acoes'].replace(',', '.')
        corretora.taxa_acoes_fracionario = request.POST['taxa_acoes_fracionario'].replace(',', '.')
        corretora.taxa_fiis = request.POST['taxa_fiis'].replace(',', '.')
        corretora.taxa_etfs = request.POST['taxa_etfs'].replace(',', '.')

        if Corretora.objects.exclude(pk=corretora_id).filter(nome=corretora.nome):
            messages.error(request, 'Nome já cadastrado em outra corretora!')
            return redirect('editar_corretora', corretora.nome)

        corretora.save()
        return redirect('visualizar_corretoras')

def excluir_corretora(request, corretora_id):
    corretora = Corretora.objects.get(pk=corretora_id)
    corretora.delete()
    return redirect('visualizar_corretoras')


