from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone # Importante para fechas
from datetime import timedelta     # Importante para sumar días

from .models import Usuario
from .serializers import UsuarioSerializer, MyTokenObtainPairSerializer
from .permissions import SoloAdminOPlanActivo

# 1. VISTA PARA EL LOGIN
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 2. VIEWSET PARA GESTIÓN DE USUARIOS
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "status": "success",
                "message": "Usuario registrado exitosamente",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- AQUÍ ESTÁ LA MODIFICACIÓN CLAVE ---
    def partial_update(self, request, *args, **kwargs):
        """
        Lógica para sumar días automáticamente si el ADMIN cambia el plan.
        """
        instance = self.get_object()
        data = request.data.copy() # Copiamos para poder editar los valores

        # 1. Verificamos si quien edita es ADMIN
        if request.user.rol == Usuario.ADMIN:
            nuevo_plan = data.get('plan')
            fecha_enviada = data.get('fecha_vencimiento')

            # 2. Si el admin cambió el plan pero NO eligió una fecha manual
            if nuevo_plan and not fecha_enviada:
                ahora = timezone.now()
                
                if nuevo_plan == 'MONTHLY':
                    # Sumamos 30 días exactos desde hoy
                    data['fecha_vencimiento'] = (ahora + timedelta(days=30)).isoformat()
                elif nuevo_plan == 'ANNUAL':
                    # Sumamos 365 días desde hoy
                    data['fecha_vencimiento'] = (ahora + timedelta(days=365)).isoformat()
                elif nuevo_plan == 'FREE':
                    # Limpiamos la fecha (vuelve a estado inicial)
                    data['fecha_vencimiento'] = None

        # 3. Procedemos con la actualización normal
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Mantenemos tu validación de seguridad original
        instance = self.get_object()
        if request.user.rol != Usuario.ADMIN and instance.id != request.user.id:
            return Response(
                {"detail": "No tienes permiso para editar un perfil ajeno."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)