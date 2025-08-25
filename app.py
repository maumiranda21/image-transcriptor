import streamlit as st
from PIL import Image
import pytesseract
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Transcriptor de Imágenes (OCR)",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Estilos CSS para el modo noche ---
st.markdown("""
<style>
    body {
        color: #fafafa; /* Color de texto principal */
        background-color: #0e1117; /* Color de fondo principal */
    }
    .stApp {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #0068c9; /* Azul brillante para botones */
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        border: 1px solid #0068c9;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0055a4;
        border-color: #0055a4;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.4);
    }
    .stFileUploader label, .stTextArea label, .stSelectbox label {
        color: #fafafa !important; /* Asegura que las etiquetas sean blancas */
        font-size: 1.1rem;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #2196F3; /* Azul claro para los títulos */
    }
    /* Estilo para el área de texto */
    .stTextArea textarea {
        background-color: #262730;
        color: #fafafa;
        border: 1px solid #3c3f44;
    }
    /* Estilo para el selectbox */
    .stSelectbox > div > div {
        background-color: #262730;
        color: #fafafa;
    }
    /* Cambia el color del texto de la leyenda de la imagen */
    .stImage figcaption {
        color: #a0a0a0;
    }
</style>
""", unsafe_allow_html=True)


# --- Funciones Principales ---

def perform_ocr(image_object, lang='eng'):
    """
    Realiza el reconocimiento óptico de caracteres en un objeto de imagen.
    """
    try:
        # Pytesseract funciona directamente con objetos de imagen de Pillow
        text = pytesseract.image_to_string(image_object, lang=lang)
        return text
    except pytesseract.TesseractNotFoundError:
        st.error(
            "Error de Tesseract: El motor OCR no está instalado o no se encuentra en la ruta del sistema. "
            "Asegúrate de que el archivo 'packages.txt' esté configurado correctamente para el despliegue en Streamlit Cloud."
        )
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado durante el proceso de OCR: {e}")
        return None


# --- Interfaz de la Aplicación ---

st.title("📷 Transcriptor de Imágenes a Texto (OCR)")

st.markdown("""
Sube una imagen para extraer su texto. Esta herramienta te permite **visualizar, editar y descargar** el contenido de forma sencilla.
""")

# Selección de idioma para el OCR
st.header("1. Selecciona el Idioma del Texto")
language_options = {
    'Español': 'spa',
    'Inglés': 'eng'
}
selected_language_name = st.selectbox(
    "Elige el idioma del texto contenido en la imagen para mejorar la precisión:",
    options=list(language_options.keys())
)
language_code = language_options[selected_language_name]

# Carga de la imagen
st.header("2. Sube tu Imagen")
uploaded_file = st.file_uploader(
    "Arrastra y suelta una imagen aquí, o haz clic para seleccionarla.",
    type=["png", "jpg", "jpeg", "bmp", "tiff"]
)


# --- Lógica de Procesamiento ---

if uploaded_file is not None:
    # Mostrar la imagen subida
    try:
        image = Image.open(uploaded_file)
        
        # Usamos un contenedor para organizar mejor la imagen
        with st.container():
            st.image(image, caption=f'Imagen subida: {uploaded_file.name}', use_column_width=True)

        # Botón para iniciar el proceso de OCR
        if st.button(f"✨ Extraer Texto en {selected_language_name}"):
            with st.spinner('Procesando la imagen, por favor espera...'):
                extracted_text = perform_ocr(image, lang=language_code)

            if extracted_text:
                st.session_state.extracted_text = extracted_text
            else:
                st.warning("No se pudo extraer texto de la imagen o el texto está vacío.")
                st.session_state.extracted_text = ""

    except Exception as e:
        st.error(f"No se pudo abrir el archivo de imagen. ¿Estás seguro de que es un formato válido? Error: {e}")

# Mostrar el área de texto y el botón de descarga si hay texto extraído
if 'extracted_text' in st.session_state and st.session_state.extracted_text:
    st.header("3. Visualiza y Descarga el Texto")
    
    # Área de texto para visualizar y editar
    text_area_content = st.text_area(
        "Texto extraído (puedes editarlo aquí antes de descargar):",
        value=st.session_state.extracted_text,
        height=300
    )

    # Botón de descarga
    st.download_button(
        label="📥 Descargar Texto (.txt)",
        data=text_area_content.encode('utf-8'),
        file_name=f'texto_extraido_{uploaded_file.name}.txt',
        mime='text/plain'
    )

st.markdown("---")
st.markdown("Hecho con ❤️ usando **Streamlit** y **Tesseract**.")
