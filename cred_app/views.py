from django.shortcuts import render, redirect, get_object_or_404
from .forms import ParticipanteForm, ParticipacaoForm, UploadFileForm
from .models import Evento, Participante, Participacao
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.db.models import Q

from django.core.paginator import Paginator  #paginações

import pandas as pd


#autenticação do sistema:

class CustomLoginView(LoginView):
    template_name = 'cred_app/login.html'



@login_required
def lista_participantes(request):
    query = request.GET.get('q', '')
    
    # Filtrar e ordenar os participantes
    participantes = Participante.objects.filter(
        Q(nome__icontains=query) | Q(cpf__icontains=query)  # Adiciona pesquisa por CPF
    ).order_by('nome')

    paginator = Paginator(participantes, 5)  # Alterar o número '5' se quiser mais ou menos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cred_app/lista_participantes.html', {'page_obj': page_obj, 'query': query})


@login_required
def detalhes_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    participacoes = Participacao.objects.filter(participante=participante)
    return render(request, 'cred_app/detalhes_participante.html', {
        'participante': participante,
        'participacoes': participacoes
    })

@login_required
def atualizar_participante(request, id):
    participante = get_object_or_404(Participante, id=id)

    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES, instance=participante)
        if form.is_valid():
            form.save()
            return redirect('detalhes_participante', participante_id=participante.id)  # Use o nome correto aqui
    else:
        form = ParticipanteForm(instance=participante)

    return render(request, 'cred_app/atualizar_participante.html', {
        'form': form,
        'participante': participante
    })




@login_required
def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'cred_app/lista_eventos.html', {'eventos': eventos})

@login_required
def detalhes_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)  # Busca o evento pelo ID ou retorna 404 se não encontrar
    return render(request, 'cred_app/detalhes_evento.html', {'evento': evento})




# Função para cadastrar o participante
def cadastro_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o participante
            participante = form.save()

            # Verificar se um evento foi selecionado e criar a participação
            evento_id = request.POST.get('evento')
            if evento_id:
                evento = Evento.objects.get(id=evento_id)
                Participacao.objects.create(participante=participante, evento=evento)
            
            # Redireciona para a página de sucesso
            return redirect('sucesso')
    else:
        form = ParticipanteForm()

    # Passando todos os eventos para o template
    eventos = Evento.objects.all()
    return render(request, 'cred_app/cadastro_participante.html', {'form': form, 'eventos': eventos})



# Função para inscrição em eventos
def inscricao_evento(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    
    if request.method == 'POST':
        form = ParticipacaoForm(request.POST)
        if form.is_valid():
            participacao = form.save(commit=False)
            participacao.participante = participante  # Associa o participante à inscrição
            participacao.save()  # Salva a participação
            return redirect('sucesso')  # Redireciona para a página de sucesso
    else:
        form = ParticipacaoForm()
    
    eventos = Evento.objects.all()  # Obtém todos os eventos
    return render(request, 'cred_app/inscricao_evento.html', {'form': form, 'eventos': eventos, 'participante': participante})


# Página de sucesso
def sucesso(request):
    return render(request, 'cred_app/sucesso.html')




#para atualizar os status de checkin e pagamentos e liberar impressao
@login_required
def atualizar_participacoes(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    participacoes = Participacao.objects.filter(participante=participante)

    if request.method == 'POST':
        for participacao in participacoes:
            pagamento_confirmado = request.POST.get(f'pagamento_confirmado_{participacao.id}') == 'True'
            checkin_realizado = request.POST.get(f'checkin_realizado_{participacao.id}') == 'on'

            # Atualiza o pagamento confirmado
            participacao.pagamento_confirmado = pagamento_confirmado

            # O check-in só pode ser feito se o pagamento estiver confirmado
            if pagamento_confirmado:
                participacao.checkin_realizado = checkin_realizado
            else:
                participacao.checkin_realizado = False

            participacao.save()

        return redirect('detalhes_participante', participante_id=participante.id)
    



#chamar a pagina de impressao:

def imprimir_etiqueta(request, participacao_id):
    participacao = get_object_or_404(Participacao, id=participacao_id)
    return render(request, 'cred_app/imprimir_etiqueta.html', {'participacao': participacao})




# Importação de dados:

def import_participantes(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            try:
                # Verifica se o arquivo é CSV ou Excel
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file, dtype=str)
                elif file.name.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(file, dtype=str)
                else:
                    messages.error(request, "Formato de arquivo inválido. Use CSV ou Excel.")
                    return redirect("import_participantes")

                # Renomeia colunas para corresponder ao modelo
                df = df.rename(columns={
                    "Foto": "foto",
                    "Nome": "nome",
                    "CPF": "cpf",
                    "E-mail": "email",
                    "Nome Empresa": "nome_empresa",
                    "CNPJ Empresa": "cnpj_empresa",
                    "Telefone": "telefone",
                })

                # Verifica se todas as colunas necessárias existem
                required_columns = {"nome", "cpf", "email", "nome_empresa", "cnpj_empresa", "telefone"}
                if not required_columns.issubset(df.columns):
                    messages.error(request, "O arquivo deve conter as colunas: Nome, CPF, Email, Nome Empresa, CNPJ Empresa e Telefone.")
                    return redirect("import_participantes")

                # Importa os dados para o banco de dados
                for _, row in df.iterrows():
                    if not Participante.objects.filter(cpf=row["cpf"]).exists():
                        Participante.objects.create(
                            nome=row["nome"],
                            cpf=row["cpf"],
                            email=row["email"],
                            nome_empresa=row["nome_empresa"],
                            cnpj_empresa=row["cnpj_empresa"],
                            telefone=row["telefone"]
                        )
                
                messages.success(request, "Dados importados com sucesso!")
                return redirect("import_participantes")

            except Exception as e:
                messages.error(request, f"Erro ao importar: {str(e)}")
                return redirect("import_participantes")

    else:
        form = UploadFileForm()
    
    return render(request, "cred_app/import_participantes.html", {"form": form})
