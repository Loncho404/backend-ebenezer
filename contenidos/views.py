from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Categoria, Contenido, Comentario, NivelCorderito, TemaCorderito, CalendarioDelMes
from .serializers import CategoriaSerializer, ContenidoSerializer, ComentarioSerializer, NivelCorderitoSerializer, TemaCorderitoSerializer, ContenidoTemaSerializer, CalendarioDelMesSerializer
from .permissions import IsAdminUserRole
from rest_framework.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]


class ContenidoListAPIView(generics.ListAPIView):
    queryset = Contenido.objects.filter(activo=True).order_by('-fecha_creacion')
    serializer_class = ContenidoSerializer
    permission_classes = [permissions.AllowAny]


class ContenidoDetailAPIView(generics.RetrieveAPIView):
    queryset = Contenido.objects.filter(activo=True)
    serializer_class = ContenidoSerializer
    permission_classes = [permissions.AllowAny]


class ContenidoCreateAPIView(generics.CreateAPIView):
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer
    permission_classes = [IsAdminUserRole]


class ComentarioListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        contenido_id = self.kwargs['contenido_id']
        return Comentario.objects.filter(
            contenido_id=contenido_id
        ).order_by('-fecha_creacion')

    def perform_create(self, serializer):
        user = self.request.user
        contenido_id = self.kwargs['contenido_id']

        if not user.activo_en_plataforma:
            raise PermissionDenied('Tu usuario no está activo en la plataforma.')

        if user.rol != 'admin' and not user.puede_comentar:
            raise PermissionDenied('No tienes permisos para comentar.')

        serializer.save(
            usuario=user,
            contenido_id=contenido_id
        )


class ResponderComentarioAPIView(generics.UpdateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAdminUserRole]

    def patch(self, request, *args, **kwargs):
        comentario = self.get_object()
        respuesta = request.data.get('respuesta')

        if not respuesta:
            return Response({'error': 'Respuesta requerida'}, status=status.HTTP_400_BAD_REQUEST)

        comentario.respuesta = respuesta
        comentario.respondido_por = request.user
        comentario.save()

        return Response({'mensaje': 'Respuesta guardada'}, status=status.HTTP_200_OK)

class NivelCorderitoListAPIView(generics.ListAPIView):
    queryset = NivelCorderito.objects.filter(activo=True).order_by('orden', 'id')
    serializer_class = NivelCorderitoSerializer
    permission_classes = [permissions.AllowAny]


class TemaPorNivelListAPIView(generics.ListAPIView):
    serializer_class = TemaCorderitoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        nivel_id = self.kwargs['nivel_id']
        return TemaCorderito.objects.filter(
            nivel_id=nivel_id,
            activo=True
        ).order_by('orden', 'id')


class ContenidoPorTemaDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ContenidoTemaSerializer
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = 'tema_id'

    def get_object(self):
        tema_id = self.kwargs['tema_id']
        return Contenido.objects.get(tema_id=tema_id, activo=True)

class DescargarPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contenido_id):
        try:
            contenido = Contenido.objects.get(id=contenido_id, activo=True)
        except Contenido.DoesNotExist:
            raise Http404("Contenido no encontrado")

        user = request.user

        if user.rol != 'admin' and not user.puede_descargar_pdfs:
            return Response(
                {'detail': 'No tienes permisos para descargar este PDF.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not contenido.pdf:
            return Response(
                {'detail': 'Este contenido no tiene PDF asociado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return FileResponse(
            contenido.pdf.open('rb'),
            as_attachment=True,
            filename=contenido.pdf.name.split('/')[-1]
        )

class CalendarioActivoAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        calendario = CalendarioDelMes.objects.filter(activo=True).first()

        if not calendario:
            return Response(
                {'detail': 'No hay calendario activo.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CalendarioDelMesSerializer(calendario)
        return Response(serializer.data)