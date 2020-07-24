from django.urls import path

from . import views

urlpatterns = [
    path('registrar/<str:codigo_acao>', views.registrar_venda, name='registrar_venda'),
    path('excluir/<int:venda_id>', views.excluir_venda, name='excluir_venda')
]