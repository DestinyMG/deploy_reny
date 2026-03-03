from django.db import models

# Create your models here.

from django.conf import settings

class Pago(models.Model):
    PLANES = (
        ('MONTHLY', 'Mensual'),
        ('ANNUAL', 'Anual'),
    )

    # Relación con el usuario (se obtiene del Token en el request)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reportes_pago'
    )
    # Carpeta donde se guardan las fotos: media/comprobantes/
    comprobante = models.ImageField(upload_to='comprobantes/')
    plan_solicitado = models.CharField(max_length=20, choices=PLANES)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.usuario.email} - Plan: {self.plan_solicitado}"