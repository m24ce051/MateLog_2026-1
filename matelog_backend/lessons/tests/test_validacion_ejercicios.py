from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Ejercicio, Tema, Leccion, OpcionMultiple


class EjercicioValidacionTestCase(TestCase):
    def setUp(self):
        """Configurar datos de prueba"""
        self.leccion = Leccion.objects.create(
            orden=1,
            titulo="Leccion de Prueba",
            descripcion="Descripcion de prueba"
        )
        self.tema = Tema.objects.create(
            leccion=self.leccion,
            orden=1,
            titulo="Tema de Prueba",
            descripcion="Descripcion de prueba"
        )

    def test_validacion_respuesta_multiple_valida(self):
        """Respuesta correcta valida (A, B, C, D) debe aceptarse"""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='MULTIPLE',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="a"  # Se normalizara a "A"
        )

        # Crear opcion multiple correspondiente
        OpcionMultiple.objects.create(
            ejercicio=ejercicio,
            letra='A',
            texto='Opcion A'
        )

        # Recargar el ejercicio para verificar normalizacion
        ejercicio.refresh_from_db()
        self.assertEqual(ejercicio.respuesta_correcta, "A")

    def test_validacion_respuesta_multiple_invalida(self):
        """Respuesta correcta invalida (no A, B, C, D) debe rechazarse"""
        with self.assertRaises(ValidationError):
            ejercicio = Ejercicio.objects.create(
                tema=self.tema,
                orden=1,
                tipo='MULTIPLE',
                dificultad='FACIL',
                instruccion="Test",
                enunciado="Test",
                respuesta_correcta="X"  # Invalida
            )

    def test_validacion_respuesta_vacia(self):
        """Respuesta correcta vacia debe rechazarse"""
        with self.assertRaises(ValidationError):
            ejercicio = Ejercicio.objects.create(
                tema=self.tema,
                orden=1,
                tipo='ABIERTO',
                dificultad='FACIL',
                instruccion="Test",
                enunciado="Test",
                respuesta_correcta=""  # Vacia
            )

    def test_normalizacion_respuesta_abierta(self):
        """Normalizacion debe manejar mayusculas, espacios y tildes"""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='ABIERTO',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="La Derivada"
        )

        # Todas estas deben ser correctas
        self.assertTrue(ejercicio.validar_respuesta("la derivada"))
        self.assertTrue(ejercicio.validar_respuesta("LA DERIVADA"))
        self.assertTrue(ejercicio.validar_respuesta("  la   derivada  "))

    def test_normalizacion_sin_puntuacion(self):
        """Normalizacion debe eliminar puntuacion"""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='ABIERTO',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="la derivada"
        )

        # Con puntuacion tambien debe aceptarse
        self.assertTrue(ejercicio.validar_respuesta("la derivada."))
        self.assertTrue(ejercicio.validar_respuesta("la derivada!"))
        self.assertTrue(ejercicio.validar_respuesta("la derivada?"))

    def test_normalizacion_sin_tildes(self):
        """Normalizacion debe eliminar tildes"""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='ABIERTO',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="derivacion"
        )

        # Con y sin tildes debe aceptarse
        self.assertTrue(ejercicio.validar_respuesta("derivacion"))
        self.assertTrue(ejercicio.validar_respuesta("derivación"))

    def test_normalizacion_multiple_a_mayuscula(self):
        """Respuestas MULTIPLE deben normalizarse a mayuscula"""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='MULTIPLE',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="b"  # Minuscula
        )

        # Crear opcion B
        OpcionMultiple.objects.create(
            ejercicio=ejercicio,
            letra='B',
            texto='Opcion B'
        )

        # Recargar y verificar normalizacion
        ejercicio.refresh_from_db()
        self.assertEqual(ejercicio.respuesta_correcta, "B")

    def test_normalizacion_abierto_espacios(self):
        """Respuestas ABIERTO deben normalizar espacios"""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='ABIERTO',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="  la   derivada  "  # Espacios extra
        )

        # Recargar y verificar normalizacion
        ejercicio.refresh_from_db()
        self.assertEqual(ejercicio.respuesta_correcta, "la derivada")

    def test_validacion_opcion_no_existe(self):
        """No se debe poder guardar ejercicio MULTIPLE si la opcion no existe"""
        # Crear ejercicio con opcion A
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            orden=1,
            tipo='MULTIPLE',
            dificultad='FACIL',
            instruccion="Test",
            enunciado="Test",
            respuesta_correcta="A"
        )

        # Crear opcion A
        OpcionMultiple.objects.create(
            ejercicio=ejercicio,
            letra='A',
            texto='Opcion A'
        )

        # Intentar cambiar a C sin crear la opcion
        ejercicio.respuesta_correcta = "C"

        with self.assertRaises(ValidationError):
            ejercicio.save()
