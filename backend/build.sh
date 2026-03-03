#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -o errexit

echo "--- Instalando dependencias ---"
pip install -r requirements.txt

echo "--- Recolectando archivos estáticos ---"
python manage.py collectstatic --no-input

echo "--- Aplicando migraciones ---"
python manage.py migrate

echo "--- Verificando Superusuario ---"
# Este bloque de Python crea el admin solo si no existe
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

# Estos valores los tomará de las variables de entorno de Render
# Si no las pones, usará los valores por defecto aquí escritos
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('ADMIN_PASSWORD', 'admin1234')

if not User.objects.filter(email=email).exists():
    print(f"Creando superusuario para {email}...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuario creado con éxito.")
else:
    print("El superusuario ya existe, saltando paso.")
EOF

echo "--- Build finalizado con éxito ---"