from django.urls import path

from . import views

urlpatterns = [
    path('cadastro/papel', views.cadastro_papel, name='cadastro_papel'),
    path('papeis', views.papeis, name='papeis'),
    path('procurar/papel', views.procurar_papeis, name='procurar_papeis'),
    path('atualizar/precos', views.atualizar_precos, name='atualizar_precos')
]
