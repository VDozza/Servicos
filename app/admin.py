from django.contrib import admin
from .models import AreaAtuacao, Pessoa, Certificacao, Solicitacao, Agendamento, Avaliacao, Pagamento, RegiaoAtendimento

class AreaAtuacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class CertificacaoInline(admin.TabularInline):
    model = Certificacao
    extra = 1

class RegiaoAtendimentoInline(admin.TabularInline):
    model = RegiaoAtendimento
    extra = 1

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'tipo', 'telefone', 'profissao')
    list_filter = ('tipo', 'areas')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'telefone')
    filter_horizontal = ('areas',)
    inlines = [CertificacaoInline, RegiaoAtendimentoInline]
    
    def nome_completo(self, obj):
        return obj.nome_completo
    nome_completo.short_description = 'Nome'

class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nome', 'prestador_nome', 'status', 'data', 'valor')
    list_filter = ('status', 'area')
    search_fields = ('cliente__usuario__first_name', 'cliente__usuario__last_name')
    
    def cliente_nome(self, obj):
        return obj.cliente.nome_completo
    cliente_nome.short_description = 'Cliente'
    
    def prestador_nome(self, obj):
        return obj.prestador.nome_completo if obj.prestador else '-'
    prestador_nome.short_description = 'Prestador'

class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'data_hora', 'duracao', 'status')
    list_filter = ('status',)
    date_hierarchy = 'data_hora'

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'nota', 'reclamacao', 'data')
    list_filter = ('nota', 'reclamacao')
    search_fields = ('comentario',)

class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'valor', 'metodo', 'status', 'data')
    list_filter = ('metodo', 'status')

class RegiaoAtendimentoAdmin(admin.ModelAdmin):
    list_display = ('prestador', 'cidade')
    search_fields = ('cidade',)

# Registre todos os modelos
admin.site.register(AreaAtuacao, AreaAtuacaoAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(RegiaoAtendimento, RegiaoAtendimentoAdmin)