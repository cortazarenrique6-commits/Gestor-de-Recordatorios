import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Gestor de Recordatorios", page_icon="✅")
st.title('✅ Gestor de Recordatorios')

# Inicializar estado
if 'lista_tareas' not in st.session_state:
    st.session_state.lista_tareas = []

# --- Funciones (Callbacks) ---
def agregar_tarea():
    if st.session_state.nueva_tarea and st.session_state.segundos_slider > 0:
        st.session_state.lista_tareas.append({
            'Tarea': st.session_state.nueva_tarea,
            'Duración (segundos)': st.session_state.segundos_slider
        })
        st.session_state.nueva_tarea = "" # Limpia el campo correctamente

# --- Sección Agregar ---
st.header('Agregar Nueva Tarea')
st.text_input('Nombre de la Tarea:', key='nueva_tarea')
st.slider('Duración (segundos):', min_value=1, max_value=60, value=5, key='segundos_slider')
st.button('Agregar Tarea', on_click=agregar_tarea)

# --- Sección Ver ---
st.header('Tareas Guardadas')
if st.session_state.lista_tareas:
    st.dataframe(pd.DataFrame(st.session_state.lista_tareas), use_container_width=True)

# --- Sección Iniciar ---
st.header('Iniciar Temporizador')
opciones = [f"{i+1}. {t['Tarea']}" for i, t in enumerate(st.session_state.lista_tareas)]
seleccion = st.selectbox('Elige tarea:', [''] + opciones)

if st.button('Iniciar'):
    if seleccion:
        idx = int(seleccion.split('.')[0]) - 1
        duracion = st.session_state.lista_tareas[idx]['Duración (segundos)']
        
        # Conteo visual
        placeholder = st.empty()
        for i in range(duracion, 0, -1):
            placeholder.metric("Tiempo restante:", f"{i}s")
            time.sleep(1)
        placeholder.empty()
        st.success(f"¡Tiempo cumplido para: {st.session_state.lista_tareas[idx]['Tarea']}!")
        st.balloons()
