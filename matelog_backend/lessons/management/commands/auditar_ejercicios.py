from django.core.management.base import BaseCommand
from lessons.models import Ejercicio, OpcionMultiple
import string


class Command(BaseCommand):
    help = 'Audita ejercicios existentes para encontrar problemas de validacion'

    def handle(self, *args, **options):
        problemas = []
        total_ejercicios = Ejercicio.objects.count()

        self.stdout.write("=" * 80)
        self.stdout.write(f"Auditando {total_ejercicios} ejercicios...")
        self.stdout.write("=" * 80)

        # 1. Verificar ejercicios MULTIPLE con respuestas invalidas
        for ej in Ejercicio.objects.filter(tipo='MULTIPLE'):
            resp = ej.respuesta_correcta.strip().upper()

            # Validar letra valida
            if resp not in ['A', 'B', 'C', 'D']:
                problemas.append({
                    'id': ej.id,
                    'tema': str(ej.tema),
                    'tipo': 'RESPUESTA_INVALIDA',
                    'detalle': f'Respuesta "{ej.respuesta_correcta}" no es A, B, C, o D'
                })

            # Validar existencia de opcion
            elif not ej.opciones.filter(letra=resp).exists():
                opciones_existentes = list(ej.opciones.values_list('letra', flat=True))
                problemas.append({
                    'id': ej.id,
                    'tema': str(ej.tema),
                    'tipo': 'OPCION_NO_EXISTE',
                    'detalle': f'Respuesta correcta es "{resp}" pero solo existen opciones: {opciones_existentes}'
                })

        # 2. Verificar ejercicios con respuesta_correcta vacia
        for ej in Ejercicio.objects.filter(respuesta_correcta=''):
            problemas.append({
                'id': ej.id,
                'tema': str(ej.tema),
                'tipo': 'RESPUESTA_VACIA',
                'detalle': 'El campo respuesta_correcta esta vacio'
            })

        # 3. Verificar ejercicios ABIERTO con puntuacion al final
        for ej in Ejercicio.objects.filter(tipo='ABIERTO'):
            if ej.respuesta_correcta:
                ultima_letra = ej.respuesta_correcta[-1]
                if ultima_letra in string.punctuation:
                    problemas.append({
                        'id': ej.id,
                        'tema': str(ej.tema),
                        'tipo': 'PUNTUACION_FINAL',
                        'detalle': f'Respuesta termina en "{ultima_letra}": "{ej.respuesta_correcta}"'
                    })

        # 4. Verificar ejercicios ABIERTO con espacios extra
        for ej in Ejercicio.objects.filter(tipo='ABIERTO'):
            if ej.respuesta_correcta:
                normalizado = ' '.join(ej.respuesta_correcta.split())
                if normalizado != ej.respuesta_correcta:
                    problemas.append({
                        'id': ej.id,
                        'tema': str(ej.tema),
                        'tipo': 'ESPACIOS_EXTRA',
                        'detalle': f'Tiene espacios inconsistentes: "{ej.respuesta_correcta}"'
                    })

        # Mostrar resultados
        self.stdout.write("")
        if not problemas:
            self.stdout.write(self.style.SUCCESS('>>> No se encontraron problemas'))
        else:
            self.stdout.write(self.style.ERROR(f'>>> Se encontraron {len(problemas)} problemas:'))
            self.stdout.write("")

            # Agrupar por tipo
            tipos = {}
            for p in problemas:
                if p['tipo'] not in tipos:
                    tipos[p['tipo']] = []
                tipos[p['tipo']].append(p)

            # Mostrar por tipo
            for tipo, items in tipos.items():
                self.stdout.write(f"\n{tipo} ({len(items)} ejercicios):")
                for item in items:
                    self.stdout.write(f"  - Ejercicio ID {item['id']} ({item['tema']})")
                    self.stdout.write(f"    {item['detalle']}")

        self.stdout.write("")
        self.stdout.write("=" * 80)
        self.stdout.write(f"Auditoria completada. Total problemas: {len(problemas)}")
        self.stdout.write("=" * 80)
