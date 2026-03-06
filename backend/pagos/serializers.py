from rest_framework import serializers
from .models import Pago

class PagoSerializer(serializers.ModelSerializer):
    # Datos para mostrar en el panel de administrador
    usuario_nombre = serializers.ReadOnlyField(source='usuario.nombre')
    usuario_apellido = serializers.ReadOnlyField(source='usuario.apellido')
    usuario_ci = serializers.ReadOnlyField(source='usuario.ci')
    usuario_email = serializers.ReadOnlyField(source='usuario.email')
    
    # --- ESTA ES LA LÍNEA CLAVE QUE FALTA ---
    # Permite que la vista asigne el usuario sin que el frontend lo envíe
    usuario = serializers.ReadOnlyField(source='usuario.id')

    class Meta:
        model = Pago
        fields = [
            'id', 
            'usuario', # <--- Agrégalo aquí
            'usuario_nombre', 
            'usuario_apellido', 
            'usuario_ci', 
            'usuario_email', 
            'comprobante', 
            'plan_solicitado', 
            'fecha_envio'
        ]
        read_only_fields = ['id', 'fecha_envio']