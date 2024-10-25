from django.db import models


class Evento(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Evento")
    data = models.DateTimeField(verbose_name="Data de Início")
    data_termino = models.DateTimeField(verbose_name="Data de Término", null=True, blank=True)
    local = models.CharField(max_length=255, verbose_name="Local do Evento")
    descricao = models.TextField(verbose_name="Descrição do Evento")
    foto = models.ImageField(upload_to='fotos/eventos/', null=True, blank=True, verbose_name="Foto do Evento")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
 

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.nome
    

class Participante(models.Model):
    foto = models.ImageField(upload_to='fotos/participante/', null=True, blank=True, verbose_name="Foto")
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    email = models.EmailField(unique=True)
    nome_empresa = models.CharField(max_length=100, verbose_name="Nome Empresa")
    cnpj_empresa = models.CharField(max_length=14, verbose_name="CNPJ Empresa")
    telefone = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    def __str__(self):
        return self.nome
    

class Participacao(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    pagamento_confirmado = models.BooleanField(default=False)
    checkin_realizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.participante.nome} - {self.evento.nome}"
    
    class Meta:
        verbose_name = "Participação"
        verbose_name_plural = "Participações"

