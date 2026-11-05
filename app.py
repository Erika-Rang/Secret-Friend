import json
import os
import random
import streamlit as st

DATA_FILE = "sorteo_data.json"

st.set_page_config(page_title="Amigo Secreto 🎁", page_icon="🎁", layout="centered")

# Funciones para persistir los datos de la app
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sorteo_realizado": False, "asignaciones": {}, "revelados": []}

def guardar_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

datos = cargar_datos()

st.title("🎁 Intercambio de Amigo Secreto")

# PESTAÑAS: Una para los invitados y otra para configurar el sorteo
tab_participante, tab_admin = st.tabs(["👤 Soy Participante", "⚙️ Organizador"])

# ---------------------------------------------------------
# VISTA DEL PARTICIPANTE
# ---------------------------------------------------------
with tab_participante:
    st.header("Descubre a tu Amigo Secreto")
    
    if not datos["sorteo_realizado"]:
        st.warning("⏳ El sorteo aún no ha sido realizado por el organizador. Vuelve a consultar más tarde.")
    else:
        participantes_disponibles = sorted(list(datos["asignaciones"].keys()))
        
        nombre_usuario = st.selectbox(
            "Selecciona tu nombre de la lista:",
            options=["-- Selecciona tu nombre --"] + participantes_disponibles
        )
        
        if nombre_usuario and nombre_usuario != "-- Selecciona tu nombre --":
            if nombre_usuario in datos["revelados"]:
                st.info("ℹ️ Ya habías consultado tu amigo secreto anteriormente.")
            
            if st.button("🔓 Revelar mi Amigo Secreto"):
                amigo_secreto = datos["asignaciones"][nombre_usuario]
                
                # Marcar como revelado para guardar registro
                if nombre_usuario not in datos["revelados"]:
                    datos["revelados"].append(nombre_usuario)
                    guardar_datos(datos)
                
                st.balloons()
                st.success(f"🤫 **{nombre_usuario}**, te tocó regalarle a: **{amigo_secreto}**")
                st.caption("Guarda bien el nombre o toma una captura de pantalla.")

# ---------------------------------------------------------
# VISTA DEL ORGANIZADOR
# ---------------------------------------------------------
with tab_admin:
    st.header("Configuración del Sorteo")
    
    # Contraseña simple para que solo tú hagas el sorteo
    clave = st.text_input("Clave de organizador:", type="password")
    
    if clave == "1234":  # Cambia esta clave por la que quieras
        st.subheader("1. Lista de Participantes")
        nombres_input = st.text_area(
            "Ingresa los nombres de todos los participantes (uno por línea):",
            placeholder="Ana\nCarlos\nBeatriz\nDavid",
            height=150
        )
        
        participantes = [n.strip() for n in nombres_input.split("\n") if n.strip()]
        
        if st.button("🎲 Realizar y Publicar Sorteo"):
            if len(participantes) < 3:
                st.error("Se necesitan al menos 3 participantes.")
            else:
                # Algoritmo de sorteo aleatorio
                asignados = participantes.copy()
                while True:
                    random.shuffle(asignados)
                    if all(p != a for p, a in zip(participantes, asignados)):
                        break
                
                # Guardar nuevo estado global
                datos["sorteo_realizado"] = True
                datos["asignaciones"] = dict(zip(participantes, asignados))
                datos["revelados"] = []
                guardar_datos(datos)
                
                st.success("🎉 ¡Sorteo realizado y guardado con éxito! Ahora tus amigos pueden entrar y consultar.")
                st.rerun()
                
        if datos["sorteo_realizado"]:
            st.divider()
            st.subheader("Estado actual del intercambio")
            st.write(f"**Progreso:** {len(datos['revelados'])} de {len(datos['asignaciones'])} personas han visto su resultado.")
            
            if st.button("🗑️ Reiniciar Sorteo"):
                guardar_datos({"sorteo_realizado": False, "asignaciones": {}, "revelados": []})
                st.warning("Sorteo reiniciado.")
                st.rerun()
    elif clave:
        st.error("Clave incorrecta.")
