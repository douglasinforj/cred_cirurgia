from django.shortcuts import render
from cred_app.models import Evento  # Importar o modelo Evento do app cred_app

from django.contrib.auth.decorators import login_required

#@login_required
def home(request):
    eventos = Evento.objects.all()
    return render(request, 'core/home.html', {'eventos': eventos})


