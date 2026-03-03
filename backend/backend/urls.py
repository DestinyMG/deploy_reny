from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
# IMPORTANTE: Importamos TU vista personalizada, no la de la librería
from usuarios.views import MyTokenObtainPairView 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN PERSONALIZADO: Ahora devuelve Tokens + Datos del Usuario (Rol, Plan, Acceso)
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # REFRESH: Para obtener un nuevo access token sin loguearse de nuevo
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoints de la App (incluye /api/usuarios/ para registro y perfiles)
    path('api/', include('usuarios.urls')),

    path('api/pagos/', include('pagos.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)