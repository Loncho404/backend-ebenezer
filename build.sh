#!/usr/bin/env bash
# Build Command para Render:  ./build.sh
# Instala dependencias, recolecta estáticos, migra la BD y (opcionalmente)
# crea el superusuario si se definen las variables DJANGO_SUPERUSER_*.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# El plan free de Render no tiene shell: el superusuario se crea desde el build
# definiendo DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL y
# DJANGO_SUPERUSER_PASSWORD en Environment. Si ya existe, no hace nada.
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
if User.objects.filter(username=username).exists():
    print(f'Superusuario {username} ya existe, se omite.')
else:
    User.objects.create_superuser(
        username=username,
        email=os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
        password=os.environ['DJANGO_SUPERUSER_PASSWORD'],
        rol='admin',
        puede_descargar_pdfs=True,
        puede_comentar=True,
    )
    print(f'Superusuario {username} creado.')
"
fi
