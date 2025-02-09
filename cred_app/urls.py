from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('cadastro/', views.cadastro_participante, name='cadastro_participante'),
    path('inscricao/<int:participante_id>/', views.inscricao_evento, name='inscricao_evento'),
    path('sucesso/', views.sucesso, name='sucesso'),
    
    path('participantes/', views.lista_participantes, name='lista_participantes'),
    path('participante/<int:participante_id>/', views.detalhes_participante, name='detalhes_participante'),  # Este caminho está correto
    # Remova a linha abaixo, pois é redundante e causa conflito
    # path('detalhes_participante/', views.detalhes_participante, name='detalhes_participante'),
    
    path('participante/atualizar/<int:id>/', views.atualizar_participante, name='atualizar_participante'),
    
    path('participantes/<int:participante_id>/atualizar/', views.atualizar_participacoes, name='atualizar_participacoes'),
    path('participacao/<int:participacao_id>/imprimir-etiqueta/', views.imprimir_etiqueta, name='imprimir_etiqueta'),
    
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalhes_evento, name='detalhes_evento'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("import_participantes/", views.import_participantes, name="import_participantes")
]
