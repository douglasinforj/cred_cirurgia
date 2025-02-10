from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Participante, Participacao

@receiver(post_save, sender=Participante)
def atualizar_pagamento_participacao(sender, instance, **kwargs):
    """
    Quando um participante tiver o pagamento confirmado,
    todas as suas participações terão `pagamento_confirmado` atualizado.
    """
    if instance.pago:  # Se o participante estiver pago
        Participacao.objects.filter(participante=instance).update(pagamento_confirmado=True)
    else:
        Participacao.objects.filter(participante=instance).update(pagamento_confirmado=False)
