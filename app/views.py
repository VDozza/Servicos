from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

def home(request):
    return render(request, 'core/home.html')

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def cadastrar_prestador(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            pessoa = form.save(commit=False)
            pessoa.usuario = request.user
            pessoa.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = PessoaForm()
    return render(request, 'core/cadastro_prestador.html', {'form': form})

@login_required
def listar_prestadores(request):
    prestadores = Pessoa.objects.filter(tipo='P')
    return render(request, 'core/lista_prestadores.html', {'prestadores': prestadores})

@login_required
def solicitar_servico(request):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.cliente = request.user.pessoa
            solicitacao.save()
            return redirect('agendar_servico', solicitacao.id)
    else:
        form = SolicitacaoForm()
    return render(request, 'core/solicitar_servico.html', {'form': form})

@login_required
def agendar_servico(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.solicitacao = solicitacao
            agendamento.save()
            return redirect('home')
    else:
        form = AgendamentoForm()
    return render(request, 'core/agendar_servico.html', {'form': form, 'solicitacao': solicitacao})

@login_required
def avaliar_servico(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.solicitacao = solicitacao
            avaliacao.save()
            return redirect('home')
    else:
        form = AvaliacaoForm()
    return render(request, 'core/avaliar_servico.html', {'form': form, 'solicitacao': solicitacao})