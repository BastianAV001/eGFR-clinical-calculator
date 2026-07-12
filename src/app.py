import streamlit as st
from ckd_epi import calcular_egfr, clasificar_categoria_kdigo, evaluar_riesgo_contraste

st.set_page_config(page_title="Calculadora eGFR & Contraste", page_icon="⚕️", layout="centered")

st.markdown("""
    <style>
    h1, h2, h3 { color: #0A2240; }
    .stButton>button {
        background-color: #0A2240;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #C28840; color: white; }
    /* Reducir el padding superior para ganar espacio visual */
    .block-container { padding-top: 2rem; padding-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("Calculadora Clínica eGFR")
st.markdown("**Sistema de Soporte a la Decisión para Inyección de Medios de Contraste**")

tab1, tab2, tab3, tab4 = st.tabs([
    "🧮 Calculadora", 
    "📚 Fundamento Clínico", 
    "🔬 Ecuación CKD-EPI", 
    "📖 Referencias"
])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        edad = st.number_input("Edad (años)", min_value=18, max_value=120, value=40)
    with col2:
        sexo = st.selectbox("Sexo Biológico", ["Masculino", "Femenino"])
    with col3:
        scr = st.number_input("Creatinina (mg/dL)", min_value=0.1, max_value=15.0, value=1.0, step=0.1)
    
    if st.button("Evaluar Riesgo Radiológico", use_container_width=True):
        try:
            sexo_formateado = 'M' if sexo == "Masculino" else 'F'
            
            resultado_egfr = calcular_egfr(edad, scr, sexo_formateado)
            kdigo_data = clasificar_categoria_kdigo(resultado_egfr)
            riesgo_data = evaluar_riesgo_contraste(resultado_egfr)                                  
            
            st.metric(label="Tasa de Filtración Glomerular Estimada (eGFR)", value=f"{resultado_egfr} mL/min/1.73m²")
                        
            col_nefro, col_radio = st.columns(2)
            
            with col_nefro:
                st.markdown("**🩺 Nefrología (KDIGO 2012)**")                
                st.info(f"**{kdigo_data['categoria']}: {kdigo_data['descripcion']}**\n\n*{kdigo_data['estatus_erc']}*\n\n**Acción:** {kdigo_data['accion_clinica']}")
                
            with col_radio:
                st.markdown(f"**☢️ Riesgo Contraste: {riesgo_data['nivel_riesgo']}**")
                texto_radio = f"**TC (Yodo):** {riesgo_data['yodo_tc']}\n\n**RM (Gadolinio):** {riesgo_data['gadolinio_rm']}"
                
                if riesgo_data['color_alerta'] == "verde":
                    st.success(texto_radio)
                elif riesgo_data['color_alerta'] == "naranja":
                    st.warning(texto_radio)
                else:
                    st.error(texto_radio)
            
        except ValueError as e:
            st.error(f"Error en validación clínica: {e}")

with tab2:
    st.header("Fundamento Fisiológico y Clínico")
    st.write("Contenido pendiente.")

with tab3:
    st.header("La Ecuación CKD-EPI 2021")
    st.write("Contenido pendiente.")

with tab4:
    st.header("Referencias Bibliográficas")
    st.write("Contenido pendiente.")