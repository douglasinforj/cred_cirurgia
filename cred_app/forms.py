from django import forms
from .models import Participante, Participacao


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email', 'cpf', 'nome_empresa', 'cnpj_empresa', 'telefone', 'foto']

class ParticipacaoForm(forms.ModelForm):
    class Meta:
        model = Participacao
        fields = ['evento']