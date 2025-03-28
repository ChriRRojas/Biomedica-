#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, data, gui
import random
import csv
from datetime import datetime

# Configuración del experimento
def create_sart_experiment():
    # Términos y Condiciones (formateado para mejor legibilidad)
    terms_text = """
    **Términos y Condiciones para la Prueba SART**

    La información recopilada durante esta prueba será 
    utilizada únicamente con fines académicos, específicamente 
    para la materia de Neurociencia en el CUCEI (Centro 
    Universitario de Ciencias Exactas e Ingenierías).

    Todos los datos proporcionados serán tratados de manera 
    confidencial y no se compartirán con terceros bajo 
    ninguna circunstancia. La información será manejada de 
    forma segura y anónima, garantizando el respeto a la 
    privacidad de los participantes.

    La participación en esta prueba es completamente voluntaria, 
    y los participantes tienen el derecho de retirarse en 
    cualquier momento sin consecuencias.

    Al continuar con la prueba, se entiende que el participante 
    acepta estos términos y condiciones.

    Presione ESPACIO para ACEPTAR o ESC para SALIR
    """

    # Configuración de la ventana para términos
    win_terms = visual.Window(
        size=[800, 600], 
        color='black',  
        units='pix', 
        fullscr=False
    )

    # Mostrar términos y condiciones
    terms_stim = visual.TextStim(
        win_terms, 
        text=terms_text, 
        color='white', 
        height=20, 
        wrapWidth=700,
        alignText='center'
    )
    terms_stim.draw()
    win_terms.flip()

    # Esperar aceptación o rechazo
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        win_terms.close()
        core.quit()
    
    win_terms.close()

    # Diálogo para información del participante
    participant_info = {
        'Nombre': '',
        'Edad': '',
        'Género': ['Masculino', 'Femenino', 'Otro']
    }
    dlg = gui.DlgFromDict(participant_info, title='Información del Participante')
    
    if not dlg.OK:
        core.quit()

    # Parámetros del experimento
    total_trials = 50
    go_probability = 0.65
    no_go_number = 9

    # Configuración de la ventana
    win = visual.Window(
        size=[0, 0],  
        color=[0.9, 0.9, 1],  
        units='pix', 
        fullscr=True
    )

    # Paleta de colores con degradados y combinaciones más sofisticadas
    color_palette = [
        '#3498db',    # Azul plano
        '#e74c3c',    # Rojo suave
        '#2ecc71',    # Verde esmeralda
        '#9b59b6',    # Púrpura
        '#f39c12',    # Naranja dorado
        '#1abc9c',    # Turquesa
        '#34495e'     # Gris azulado oscuro
    ]

    # Fuentes para añadir variabilidad
    font_list = [
        'Arial', 
        'Times New Roman', 
        'Courier', 
        'Comic Sans MS', 
        'Impact', 
        'Verdana', 
        'Georgia'
    ]

    # Estímulo de fijación con un diseño más estilizado
    fix_cross = visual.TextStim(
        win, 
        text='+', 
        color='black', 
        height=50,
        bold=True
    )

    # Estímulo de número con fuente y estilo dinámicos
    number_stim = visual.TextStim(
        win, 
        color='black', 
        height=120,
        bold=True
    )

    # Instrucciones actualizadas
    instructions = visual.TextStim(
        win, 
        text='Presiona ESPACIO para cualquier número EXCEPTO 9\nSi ves un 9, NO presiones nada\nPresiona ESPACIO para comenzar', 
        color='black', 
        height=35, 
        wrapWidth=600,
        alignText='center'
    )

    # Pantalla de resultados
    def create_results_text(total_trials, total_correct):
        return f"""
        Fin del Experimento
        
        Total de Ensayos: {total_trials}
        Respuestas Correctas: {total_correct}
        Precisión: {total_correct/total_trials*100:.2f}%
        
        Presiona ESPACIO para salir
        """

    # Preparar archivos de registro
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'SART_data_{participant_info["Nombre"]}_{timestamp}'
    
    # Crear archivos CSV para datos
    data_file = open(f'{filename}_trials.csv', 'w', newline='')
    data_writer = csv.writer(data_file)
    data_writer.writerow(['Nombre', 'Género', 'Edad', 'Trial', 'Number', 'Number_Color', 'Font', 'Is_NoGo', 'Response', 'RT', 'Correct'])

    # Preparar lista de números para los ensayos
    trial_numbers = []
    for _ in range(total_trials):
        if random.random() < go_probability:
            trial_number = no_go_number
            is_no_go = True
        else:
            trial_number = random.choice([num for num in range(1, 10) if num != no_go_number])
            is_no_go = False
        
        number_color = random.choice(color_palette)
        number_font = random.choice(font_list)
        
        trial_numbers.append((trial_number, is_no_go, number_color, number_font))

    # Mostrar instrucciones
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    # Variables para el seguimiento
    total_correct = 0
    total_responses = 0

    # Bucle de ensayos
    for trial_num, (number, is_no_go, number_color, number_font) in enumerate(trial_numbers, 1):
        # Cruz de fijación más corta
        fix_cross.draw()
        win.flip()
        core.wait(0.2)  # Reducido aún más

        # Presentar número con fuente dinámica
        number_stim.text = str(number)
        number_stim.color = number_color
        number_stim.font = number_font
        number_stim.draw()
        win.flip()

        # Tiempo de respuesta aún más reducido
        timer = core.Clock()
        keys = event.waitKeys(
            maxWait=1.0,  # Reducido de 1.2 a 1.0 segundos 
            keyList=['space', 'escape'], 
            timeStamped=timer
        )

        # Procesar respuesta
        if keys is None:
            if is_no_go:
                response = 'No Response'
                is_correct = True
                rt = None
            else:
                response = 'No Response'
                is_correct = False
                rt = None
        else:
            key, rt = keys[0]
            
            if key == 'escape':
                data_file.close()
                win.close()
                core.quit()
            
            if is_no_go:
                response = 'Responded'
                is_correct = False
            else:
                response = 'Responded'
                is_correct = True

        # Actualizar contadores
        if is_correct:
            total_correct += 1
        total_responses += 1

        # Registrar datos del ensayo
        data_writer.writerow([
            participant_info['Nombre'],
            participant_info['Género'],
            participant_info['Edad'],
            trial_num, 
            number, 
            number_color,
            number_font,
            is_no_go, 
            response, 
            rt, 
            is_correct
        ])

        # Intervalo entre ensayos más corto
        core.wait(0.2)  # Reducido aún más

    # Pantalla de resultados
    results_stim = visual.TextStim(
        win, 
        text=create_results_text(total_trials, total_correct), 
        color='black', 
        height=30, 
        wrapWidth=600,
        alignText='center'
    )
    results_stim.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    # Cerrar archivos y ventana
    data_file.close()
    win.close()
    core.quit()

# Ejecutar el experimento
if __name__ == "__main__":
    create_sart_experiment()