from django.contrib import admin
from .models import Categoria, NivelCorderito, TemaCorderito, Contenido, Comentario, CalendarioDelMes


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(NivelCorderito)
class NivelCorderitoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'orden', 'activo')
    list_editable = ('orden', 'activo')


@admin.register(TemaCorderito)
class TemaCorderitoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nivel', 'orden', 'activo')
    list_filter = ('nivel', 'activo')
    list_editable = ('orden', 'activo')


@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'tema', 'categoria', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'categoria')
    search_fields = ('titulo',)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'contenido', 'usuario', 'fecha_creacion')

@admin.register(CalendarioDelMes)
class CalendarioDelMesAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'mes', 'anio', 'activo', 'fecha_creacion')
    list_filter = ('mes', 'anio', 'activo')
    list_editable = ('activo',)