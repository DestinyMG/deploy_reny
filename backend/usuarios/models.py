from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
    # Definición de Roles
    ADMIN = 'ADMIN'
    USER = 'USER'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (USER, 'Usuario Estándar'),
    ]

    # --- Campos de Identificación ---
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, unique=True)

    # --- Campo de Rol (Por defecto USER) ---
    rol = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default=USER
    )

    # --- Campos de Suscripción (Solo aplican a USER) ---
    PLAN_CHOICES = [
        ('FREE', 'Gratis'),
        ('MONTHLY', 'Mensual'),
        ('ANNUAL', 'Anual'),
    ]
    
    plan = models.CharField(
        max_length=10, 
        choices=PLAN_CHOICES, 
        default='FREE'
    )
    
    fecha_suscripcion = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)

    # Configuración de Login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido', 'ci']

    @property
    def tiene_acceso(self):
        """
        Lógica central de permisos:
        - Si es ADMIN o Superusuario: Acceso concedido (True).
        - Si es USER: Acceso concedido solo si la fecha actual es menor al vencimiento.
        """
        if self.rol == self.ADMIN or self.is_superuser or self.is_staff:
            return True
            
        if not self.fecha_vencimiento:
            return False
            
        return timezone.now() < self.fecha_vencimiento

    @property
    def dias_restantes(self):
        """Calcula los días de gracia restantes para usuarios con plan."""
        if self.rol == self.ADMIN:
            return 9999 # Valor simbólico para admins
            
        if not self.fecha_vencimiento:
            return 0
            
        delta = self.fecha_vencimiento - timezone.now()
        return max(0, delta.days)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol} ({self.plan})"