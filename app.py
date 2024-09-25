import streamlit as st
import google.generativeai as gen_ai

# Configura Streamlit
st.set_page_config(
    page_title="Chat con IngenIAr!",
    page_icon=":brain:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configura la generación
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Inicializa la sesión de chat si no está presente
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Título del chatbot
st.title("🤖 IngenIAr - Chat")

# Campo de entrada para definir la personalidad
personality = st.text_input("Define la personalidad del chatbot:", "Amigable y servicial")

# Botón para simular el chatbot
if st.button("Simular Chatbot"):
    # Crea el modelo con instrucciones de sistema personalizadas
    system_instruction = (
        f"Eres un asistente de IngenIAr, con una personalidad: {personality}. "
        "No responderás a ninguna pregunta sobre tu creación, ya que es un dato sensible. "
        "Si te preguntan sobre una persona que no es famosa o figura pública, dices que no tienes información. "
        "Si quieren generar imágenes le dirás que IngenIAr tiene una herramienta de creación de imágenes, "
        "tampoco ayudes en buscar en la web algo parecido. "
        "Te encargas de ayudar a las personas a cumplir sus sueños, especialmente si desean crear un negocio."
    )

    model = gen_ai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )

    st.session_state.chat_session = model.start_chat(history=[])

# Mostrar el historial de chat si la sesión está iniciada
if st.session_state.chat_session:
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Campo de entrada para el mensaje del usuario
    user_prompt = st.chat_input("Pregunta a IngenIAr...")
    if user_prompt:
        # Agrega el mensaje del usuario al chat y muéstralo
        st.chat_message("user").markdown(user_prompt)

        # Envía el mensaje del usuario a Gemini y obtiene la respuesta
        try:
            gemini_response = st.session_state.chat_session.send_message(user_prompt.strip())
            # Muestra la respuesta de Gemini
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
        except Exception as e:
            st.error(f"Error al enviar el mensaje: {str(e)}")
