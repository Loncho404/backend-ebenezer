from django.urls import path
from .views import (
    CategoriaListAPIView,
    ContenidoListAPIView,
    ContenidoDetailAPIView,
    ContenidoCreateAPIView,
    ComentarioListCreateAPIView,
    ResponderComentarioAPIView,
    NivelCorderitoListAPIView,
    TemaPorNivelListAPIView,
    ContenidoPorTemaDetailAPIView, 
    DescargarPDFAPIView,
    CalendarioActivoAPIView,
)

urlpatterns = [
    path('categorias/', CategoriaListAPIView.as_view(), name='categoria-list'),
    path('contenidos/', ContenidoListAPIView.as_view(), name='contenido-list'),
    path('contenidos/create/', ContenidoCreateAPIView.as_view(), name='contenido-create'),
    path('contenidos/<int:pk>/', ContenidoDetailAPIView.as_view(), name='contenido-detail'),
    path('contenidos/<int:contenido_id>/comentarios/', ComentarioListCreateAPIView.as_view(), name='comentario-list-create'),
    path('comentarios/<int:pk>/responder/', ResponderComentarioAPIView.as_view(), name='comentario-responder'),
    path('corderitos/niveles/', NivelCorderitoListAPIView.as_view(), name='corderitos-niveles'),
    path('corderitos/niveles/<int:nivel_id>/temas/', TemaPorNivelListAPIView.as_view(), name='corderitos-temas'),
    path('corderitos/temas/<int:tema_id>/contenido/', ContenidoPorTemaDetailAPIView.as_view(), name='corderitos-contenido'),
    path('contenidos/<int:contenido_id>/descargar-pdf/',DescargarPDFAPIView.as_view(),name='contenido-descargar-pdf'),
    path('calendario-activo/',CalendarioActivoAPIView.as_view(),name='calendario-activo'),
]