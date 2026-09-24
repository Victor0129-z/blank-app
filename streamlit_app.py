import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import av

st.set_page_config(page_title="Cámara en la Nube", layout="centered")

st.title("Procesamiento de Video en la Nube ☁️📷")
st.write("Abre esta página en tu celular, otorga permisos de cámara y mira el procesamiento en tiempo real.")

# Esta función se ejecutará por CADA cuadro (frame) de video que llegue al servidor
def procesar_video(frame: av.VideoFrame) -> av.VideoFrame:
    # 1. Convertir el formato de WebRTC a un formato que OpenCV entienda (NumPy array)
    img = frame.to_ndarray(format="bgr24")

    # --- INICIO DE TU PROCESAMIENTO OPENCV ---
    
    # Convertimos la imagen a escala de grises
    grises = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicamos un filtro de detección de bordes (Canny)
    bordes = cv2.Canny(grises, 100, 200)
    
    # Volvemos a convertir a color (BGR) porque Streamlit espera una imagen de 3 canales
    img_procesada = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
    
    # --- FIN DE TU PROCESAMIENTO OPENCV ---

    # 2. Devolver el cuadro procesado al navegador
    return av.VideoFrame.from_ndarray(img_procesada, format="bgr24")

# Configurar e iniciar el componente web de la cámara
webrtc_streamer(
    key="camara-procesamiento",
    video_frame_callback=procesar_video,
    media_stream_constraints={
        "video": True, 
        "audio": False  # Apagamos el audio para ahorrar ancho de banda
    },
    rtc_configuration={  # Ayuda a mantener la conexión estable en la nube
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
