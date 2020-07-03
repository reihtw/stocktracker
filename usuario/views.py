from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages

# Create your views here.

def home(request):
    return render(request, 'usuario/home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos de email e senha não podem ficar vazios')
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('home')
            else:
                messages.error(request, 'Senha inválida!')
                return redirect('home')
        else:
            messages.error(request, 'Email inválido!')
    return render(request, 'usuario/home.html')

def campo_vazio(campo):
    return not campo.strip()

def nao_sao_iguais(senha, senha2):
    return senha != senha2