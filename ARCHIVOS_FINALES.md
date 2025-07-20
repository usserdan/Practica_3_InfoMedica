## ARCHIVOS NECESARIOS PARA EJECUTAR LA APLICACIÓN

### Archivos del proyecto principal:

- manage.py - gestor de comandos django
- db.sqlite3 - base de datos
- logoU.png - logo de la universidad
- requirments.txt - dependencias del proyecto

### Carpeta infomedica_api/:

- **init**.py - paquete python
- settings.py - configuración django
- urls.py - rutas principales
- wsgi.py - configuración wsgi
- asgi.py - configuración asgi

### Carpeta predictor/:

- **init**.py - paquete python
- admin.py - configuración admin django
- apps.py - configuración aplicación
- models.py - modelos django
- views.py - lógica de vistas (limpiado)
- forms.py - formularios django (limpiado)
- urls.py - rutas de la aplicación
- serializers.py - serializadores rest api
- tests.py - pruebas unitarias
- features.py - lista de características del modelo (limpiado)
- model_loader.py - carga del modelo ml (limpiado)
- codigo_choices_final.json - códigos válidos para formularios
- migrations/ - migraciones base de datos
- model_store/best_model.pkl - modelo entrenado
- model_store/label_encoder.pkl - codificador de etiquetas

### Carpeta templates/:

- base.html - plantilla base
- predictor/prediction_form.html - formulario web (limpiado)

### Carpeta static/:

- css/ - estilos personalizados
- js/ - scripts javascript

### Carpeta data/:

- data_cleaned.csv - datos limpios
- data_process.csv - datos procesados
- data.xlsx - datos originales

### Carpeta train/:

- Notebook_XGBoost.ipynb - documentación del proceso de entrenamiento

### Carpeta venv/:

- entorno virtual python

### Archivos git:

- .git/ - repositorio git
- .gitignore - archivos ignorados
- .gitattributes - configuración git
- README.md - documentación

TODOS LOS COMENTARIOS INNECESARIOS HAN SIDO ELIMINADOS
SOLO PERMANECEN COMENTARIOS IMPORTANTES Y CONCISOS EN MINÚSCULA
