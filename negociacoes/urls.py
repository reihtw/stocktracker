from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_negociacoes, name='visualizar_negociacoes'),
    path('atualizar_resultados', views.atualizar_resultados, name='atualizar_resultados'),
    path('<str:codigo_acao>/atualizar_resultado', views.atualizar_resultado, name='atualizar_resultado'),
    path('<str:codigo_acao>', views.negociacoes_papel, name='negociacoes_papel'),
]