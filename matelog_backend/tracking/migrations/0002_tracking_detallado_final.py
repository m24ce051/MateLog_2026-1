# tracking/migrations/0002_tracking_detallado_final.py
# MIGRACIÓN COMPLETA - 8 campos nuevos en ProgresoTema

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        # ===== TRACKING DE TIEMPO (3 campos) =====
        migrations.AddField(
            model_name='progresotema',
            name='tiempo_total_teoria_segundos',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Tiempo total acumulado viendo pantallas de TEORÍA'
            ),
        ),
        migrations.AddField(
            model_name='progresotema',
            name='tiempo_total_ejemplos_segundos',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Tiempo total acumulado viendo pantallas de EJEMPLO (no incluye EJEMPLO_EXTRA)'
            ),
        ),
        migrations.AddField(
            model_name='progresotema',
            name='tiempo_total_ejemplos_extra_segundos',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Tiempo total acumulado viendo pantallas de EJEMPLO_EXTRA'
            ),
        ),
        
        # ===== TRACKING DE INTERACCIONES (5 campos) =====
        migrations.AddField(
            model_name='progresotema',
            name='clics_ver_otro_ejemplo',
            field=models.PositiveIntegerField(
                default=0,
                help_text="Cantidad de veces que hizo clic en 'Ver Otro Ejemplo'"
            ),
        ),
        migrations.AddField(
            model_name='progresotema',
            name='clics_volver_contenido',
            field=models.PositiveIntegerField(
                default=0,
                help_text="Cantidad de veces que hizo clic en '← Volver' desde contenido (teoría/ejemplos)"
            ),
        ),
        migrations.AddField(
            model_name='progresotema',
            name='clics_volver_ejercicios',
            field=models.PositiveIntegerField(
                default=0,
                help_text="Cantidad de veces que hizo clic en '← Volver al Tema' desde ejercicios"
            ),
        ),
        migrations.AddField(
            model_name='progresotema',
            name='clics_ir_a_ejercicios',
            field=models.PositiveIntegerField(
                default=0,
                help_text="Cantidad de veces que hizo clic en 'Ir a Ejercicios →'"
            ),
        ),
        migrations.AddField(
            model_name='progresotema',
            name='clics_ayuda_total',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Cantidad total de veces que solicitó ayuda en ejercicios del tema'
            ),
        ),
    ]