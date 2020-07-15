from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_corretoras, name='visualizar_corretoras'),
    path('cadastrar', views.cadastrar_corretora, name='cadastrar_corretora')
]