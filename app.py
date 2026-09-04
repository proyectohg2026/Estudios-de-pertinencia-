import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Encuesta de Pertinencia - Enfermería Profesional",
    page_icon="🏥",
    layout="wide"
)

# Título y presentación
st.title("🏥 Estudio de Pertinencia - Enfermería Profesional")
st.markdown("""
### Universidad/Institución [Nombre de tu institución]
**Objetivo:** Evaluar la viabilidad de apertura del programa de Enfermería Profesional en Cali y municipios aledaños.

Sus respuestas son fundamentales para alinear la formación académica con las necesidades del sector salud.
""")

st.divider()

# Inicializar archivo de respuestas si no existe
ARCHIVO_RESPUESTAS = "datos_respuestas.csv"

# --- SECCIÓN 1: INFORMACIÓN DEL EMPLEADOR ---
st.header("📋 Información del Empleador y su Institución")

with st.form("encuesta_form"):
    # Pregunta 1
    nombre_institucion = st.text_input(
        "1. Nombre de la Institución de Salud (IPS, Clínica, Hospital, EPS, etc.)",
        placeholder="Ej: Clínica Imbanaco, Hospital Universitario del Valle, etc."
    )
    
    # Pregunta 2
    tipo_institucion = st.selectbox(
        "2. Tipo de Institución",
        [
            "Seleccione una opción",
            "Clínica / Hospital de alta complejidad (Nivel III o IV)",
            "Clínica / Hospital de mediana complejidad (Nivel II)",
            "Centro de salud / IPS de baja complejidad (Nivel I)",
            "EPS / Entidad Administradora de Planes de Beneficios",
            "Institución prestadora de servicios ambulatorios o de especialidades",
            "Empresa de servicios de salud domiciliaria",
            "Centro de atención a la salud ocupacional",
            "Otro"
        ]
    )
    
    # Pregunta 3
    municipio = st.selectbox(
        "3. Municipio donde opera principalmente su institución",
        [
            "Seleccione una opción",
            "Cali", "Palmira", "Yumbo", "Jamundí", 
            "Candelaria", "Florida", "Pradera", "Otro"
        ]
    )
    
    st.divider()
    
    # --- SECCIÓN 2: DEMANDA DE PROFESIONALES ---
    st.header("📊 Demanda de Profesionales de Enfermería")
    
    # Pregunta 4
    contrataciones = st.radio(
        "4. En los últimos 2 años, ¿cuántos profesionales de enfermería (con título de pregrado universitario) ha contratado su institución?",
        ["Ninguno", "1 a 3", "4 a 10", "Más de 10"],
        index=None
    )
    
    # Pregunta 5
    necesidad = st.radio(
        "5. Actualmente, ¿existe en su institución una necesidad insatisfecha de enfermeros profesionales?",
        ["Sí, es una necesidad alta y apremiante", "Sí, tenemos algunas vacantes", "No, actualmente la planta está cubierta", "No lo sé con certeza"],
        index=None
    )
    
    # Pregunta 6
    demanda_futura = st.radio(
        "6. A futuro (próximos 3 a 5 años), ¿cómo cree que será la demanda de enfermeros profesionales en su institución?",
        ["Aumentará considerablemente", "Aumentará ligeramente", "Se mantendrá estable", "Disminuirá", "No lo sé"],
        index=None
    )
    
    # Pregunta 7
    dificultad_contratacion = st.radio(
        "7. ¿Qué tan difícil le resulta encontrar enfermeros profesionales que cumplan con el perfil que su institución requiere?",
        ["Muy difícil, hay una escasez significativa", "Algo difícil, se requiere mucho tiempo", "Relativamente fácil, hay un número adecuado", "Muy fácil, hay muchos candidatos"],
        index=None
    )
    
    st.divider()
    
    # --- SECCIÓN 3: PERFIL Y COMPETENCIAS ---
    st.header("🎯 Perfil y Competencias Requeridas")
    
    # Pregunta 8
    nivel_formacion = st.selectbox(
        "8. Para los cargos que usted supervisa, ¿cuál es el nivel de formación deseable para un enfermero profesional?",
        [
            "Seleccione una opción",
            "Profesional Universitario (Pregrado)",
            "Especialista en un área clínica (ej. Cuidado Crítico, Urgencias, Pediatría)",
            "Con formación en diplomados o cursos de actualización específicos"
        ]
    )
    
    # Pregunta 9 - Competencias (escala 1-5)
    st.subheader("9. Clasifique la importancia de las siguientes competencias")
    st.caption("1 = Menos importante | 5 = Esencial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        competencia_clinica = st.slider("Competencias Clínicas", 1, 5, 3)
        pensamiento_critico = st.slider("Pensamiento Crítico y Juicio Clínico", 1, 5, 3)
        comunicacion = st.slider("Comunicación y Trabajo en Equipo", 1, 5, 3)
        liderazgo = st.slider("Liderazgo y Gestión del Cuidado", 1, 5, 3)
    
    with col2:
        humanizacion = st.slider("Humanización y Ética", 1, 5, 3)
        educacion_salud = st.slider("Educación para la Salud", 1, 5, 3)
        tecnologia = st.slider("Manejo de Tecnología e Informática en Salud", 1, 5, 3)
    
    # Pregunta 10 - Áreas de especialización
    st.subheader("10. ¿Cuáles de estas áreas de especialización son más demandadas? (Seleccione hasta 3)")
    areas = st.multiselect(
        "Seleccione hasta 3 opciones",
        [
            "Cuidado Crítico (UCI)",
            "Urgencias y Emergencias",
            "Quirófano y Central de Esterilización",
            "Pediatría y Neonatología",
            "Salud Mental",
            "Salud Ocupacional y del Trabajador",
            "Geriatría y Cuidados Paliativos",
            "Consulta Externa y Promoción de la Salud",
            "Otra"
        ],
        max_selections=3
    )
    
    st.divider()
    
    # --- SECCIÓN 4: PERTINENCIA Y EXPECTATIVAS ---
    st.header("📈 Pertinencia del Programa y Expectativas")
    
    # Pregunta 11
    preparacion = st.radio(
        "11. ¿Considera que los programas de formación en enfermería en la región de Cali están preparando adecuadamente a los profesionales?",
        ["Sí, totalmente", "Sí, en su mayoría", "No, creo que hay una brecha entre la teoría y la práctica", "No, existe un desfase importante con las necesidades del sector"],
        index=None
    )
    
    # Pregunta 12
    aspectos_mejorar = st.multiselect(
        "12. ¿Qué aspectos cree que un nuevo programa debería reforzar? (Seleccione hasta 3)",
        [
            "Aumentar las horas de práctica clínica en escenarios reales",
            "Fortalecer competencias en gestión y administración de servicios de salud",
            "Profundizar en el manejo de tecnologías de la información y telemedicina",
            "Incorporar un enfoque más fuerte en salud mental y comunitaria",
            "Mejorar la formación en humanización y comunicación asertiva",
            "Ofrecer énfasis en áreas críticas como UCI y urgencias",
            "Potenciar la capacidad de investigación y práctica basada en evidencia"
        ],
        max_selections=3
    )
    
    # Pregunta 13
    remuneracion = st.selectbox(
        "13. ¿Cuál es el rango de remuneración mensual (en COP) que usualmente ofrece a un enfermero profesional recién egresado?",
        [
            "Seleccione una opción",
            "Menos de $2.500.000",
            "Entre $2.500.000 y $3.200.000",
            "Entre $3.200.000 y $4.000.000",
            "Más de $4.000.000"
        ]
    )
    
    # Pregunta 14 - Texto libre
    st.subheader("14. Retos específicos del mercado laboral en la región")
    retos = st.text_area(
        "¿Existe algún reto específico (ej. alta rotación, falta de especialistas, condiciones contractuales) que un nuevo programa deba tener en cuenta?",
        placeholder="Escriba su respuesta aquí...",
        height=100
    )
    
    st.divider()
    
    # --- BOTÓN DE ENVÍO ---
    submitted = st.form_submit_button("✅ Enviar Encuesta", use_container_width=True)

# --- PROCESAMIENTO DEL FORMULARIO ---
if submitted:
    # Validar campos obligatorios
    if not nombre_institucion:
        st.error("⚠️ Por favor, ingrese el nombre de la institución.")
    elif tipo_institucion == "Seleccione una opción":
        st.error("⚠️ Por favor, seleccione el tipo de institución.")
    elif municipio == "Seleccione una opción":
        st.error("⚠️ Por favor, seleccione el municipio.")
    elif contrataciones is None:
        st.error("⚠️ Por favor, responda la pregunta 4 sobre contrataciones.")
    elif necesidad is None:
        st.error("⚠️ Por favor, responda la pregunta 5 sobre necesidad insatisfecha.")
    elif demanda_futura is None:
        st.error("⚠️ Por favor, responda la pregunta 6 sobre demanda futura.")
    elif dificultad_contratacion is None:
        st.error("⚠️ Por favor, responda la pregunta 7 sobre dificultad de contratación.")
    elif nivel_formacion == "Seleccione una opción":
        st.error("⚠️ Por favor, seleccione el nivel de formación deseable.")
    elif preparacion is None:
        st.error("⚠️ Por favor, responda la pregunta 11 sobre la preparación actual.")
    elif remuneracion == "Seleccione una opción":
        st.error("⚠️ Por favor, seleccione el rango de remuneración.")
    else:
        # Crear diccionario con respuestas
        nueva_respuesta = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nombre_Institución": nombre_institucion,
            "Tipo_Institución": tipo_institucion,
            "Municipio": municipio,
            "Contrataciones_2años": contrataciones,
            "Necesidad_Insatisfecha": necesidad,
            "Demanda_Futura": demanda_futura,
            "Dificultad_Contratación": dificultad_contratacion,
            "Nivel_Formación": nivel_formacion,
            "Competencias_Clínicas": competencia_clinica,
            "Pensamiento_Crítico": pensamiento_critico,
            "Comunicación_Equipo": comunicacion,
            "Liderazgo_Gestión": liderazgo,
            "Humanización_Ética": humanizacion,
            "Educación_Salud": educacion_salud,
            "Tecnología": tecnologia,
            "Áreas_Demanda": ", ".join(areas) if areas else "",
            "Preparación_Actual": preparacion,
            "Aspectos_Mejorar": ", ".join(aspectos_mejorar) if aspectos_mejorar else "",
            "Remuneración": remuneracion,
            "Retos_Región": retos
        }
        
        # Guardar en CSV
        df_nuevo = pd.DataFrame([nueva_respuesta])
        
        # Si el archivo no existe, crear con cabecera
        if not os.path.exists(ARCHIVO_RESPUESTAS):
            df_nuevo.to_csv(ARCHIVO_RESPUESTAS, index=False, encoding='utf-8-sig')
        else:
            df_existente = pd.read_csv(ARCHIVO_RESPUESTAS, encoding='utf-8-sig')
            df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
            df_actualizado.to_csv(ARCHIVO_RESPUESTAS, index=False, encoding='utf-8-sig')
        
        st.balloons()
        st.success("✅ ¡Encuesta enviada exitosamente! Muchas gracias por su participación.")
        st.info("📊 Sus respuestas nos ayudarán a diseñar un programa de enfermería que responda a las necesidades reales de Cali y su región.")

# --- SECCIÓN DE ADMINISTRACIÓN (VER RESPUESTAS) ---
st.divider()
with st.expander("🔐 Administración - Ver respuestas recopiladas (solo para el investigador)"):
    if os.path.exists(ARCHIVO_RESPUESTAS):
        df_respuestas = pd.read_csv(ARCHIVO_RESPUESTAS, encoding='utf-8-sig')
        st.write(f"**Total de respuestas:** {len(df_respuestas)}")
        st.dataframe(df_respuestas, use_container_width=True)
        
        # Botón para descargar CSV
        csv = df_respuestas.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Descargar respuestas como CSV",
            data=csv,
            file_name="respuestas_encuesta_enfermeria.csv",
            mime="text/csv"
        )
    else:
        st.info("Aún no hay respuestas registradas.")