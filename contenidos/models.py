from django.conf import settings
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class NivelCorderito(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Nivel de Corderitos'
        verbose_name_plural = 'Niveles de Corderitos'

    def __str__(self):
        return self.nombre


class TemaCorderito(models.Model):
    nivel = models.ForeignKey(
        NivelCorderito,
        on_delete=models.CASCADE,
        related_name='temas'
    )
    nombre = models.CharField(max_length=150)
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Tema de Corderitos'
        verbose_name_plural = 'Temas de Corderitos'

    def __str__(self):
        return f'{self.nivel.nombre} - {self.nombre}'


class Contenido(models.Model):
    tema = models.OneToOneField(
        TemaCorderito,
        on_delete=models.CASCADE,
        related_name='contenido',
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    youtube_url = models.URLField()
    pdf = models.FileField(upload_to='pdfs/')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='contenidos',
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    contenido = models.ForeignKey(
        Contenido,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    mensaje = models.TextField()
    respuesta = models.TextField(blank=True, null=True)
    respondido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='respuestas_realizadas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.contenido.titulo}'

class CalendarioDelMes(models.Model):
    MESES = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    )

    titulo = models.CharField(max_length=150)
    imagen = models.CharField(max_length=255)
    mes = models.PositiveSmallIntegerField(choices=MESES)
    anio = models.PositiveIntegerField()
    activo = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-anio', '-mes', '-fecha_creacion']
        verbose_name = 'Calendario del mes'
        verbose_name_plural = 'Calendarios del mes'

    def __str__(self):
        return f'{self.titulo} - {self.get_mes_display()} {self.anio}'

    def save(self, *args, **kwargs):
        if self.activo:
            CalendarioDelMes.objects.exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)