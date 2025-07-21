# 🎯 Clasificación de Grupos Relacionados por el Diagnóstico (GRD)

<p align="center">
  <img src="logoU.png" alt="Logo UdeA" width="500"/>
</p>

## 📘 Proyecto 3 – Informática Médica

**Autores:**

- Daniel Barrera Mazo
- Isabella Bedoya Orozco
- Juan David Santofimio Rojas

---

## 🧠 Objetivo

El objetivo de este proyecto es construir un modelo de inteligencia artificial capaz de predecir el **GRD (Grupo Relacionado por el Diagnóstico)** a partir de registros clínicos anonimizados. El modelo busca replicar el comportamiento del _grouper_ original, asignando la etiqueta GRD más adecuada a cada paciente según sus características clínicas y administrativas.

---

## 📂 Estructura del proyecto

- **Notebook_XGBoost.ipynb:** contiene todo el flujo de desarrollo, desde la limpieza de datos hasta el entrenamiento y evaluación del modelo.
- **api/**: Carpeta con el código fuente de la API Django.
- **data/**: Datos anonimizados utilizados para el entrenamiento y pruebas.
- **requirements.txt:** Dependencias necesarias para ejecutar el proyecto.
- **README.md:** Documentación del proyecto.

---

## 🤖 Modelo y resultados

- **Modelo final:** XGBoost.
- **Train Accuracy:** 92.65%
- **Test Accuracy:** 84.98%
- **F1-score (ponderado):** 0.84

---

## 📈 Creación de la API

Se hizo una interfaz web mediante Django, donde los usuarios pueden ingresar los datos clínicos en un formulario HTML y obtener la predicción del GRD directamente en la página.

---

## 🚀 Instalación y ejecución de la API

1. Ubícate en la carpeta principal del proyecto (`Practica_3_InfoMedica`).
2. **Crea un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   ```
3. **Activa el entorno virtual**:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecuta el servidor de Django**:
   ```bash
   python manage.py runserver
   ```

Accede a la interfaz web en el enlace que aparece en la terminal al iniciar el servidor, normalmente [http://localhost:8000](http://localhost:8000).

---

## 🧪 Uso de la aplicación web

La predicción del GRD se realiza a través de un formulario HTML disponible en la interfaz web.  
**Pasos:**
1. Abre el enlace del servidor en tu navegador (por defecto [http://localhost:8000](http://localhost:8000)).
2. Llena el formulario con los datos clínicos solicitados.
3. Haz clic en "Realizar Predicción" para obtener la predicción del GRD en la misma página.

Toda la interacción se realiza desde la web, no es necesario usar herramientas como `curl`.

---

### Endpoints principales

- `/predict/`: Procesa los datos enviados desde el formulario y retorna la predicción del GRD para mostrarla en la interfaz web.

---