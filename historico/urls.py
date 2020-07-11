from django.urls import path

from . import views

urlpatterns = [
    path('historico/<str:codigo_acao>', views.visualizar_historico, name='visualizar_historico'),
    path('historico/<str:codigo_acao>/carregar', views.carregar_historico, name='carregar_historico')
]