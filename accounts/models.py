from django.contrib.auth.models import AbstractUser
from django.db import models


class Polo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    regiao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.regiao})"


class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ADMIN = "ADMIN", "Admin / Gestão Central"
        VENDEDOR = "VENDEDOR", "Vendedor"
        ESTOQUISTA = "ESTOQUISTA", "Estoquista"

    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ADMIN,
    )
    polo = models.ForeignKey(
        Polo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios",
        help_text="Polo de atuação (obrigatório para Vendedor e Estoquista).",
    )

    def __str__(self):
        return f"{self.username} - {self.get_tipo_display()}"