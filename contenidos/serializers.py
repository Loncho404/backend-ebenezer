from rest_framework import serializers
from .models import Categoria, Contenido, Comentario, NivelCorderito, TemaCorderito, CalendarioDelMes


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ContenidoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True
    )

    class Meta:
        model = Contenido
        fields = [
            'id',
            'titulo',
            'descripcion',
            'youtube_url',
            'pdf',
            'categoria',
            'categoria_id',
            'fecha_creacion',
            'activo'
        ]


class ComentarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Comentario
        fields = [
            'id',
            'contenido',
            'usuario',
            'usuario_nombre',
            'mensaje',
            'respuesta',
            'fecha_creacion',
        ]
        read_only_fields = [
            'contenido',
            'usuario',
            'usuario_nombre',
            'respuesta',
            'fecha_creacion',
        ]


class NivelCorderitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelCorderito
        fields = ['id', 'nombre', 'orden', 'activo']


class TemaCorderitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemaCorderito
        fields = ['id', 'nombre', 'orden', 'activo', 'nivel']


class ContenidoTemaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    tema = TemaCorderitoSerializer(read_only=True)

    class Meta:
        model = Contenido
        fields = [
            'id',
            'titulo',
            'descripcion',
            'youtube_url',
            'pdf',
            'categoria',
            'tema',
            'fecha_creacion',
            'activo',
        ]

class CalendarioDelMesSerializer(serializers.ModelSerializer):
    mes_nombre = serializers.CharField(source='get_mes_display', read_only=True)

    class Meta:
        model = CalendarioDelMes
        fields = [
            'id',
            'titulo',
            'imagen',
            'mes',
            'mes_nombre',
            'anio',
            'activo',
            'fecha_creacion',
        ]