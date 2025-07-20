import os
import joblib
from threading import Lock

_model = None
_encoder = None
_model_lock = Lock()
_encoder_lock = Lock()

def get_model():
    """Carga el modelo de predicción si no está cargado y lo devuelve."""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:  # doble chequeo
                base_dir = os.path.dirname(os.path.abspath(__file__))
                model_path = os.path.join(base_dir, 'model_store', 'best_model.pkl')
                _model = joblib.load(model_path)
    return _model

def get_label_encoder():
    """Carga el LabelEncoder si no está cargado y lo devuelve."""
    global _encoder
    if _encoder is None:
        with _encoder_lock:
            if _encoder is None:  # doble chequeo
                base_dir = os.path.dirname(os.path.abspath(__file__))
                encoder_path = os.path.join(base_dir, 'model_store', 'label_encoder.pkl')
                _encoder = joblib.load(encoder_path)
    return _encoder
