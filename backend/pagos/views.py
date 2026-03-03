from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta, date, datetime  # Importamos date
from .models import Pago
from .serializers import PagoSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    def get_permissions(self):
        """
        POST: Cualquier usuario logueado.
        GET/PATCH/DELETE: Solo administradores.
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        # Vincula el pago automáticamente al usuario logueado
        serializer.save(usuario=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        """
        Al aprobar, se actualiza el usuario y se ELIMINA el reporte de pago.
        """
        pago = self.get_object()
        nuevo_estado = request.data.get('estado')

        if nuevo_estado == 'APROBADO':
            usuario = pago.usuario
            # Definir días según el plan
            dias_a_sumar = 30 if pago.plan_solicitado == 'MONTHLY' else 365
            
            # --- CORRECCIÓN: Usar fechas en lugar de datetime ---
            hoy = date.today()
            
            # Lógica de acumulación usando fechas
            if usuario.fecha_vencimiento and usuario.fecha_vencimiento.date() > hoy:
                # Si la membresía NO ha vencido, sumar a la fecha existente
                fecha_base = usuario.fecha_vencimiento.date()
            else:
                # Si ya venció o no tiene, empezar desde hoy
                fecha_base = hoy
            
            # Calcular nueva fecha de vencimiento
            nueva_fecha = fecha_base + timedelta(days=dias_a_sumar)
            
            # Convertir a datetime para guardar (opcional, mantener consistencia)
            fecha_vencimiento_datetime = datetime.combine(nueva_fecha, datetime.max.time())
            # O si prefieres mantener solo fecha:
            # usuario.fecha_vencimiento = nueva_fecha
            
            # 1. Actualizar el perfil del usuario
            usuario.fecha_vencimiento = fecha_vencimiento_datetime  # O nueva_fecha si cambias el modelo
            usuario.fecha_suscripcion = timezone.now()
            usuario.plan = pago.plan_solicitado
            usuario.save()

            # 2. Limpieza de datos (Eliminar imagen y registro de pago)
            if pago.comprobante:
                pago.comprobante.delete(save=False)
            
            pago.delete()

            return Response({
                'status': 'success',
                'message': f'Membresía activada hasta {nueva_fecha.strftime("%d/%m/%Y")}. El reporte ha sido procesado y eliminado.'
            }, status=status.HTTP_200_OK)

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Al rechazar (DELETE), borramos la imagen físicamente antes de borrar el registro.
        """
        pago = self.get_object()
        if pago.comprobante:
            pago.comprobante.delete(save=False)
        return super().destroy(request, *args, **kwargs)