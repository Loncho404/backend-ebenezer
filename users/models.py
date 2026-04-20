from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
    )

    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')

    puede_descargar_pdfs = models.BooleanField(default=False)
    puede_comentar = models.BooleanField(default=False)
    activo_en_plataforma = models.BooleanField(default=True)

    def __str__(self):
        return self.username