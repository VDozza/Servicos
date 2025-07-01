from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class AreaAtuacao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    TIPOS = [
        ('C', 'Cliente'),
        ('P', 'Prestador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    profissao = models.CharField(max_length=100, blank=True, null=True)
    areas = models.ManyToManyField(AreaAtuacao, blank=True)
    
    @property
    def nome_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
    
    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_display()})"

class Certificacao(models.Model):
    prestador = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'tipo': 'P'})
    nome = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    data = models.DateField()
    
    def __str__(self):
        return f"{self.nome} ({self.instituicao})"

class Solicitacao(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aguardando'),
        ('C', 'Confirmado'),
        ('E', 'Em andamento'),
        ('F', 'Finalizado'),
        ('X', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'tipo': 'C'})
    prestador = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, 
                                 limit_choices_to={'tipo': 'P'}, related_name='servicos_prestados')
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    area = models.ForeignKey(AreaAtuacao, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Solicitação #{self.id} - {self.cliente.nome_completo}"

class Agendamento(models.Model):
    solicitacao = models.OneToOneField(Solicitacao, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    duracao = models.DurationField()
    status = models.CharField(max_length=1, choices=Solicitacao.STATUS_CHOICES, default='A')
    
    def __str__(self):
        return f"Agendamento para {self.solicitacao.cliente.nome_completo} em {self.data_hora}"

class Avaliacao(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    reclamacao = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Avaliação {self.nota} estrelas para {self.solicitacao.prestador.nome_completo}"

class Pagamento(models.Model):
    METODOS = [
        ('D', 'Dinheiro'),
        ('P', 'PIX'),
        ('C', 'Cartão'),
        ('B', 'Boleto'),
    ]
    
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=1, choices=METODOS)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Solicitacao.STATUS_CHOICES, default='A')
    
    def __str__(self):
        return f"Pagamento de R${self.valor} para {self.solicitacao}"

class RegiaoAtendimento(models.Model):
    prestador = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'tipo': 'P'})
    cidade = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.cidade} - {self.prestador.nome_completo}"