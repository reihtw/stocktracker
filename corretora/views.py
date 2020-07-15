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
    return render(request, 'corretora/cadastrar_corretora.html')