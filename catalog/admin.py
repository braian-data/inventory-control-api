from django.contrib import admin
from .models import Categoria, Fornecedor, Produto, Estoque, MovimentacaoEstoque

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'email', 'telefone')
    search_fields = ('razao_social', 'cnpj')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'preco_base', 'categoria', 'fornecedor_padrao', 'ativo')
    list_filter = ('categoria', 'ativo', 'fornecedor_padrao')
    search_fields = ('nome', 'sku')

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'polo', 'quantidade')
    list_filter = ('polo', 'produto__categoria')
    search_fields = ('produto__nome', 'polo__nome')

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'polo', 'produto', 'tipo', 'quantidade', 'usuario')
    list_filter = ('tipo', 'polo', 'data_hora')
    search_fields = ('produto__nome', 'observacao')
    readonly_fields = ('data_hora',)