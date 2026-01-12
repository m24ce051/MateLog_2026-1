from django.core.management.base import BaseCommand
from lessons.models import Ejercicio
import string


class Command(BaseCommand):
    help = 'Corrige automaticamente problemas comunes en ejercicios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra que se corregiria sin hacer cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        correcciones = 0

        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: No se haran cambios reales'))

        self.stdout.write("=" * 80)
        self.stdout.write("Corrigiendo ejercicios...")
        self.stdout.write("=" * 80)

        # 1. Normalizar respuestas MULTIPLE a mayuscula
        for ej in Ejercicio.objects.filter(tipo='MULTIPLE'):
            original = ej.respuesta_correcta
            normalizado = ej.respuesta_correcta.strip().upper()

            if original != normalizado and normalizado in ['A', 'B', 'C', 'D']:
                self.stdout.write(f"Ejercicio {ej.id}: '{original}' -> '{normalizado}'")
                if not dry_run:
                    # Actualizar directamente sin llamar a save() para evitar full_clean()
                    Ejercicio.objects.filter(pk=ej.pk).update(respuesta_correcta=normalizado)
                correcciones += 1

        # 2. Quitar espacios extra en respuestas ABIERTO
        for ej in Ejercicio.objects.filter(tipo='ABIERTO'):
            original = ej.respuesta_correcta
            normalizado = ' '.join(ej.respuesta_correcta.split()).strip()

            if original != normalizado:
                self.stdout.write(f"Ejercicio {ej.id}: espacios normalizados")
                self.stdout.write(f"  Antes: '{original}'")
                self.stdout.write(f"  Despues: '{normalizado}'")
                if not dry_run:
                    # Actualizar directamente sin llamar a save() para evitar full_clean()
                    Ejercicio.objects.filter(pk=ej.pk).update(respuesta_correcta=normalizado)
                correcciones += 1

        # 3. Quitar puntuacion final en respuestas ABIERTO (opcional)
        for ej in Ejercicio.objects.filter(tipo='ABIERTO'):
            if ej.respuesta_correcta and ej.respuesta_correcta[-1] in '.!?':
                original = ej.respuesta_correcta
                sin_puntuacion = ej.respuesta_correcta.rstrip('.!?')

                self.stdout.write(f"Ejercicio {ej.id}: puntuacion final eliminada")
                self.stdout.write(f"  Antes: '{original}'")
                self.stdout.write(f"  Despues: '{sin_puntuacion}'")
                if not dry_run:
                    # Actualizar directamente sin llamar a save() para evitar full_clean()
                    Ejercicio.objects.filter(pk=ej.pk).update(respuesta_correcta=sin_puntuacion)
                correcciones += 1

        self.stdout.write("")
        self.stdout.write("=" * 80)
        if dry_run:
            self.stdout.write(f"Se CORREGIRIAN {correcciones} ejercicios")
        else:
            self.stdout.write(self.style.SUCCESS(f'>>> Se corrigieron {correcciones} ejercicios'))
        self.stdout.write("=" * 80)
