from rest_framework import permissions

class SoloAdminOPlanActivo(permissions.BasePermission):
    """
    Permiso personalizado para DRF:
    - ADMIN: Acceso total garantizado.
    - USER: Solo accede si tiene_acceso es True (suscripción vigente).
    """
    message = "Acceso denegado. Tu suscripción ha vencido o no tienes permisos suficientes."

    def has_permission(self, request, view):
        # 1. Verificamos que el usuario esté autenticado (haya hecho login)
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 2. Usamos la lógica centralizada en nuestro modelo de Usuario
        # Esto cubre: Superusuarios, is_staff, Rol ADMIN y Usuarios con plan activo.
        return request.user.tiene_acceso