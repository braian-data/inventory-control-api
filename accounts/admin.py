from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Polo, Usuario

@admin.register(Polo)
class PoloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regiao', 'ativo')
    search_fields = ('nome', 'regiao')
    list_filter = ('regiao', 'ativo')

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Regras de Negócio ElectroHub', {'fields': ('tipo', 'polo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Regras de Negócio ElectroHub', {'fields': ('tipo', 'polo')}),
    )
    list_display = ('username', 'email', 'tipo', 'polo', 'is_staff')
    list_filter = ('tipo', 'polo', 'is_staff', 'is_superuser')