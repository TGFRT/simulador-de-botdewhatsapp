import streamlit as st
import google.generativeai as gen_ai

# Configura Streamlit
st.set_page_config(
    page_title="Analizador de Negocios - IngenIAr",
    page_icon=":bar_chart:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configuración de generación (ajustar según el modelo)
generation_config = {
    "temperature": 0.7,  # Controlar la creatividad del modelo
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
}

# Título de la web
st.title("Analizador de Negocios 📈")

# Sección de datos del negocio
st.header("Información de tu negocio")

# Cajas de texto para ingresar datos del negocio
nombre_negocio = st.text_input("Nombre del negocio")
descripcion = st.text_area("Descripción del negocio")
productos_servicios = st.text_area("Productos o servicios")
mercado = st.text_area("Mercado actual")
desafios = st.text_area("Desafíos")
metas = st.text_area("Metas")

# Crea el modelo aquí:
# Elige el modelo de Gemini (adapta según tus necesidades)
model = gen_ai.GenerativeModel(
    model_name="gemini-pro",  # Ajusta el nombre del modelo
    generation_config=generation_config,
)

# Botón para iniciar el análisis
if st.button("Analizar"):
    # Crea el modelo con instrucciones de sistema personalizadas
    system_instruction = (
        "Eres un analista de negocios experto. "
        "Analiza la información del negocio y proporciona sugerencias para mejorar, "
        "estrategias de marketing y posibles amenazas."
        "Organiza la información en tres secciones: \n"
        "* **Mejora del negocio:** \n"
        "* **Estrategias de marketing:** \n"
        "* **Amenazas potenciales:** \n"
        "Incluye ideas para reducir costos, mejorar la eficiencia, aumentar las ventas, "
        "y estrategias concretas de campañas en redes sociales."
        "Escribe las tres secciones en un solo texto con encabezados claros."
    )

    # Crea una entrada de texto con todos los datos del negocio
    datos_negocio = f"""
    Nombre del negocio: {nombre_negocio}
    Descripción: {descripcion}
    Productos/Servicios: {productos_servicios}
    Mercado actual: {mercado}
    Desafios: {desafios}
    Metas: {metas}
    """

    # Envía la información al modelo de Gemini para su análisis
    response = model.generate_text(text=datos_negocio, system_instruction=system_instruction)

    # Muestra la respuesta del modelo en un solo texto
    st.markdown(f"## Análisis de tu negocio:\n{response}")
