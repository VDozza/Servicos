# Generated by Django 5.2.3 on 2025-07-01 12:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaAtuacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('C', 'Cliente'), ('P', 'Prestador')], max_length=1)),
                ('telefone', models.CharField(max_length=20)),
                ('endereco', models.TextField()),
                ('profissao', models.CharField(blank=True, max_length=100, null=True)),
                ('areas', models.ManyToManyField(blank=True, to='app.areaatuacao')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('instituicao', models.CharField(max_length=100)),
                ('data', models.DateField()),
                ('prestador', models.ForeignKey(limit_choices_to={'tipo': 'P'}, on_delete=django.db.models.deletion.CASCADE, to='app.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='RegiaoAtendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=100)),
                ('prestador', models.ForeignKey(limit_choices_to={'tipo': 'P'}, on_delete=django.db.models.deletion.CASCADE, to='app.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('A', 'Aguardando'), ('C', 'Confirmado'), ('E', 'Em andamento'), ('F', 'Finalizado'), ('X', 'Cancelado')], default='A', max_length=1)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.areaatuacao')),
                ('cliente', models.ForeignKey(limit_choices_to={'tipo': 'C'}, on_delete=django.db.models.deletion.CASCADE, to='app.pessoa')),
                ('prestador', models.ForeignKey(blank=True, limit_choices_to={'tipo': 'P'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicos_prestados', to='app.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo', models.CharField(choices=[('D', 'Dinheiro'), ('P', 'PIX'), ('C', 'Cartão'), ('B', 'Boleto')], max_length=1)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('A', 'Aguardando'), ('C', 'Confirmado'), ('E', 'Em andamento'), ('F', 'Finalizado'), ('X', 'Cancelado')], default='A', max_length=1)),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.solicitacao')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('reclamacao', models.BooleanField(default=False)),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.solicitacao')),
            ],
        ),
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField()),
                ('duracao', models.DurationField()),
                ('status', models.CharField(choices=[('A', 'Aguardando'), ('C', 'Confirmado'), ('E', 'Em andamento'), ('F', 'Finalizado'), ('X', 'Cancelado')], default='A', max_length=1)),
                ('solicitacao', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.solicitacao')),
            ],
        ),
    ]
