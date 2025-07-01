from django import forms
from .models import *

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['tipo', 'telefone', 'endereco', 'profissao', 'areas']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['areas'].required = False

class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['descricao', 'area', 'valor']
        
class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data_hora', 'duracao']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario', 'reclamacao']