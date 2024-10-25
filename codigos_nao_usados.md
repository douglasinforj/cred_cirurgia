@login_required
def detalhes_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    participacoes = Participacao.objects.filter(participante=participante)

    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES, instance=participante)
        if form.is_valid():
            form.save()  # Salva as alterações
            return redirect('detalhes_participante', participante_id=participante.id)  # Redireciona para a página de detalhes
    else:
        form = ParticipanteForm(instance=participante)

    return render(request, 'cred_app/detalhes_participante.html', {
        'participante': participante,
        'participacoes': participacoes,
        'form': form
    })