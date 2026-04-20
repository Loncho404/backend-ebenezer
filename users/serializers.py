from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            rol='usuario',
            puede_descargar_pdfs=False,
            puede_comentar=False,
            activo_en_plataforma=True,
        )
        return user

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'rol',
            'puede_descargar_pdfs',
            'puede_comentar',
            'activo_en_plataforma',
        ]