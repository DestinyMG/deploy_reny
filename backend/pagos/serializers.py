from rest_framework import serializers
from .models import Pago

class PagoSerializer(serializers.ModelSerializer):
    # Traemos los datos específicos del modelo Usuario relacionado
    usuario_nombre = serializers.ReadOnlyField(source='usuario.nombre')
    usuario_apellido = serializers.ReadOnlyField(source='usuario.apellido')
    usuario_ci = serializers.ReadOnlyField(source='usuario.ci')
    usuario_email = serializers.ReadOnlyField(source='usuario.email')

    class Meta:
        model = Pago
        # Incluimos los nuevos campos en la lista de fields
        fields = [
            'id', 
            'usuario_nombre', 
            'usuario_apellido', 
            'usuario_ci', 
            'usuario_email', 
            'comprobante', 
            'plan_solicitado', 
            'fecha_envio'
        ]
        # Marcamos como solo lectura para que no interfieran en el POST
        read_only_fields = ['id', 'fecha_envio']