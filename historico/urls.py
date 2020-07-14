from django.urls import path

from . import views

urlpatterns = [
    path('atualizar_tudo', views.atualizar_tudo, name='atualizar_tudo'),
    path('<str:codigo_acao>', views.visualizar_historico, name='visualizar_historico'),
    path('<str:codigo_acao>/carregar', views.carregar_historico, name='carregar_historico'),
    path('<str:codigo_acao>/atualizar', views.atualizar_historico, name='atualizar_historico')
]