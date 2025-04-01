from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('cadastro/', views.cadastro_participante, name='cadastro_participante'),
    path('inscricao/<int:participante_id>/', views.inscricao_evento, name='inscricao_evento'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cadastro_sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),
    
    path('participantes/', views.lista_participantes, name='lista_participantes'),
    path('participante/<int:participante_id>/', views.detalhes_participante, name='detalhes_participante'),  # Este caminho está correto
    
    path('participante/atualizar/<int:id>/', views.atualizar_participante, name='atualizar_participante'),
    
    path('participacao/<int:participante_id>/atualizar/', views.atualizar_participacoes, name='atualizar_participacoes'),
    path('participacao/<int:participacao_id>/imprimir-etiqueta/', views.imprimir_etiqueta, name='imprimir_etiqueta'),
    path('cancelar/<int:participacao_id>/', views.cancelar_inscricao, name='cancelar_inscricao'),
    path('sucesso/', views.sucesso, name='sucesso'),
    
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalhes_evento, name='detalhes_evento'),
    path('evento/<int:evento_id>/participantes/', views.lista_participantes_evento, name='lista_participantes_evento'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("import_participantes/", views.import_participantes, name="import_participantes"),

    path('relatorio-kpi/', views.kpi_relatorio, name='relatorio_kpi'),
]
