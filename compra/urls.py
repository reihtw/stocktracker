from django.urls import path

from . import views

urlpatterns = [
    path('registrar', views.registrar_compra, name='registrar_compra'),
    path('registrar/<str:codigo_acao>', views.registrar_compra_papel, name='registrar_compra_papel'),
    path('excluir/<int:compra_id>', views.excluir_compra, name='excluir_compra')
]