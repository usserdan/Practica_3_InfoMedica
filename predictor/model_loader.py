import os
import joblib
from threading import Lock

_model = None
_model_lock = Lock()

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
