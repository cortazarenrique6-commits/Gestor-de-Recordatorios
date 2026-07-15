
import streamlit as st
import pandas as pd
import time
import base64

# Título de la aplicación
st.title('Aplicación de Temporizador de Tareas')

# Inicializar lista_tareas en st.session_state si no existe
if 'lista_tareas' not in st.session_state:
    st.session_state.lista_tareas = []

# URL del audio de notificación (usando el valor de tu entorno)
url_audio = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'

# --- Sección para Agregar Tareas ---
st.header('Agregar Nueva Tarea')

tarea_input = st.text_input('Nombre de la Tarea:')
segundos_slider = st.slider('Duración (segundos):', min_value=1, max_value=60, value=5)

if st.button('Agregar Tarea'):
    if tarea_input and segundos_slider > 0:
        st.session_state.lista_tareas.append({
            'Tarea': tarea_input,
            'Duración (segundos)': segundos_slider
        })
        st.success(f'Tarea "{tarea_input}" agregada.')
        # Limpiar el campo de entrada después de agregar
        tarea_input = '' # Esto no limpia el widget directamente, pero se refrescará en la siguiente ejecución
    else:
        st.warning('Por favor, ingresa una tarea y una duración válida.')

# --- Sección para Ver Tareas ---
st.header('Tareas Guardadas')

if st.session_state.lista_tareas:
    df_tareas = pd.DataFrame(st.session_state.lista_tareas)
    st.dataframe(df_tareas, use_container_width=True)
else:
    st.info('No hay tareas guardadas.')

# --- Sección para Iniciar Temporizador ---
st.header('Iniciar Temporizador')

opciones_tareas_iniciar = [''] + [f"{i+1}. {t['Tarea']} ({t['Duración (segundos)']}s)" for i, t in enumerate(st.session_state.lista_tareas)]
tarea_seleccionada_iniciar = st.selectbox('Selecciona una tarea para iniciar:', opciones_tareas_iniciar)

# Placeholder para el contador
countdown_placeholder = st.empty()

if st.button('Iniciar Temporizador Seleccionado'):
    if tarea_seleccionada_iniciar:
        indice_seleccionado = int(tarea_seleccionada_iniciar.split('.')[0]) - 1
        if 0 <= indice_seleccionado < len(st.session_state.lista_tareas):
            tarea_para_iniciar = st.session_state.lista_tareas[indice_seleccionado]
            st.write(f"⌛ Iniciando: '{tarea_para_iniciar['Tarea']}' por {tarea_para_iniciar['Duración (segundos)']} segundos...")

            # Contador visual en tiempo real
            with countdown_placeholder.container():
                for i in range(tarea_para_iniciar['Duración (segundos)'], 0, -1):
                    st.metric(label="Tiempo restante:", value=f"{i} segundos")
                    time.sleep(1)
                st.metric(label="Tiempo restante:", value="0 segundos")

            # Limpiar el placeholder después del conteo
            countdown_placeholder.empty()

            # Notificación visual
            st.markdown(f"<h2 style='color: green;'>🔔 ¡TIEMPO CUMPLIDO: {tarea_para_iniciar['Tarea']}!</h2>", unsafe_allow_html=True)

            # Notificación de audio
            st.markdown(f"<audio autoplay><source src='{url_audio}' type='audio/mp3'></audio>", unsafe_allow_html=True)
            st.balloons() # Pequeña celebración
        else:
            st.error('Error al seleccionar la tarea.')
    else:
        st.warning('Por favor, selecciona una tarea para iniciar el temporizador.')

# --- Sección para Eliminar Tareas ---
st.header('Eliminar Tarea')

opciones_tareas_eliminar = [''] + [f"{i+1}. {t['Tarea']} ({t['Duración (segundos)']}s)" for i, t in enumerate(st.session_state.lista_tareas)]
tarea_seleccionada_eliminar = st.selectbox('Selecciona una tarea para eliminar:', opciones_tareas_eliminar)

if st.button('Eliminar Tarea Seleccionada'):
    if tarea_seleccionada_eliminar:
        indice_a_eliminar = int(tarea_seleccionada_eliminar.split('.')[0]) - 1
        if 0 <= indice_a_eliminar < len(st.session_state.lista_tareas):
            tarea_eliminada = st.session_state.lista_tareas.pop(indice_a_eliminar)
            st.success(f"Tarea '{tarea_eliminada['Tarea']}' eliminada.")
            # Actualizar la vista (Streamlit refrescará la página)
        else:
            st.error('Índice de tarea inválido para eliminar.')
    else:
        st.warning('Selecciona una tarea para eliminar.')
