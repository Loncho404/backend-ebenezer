from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'username',
        'email',
        'rol',
        'puede_descargar_pdfs',
        'puede_comentar',
        'activo_en_plataforma',
        'is_active',
    )

    list_filter = (
        'rol',
        'puede_descargar_pdfs',
        'puede_comentar',
        'activo_en_plataforma',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Permisos de plataforma', {
            'fields': (
                'rol',
                'puede_descargar_pdfs',
                'puede_comentar',
                'activo_en_plataforma',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Permisos de plataforma', {
            'fields': (
                'rol',
                'puede_descargar_pdfs',
                'puede_comentar',
                'activo_en_plataforma',
            )
        }),
    )