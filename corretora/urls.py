from django.urls import path

from . import views

urlpatterns = [
    path('', views.visualizar_corretoras, name='visualizar_corretoras'),
    path('cadastrar', views.cadastrar_corretora, name='cadastrar_corretora'),
    path('editar/<str:nome>', views.editar_corretora, name='editar_corretora'),
    path('atualizar', views.atualizar_corretora, name='atualizar_corretora'),
    path('excluir/<int:corretora_id>', views.excluir_corretora, name='excluir_corretora'),
]