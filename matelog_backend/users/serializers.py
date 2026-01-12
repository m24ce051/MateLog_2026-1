from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from ml_adaptive.models import CodigoAcceso




class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de nuevos usuarios.
    Incluye validación de código de participación para MateLog-AE.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    codigo_participacion = serializers.CharField(
        write_only=True,
        required=True,
        max_length=10,
        help_text="Código de participación proporcionado por el investigador (LMB o MLZ)"
    )


    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password_confirm', 'codigo_participacion', 'grupo', 'especialidad', 'genero', 'edad')


    def validate_codigo_participacion(self, value):
        """
        Valida que el código de participación sea válido y esté activo.
        """
        codigo = value.strip().upper()

        try:
            codigo_obj = CodigoAcceso.objects.get(codigo=codigo, activo=True)
        except CodigoAcceso.DoesNotExist:
            raise serializers.ValidationError(
                "Código de participación inválido. Por favor, verifica con tu instructor."
            )

        return codigo


    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password_confirm": "Las contraseñas no coinciden."
            })
        return attrs


    def create(self, validated_data):
        # Extraer el código antes de crear el usuario
        codigo_participacion = validated_data.pop('codigo_participacion')
        validated_data.pop('password_confirm')

        # Crear el usuario
        user = CustomUser.objects.create_user(**validated_data)

        # Obtener el código de acceso para asignar el grupo
        codigo_obj = CodigoAcceso.objects.get(codigo=codigo_participacion, activo=True)

        # Crear el perfil de usuario con el grupo asignado
        from ml_adaptive.models import PerfilUsuario
        PerfilUsuario.objects.create(
            user=user,
            grupo=codigo_obj.grupo,
            codigo_usado=codigo_participacion
        )

        return user




class UserLoginSerializer(serializers.Serializer):
    """
    Serializer para el inicio de sesión.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )




class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar el perfil del usuario.
    Incluye los valores display de los campos con choices.
    Incluye información del grupo experimental (MateLog-AE).
    """
    grupo_display = serializers.CharField(source='get_grupo_display', read_only=True)
    especialidad_display = serializers.CharField(source='get_especialidad_display', read_only=True)
    genero_display = serializers.CharField(source='get_genero_display', read_only=True)
    edad_display = serializers.CharField(source='get_edad_display', read_only=True)

    # MateLog-AE: Información del perfil experimental
    grupo_experimental = serializers.SerializerMethodField()
    clasificacion_autoeficacia = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'grupo',
            'grupo_display',
            'especialidad',
            'especialidad_display',
            'genero',
            'genero_display',
            'edad',
            'edad_display',
            'date_joined',
            'grupo_experimental',
            'clasificacion_autoeficacia'
        )

    def get_grupo_experimental(self, obj):
        """Retorna el grupo experimental del usuario (CONTROL o EXPERIMENTAL)."""
        try:
            return obj.perfil.grupo
        except:
            return None

    def get_clasificacion_autoeficacia(self, obj):
        """Retorna la clasificación de autoeficacia del usuario."""
        try:
            return obj.perfil.clasificacion_autoeficacia
        except:
            return None




class ChoicesSerializer(serializers.Serializer):
    """
    Serializer para exponer las opciones de choices en la API.
    Permite que el frontend cargue dinámicamente las opciones de los dropdowns.
    """
    def to_representation(self, instance):
        from users.models import GRUPO_CHOICES, ESPECIALIDAD_CHOICES, GENERO_CHOICES, EDAD_CHOICES
       
        return {
            'grupos': [{'value': value, 'label': label} for value, label in GRUPO_CHOICES],
            'especialidades': [{'value': value, 'label': label} for value, label in ESPECIALIDAD_CHOICES],
            'generos': [{'value': value, 'label': label} for value, label in GENERO_CHOICES],
            'edades': [{'value': value, 'label': label} for value, label in EDAD_CHOICES],
        }


