from django.urls import path

from . import views

urlpatterns = [
    path('cadastro/papel', views.cadastro_papel, name='cadastro_papel')
]
