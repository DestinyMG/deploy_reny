

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    # Agregamos nuestros campos personalizados a la edición del admin
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Suscripción', {'fields': ('rol', 'plan', 'fecha_vencimiento', 'fecha_suscripcion')}),
        ('Datos Personales Extra', {'fields': ('ci', 'nombre', 'apellido')}),
    )
    # Campos para mostrar en la lista
    list_display = ['email', 'nombre', 'apellido', 'rol', 'plan', 'is_staff']

admin.site.register(Usuario, CustomUserAdmin)