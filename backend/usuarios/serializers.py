from rest_framework import serializers
from .models import Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 1. SERIALIZADOR PARA MANEJAR DATOS DE USUARIO (Registro y Gestión)
class UsuarioSerializer(serializers.ModelSerializer):
    # Campos calculados que Vue necesita leer
    tiene_acceso = serializers.BooleanField(read_only=True)
    dias_restantes = serializers.IntegerField(read_only=True)
    
    # Permitimos que la fecha sea nula para poder "limpiarla" (resetear acceso)
    fecha_vencimiento = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellido', 'ci', 'email', 'password', 
            'rol', 'plan', 'fecha_vencimiento', 'tiene_acceso', 'dias_restantes'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}, # Opcional al editar
            'email': {'required': True},
            # QUITAMOS 'read_only': True de plan y fecha_vencimiento para permitir cambios
        }

    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if Usuario.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def validate_ci(self, value):
        user_id = self.instance.id if self.instance else None
        if Usuario.objects.filter(ci=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Esta cédula de identidad ya existe.")
        return value

    def create(self, validated_data):
        rol = validated_data.get('rol', Usuario.USER)
        is_staff_status = True if rol == Usuario.ADMIN else False

        user = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            ci=validated_data['ci'],
            rol=rol,
            is_staff=is_staff_status
        )
        return user

    def update(self, instance, validated_data):
        plan = validated_data.get('plan')
        fecha = validated_data.get('fecha_vencimiento')

        # 1. Si el plan es FREE, reseteamos la fecha a None (limpio)
        if plan == 'FREE':
            validated_data['fecha_vencimiento'] = None
        
        # 2. FIX DEL DÍA ANTERIOR: Si viene una fecha, la ponemos al FINAL del día
        elif fecha:
            # Forzamos 23:59:59 para que el ajuste de zona horaria no cambie el día
            validated_data['fecha_vencimiento'] = fecha.replace(hour=23, minute=59, second=59)

        # Manejo de password (opcional)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        return super().update(instance, validated_data)


# 2. SERIALIZADOR PARA EL LOGIN (JWT + DATOS EXTRA)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = user.rol
        token['nombre'] = user.nombre
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['user'] = {
            'id': self.user.id,
            'nombre': self.user.nombre,
            'apellido': self.user.apellido,
            'email': self.user.email,
            'rol': self.user.rol,
            'plan': self.user.plan,
            'tiene_acceso': self.user.tiene_acceso,
            'dias_restantes': self.user.dias_restantes
        }
        return data