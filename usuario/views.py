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


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ficar vazio')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O email não pode ficar vazio')
            return redirect('cadastro')
        if nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome de usuário já cadastrado')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()

        messages.success(request, 'Usuário cadstrado com sucesso!')
        return redirect('login')
    return render(request, 'usuario/cadastro.html')

def campo_vazio(campo):
    return not campo.strip()

def nao_sao_iguais(senha, senha2):
    return senha != senha2