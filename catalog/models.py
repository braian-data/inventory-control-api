from django.db import models
from django.conf import settings
from accounts.models import Polo


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.razao_social


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    preco_base = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produtos"
    )
    fornecedor_padrao = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produtos"
    )
    estoque_minimo = models.PositiveIntegerField(default=5)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.sku})"


class Estoque(models.Model):
    polo = models.ForeignKey(
        Polo,
        on_delete=models.CASCADE,
        related_name="estoques"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="saldos_polo"
    )
    quantidade = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Estoque do Polo"
        verbose_name_plural = "Estoques dos Polos"
        unique_together = ('polo', 'produto')  # Garante 1 registro por produto em cada polo

    def __str__(self):
        return f"{self.produto.nome} | {self.polo.nome}: {self.quantidade} un."


class MovimentacaoEstoque(models.Model):
    class TipoMovimentacao(models.TextChoices):
        ENTRADA_RIR = "ENTRADA_RIR", "Entrada (RIR Aprovado)"
        SAIDA_VENDA = "SAIDA_VENDA", "Saída (Venda)"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferência entre Polos"
        AJUSTE = "AJUSTE", "Ajuste Manual (Perda/Quebra)"
        DEVOLUCAO = "DEVOLUCAO", "Devolução ao Fornecedor"

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    polo = models.ForeignKey(Polo, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=20, choices=TipoMovimentacao.choices)
    quantidade = models.IntegerField(help_text="Valores positivos para entrada, negativos para saída.")
    data_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} ({self.quantidade}) em {self.polo.nome}"