from django.shortcuts import render
from django.contrib import messages

import numpy as np
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictRequestSerializer
from .model_loader import get_model, get_label_encoder
from .features import FEATURES
from .forms import PredictionForm


def prediction_form_view(request):
    prediction_result = None
    form = PredictionForm()
    
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            try:
                form_data = form.cleaned_data
                
                manual_fields = ['servicioalta', 'dx_principal_egreso', 'proc1', 'dxr_1', 'dxr_2', 'dxr_3', 'dxr_4']
                for field in manual_fields:
                    manual_value = request.POST.get(f'{field}_manual')
                    if manual_value and manual_value.strip():
                        form_data[field] = manual_value.strip()
                    elif form_data.get(field) == 'OTRO':
                        if field == 'dx_principal_egreso':
                            form_data[field] = 'MISSING'
                        elif field == 'servicioalta':
                            form_data[field] = '20'
                        else:
                            form_data[field] = 'MISSING'
                
                sexo_encoded = 0 if form_data['sexo'] == 'F' else 1
                tipo_ingreso_encoded = 0 if form_data['tipo_ingreso'] == 'URGENCIA' else 1
                cuidados_intensivos_encoded = 0 if form_data['cuidados_intensivos'] == 'NO' else 1
                situacion_al_alta_encoded = 0 if form_data['situacion_al_alta'] == 'FALLECIDO' else 1
                infecciones_encoded = 0 if form_data['infecciones'] == 'NO' else 1
                infeccion_quirurgica_encoded = 0 if form_data['infeccion_quirurgica'] == 'NO' else 1
                
                tipo_servicio_NO_APLICA = 1 if form_data['tipo_servicio'] == 'NO APLICA' else 0
                tipo_servicio_URGENCIA_ADULTOS = 1 if form_data['tipo_servicio'] == 'URGENCIA ADULTOS' else 0
                tipo_servicio_URGENCIA_PEDIATRICAS = 1 if form_data['tipo_servicio'] == 'URGENCIA PEDIATRICAS' else 0
                
                servicioalta_code = f"X{form_data['servicioalta']}"
                dx_de_ingreso_code = f"X{form_data['dx_de_ingreso']}"
                
                proc1_value = form_data['proc1'] if form_data['proc1'] else 'MISSING'
                if proc1_value == 'MISSING' or proc1_value == '':
                    proc1_code = 'XMISSING'
                else:
                    proc1_code = f"X{proc1_value}"
                
                # crear dataframe con orden exacto de features
                data_dict = {
                    'edad': form_data['edad'],
                    'sexo': sexo_encoded,
                    'tipo_ingreso': tipo_ingreso_encoded,
                    'días_estancia': form_data['días_estancia'],
                    'servicioalta': servicioalta_code,
                    'cuidados_intensivos': cuidados_intensivos_encoded,
                    'dias_uci': form_data['dias_uci'],
                    'dx_de_ingreso': dx_de_ingreso_code,
                    'dx_principal_egreso': form_data['dx_principal_egreso'],
                    'dxr_1': form_data['dxr_1'],
                    'dxr_2': form_data['dxr_2'],
                    'dxr_3': form_data['dxr_3'],
                    'dxr_4': form_data['dxr_4'],
                    'situacion_al_alta': situacion_al_alta_encoded,
                    'proc1': proc1_code,
                    'infecciones': infecciones_encoded,
                    'infeccion_quirurgica': infeccion_quirurgica_encoded,
                    'tipo_servicio_NO APLICA': tipo_servicio_NO_APLICA,
                    'tipo_servicio_URGENCIA ADULTOS': tipo_servicio_URGENCIA_ADULTOS,
                    'tipo_servicio_URGENCIA PEDIATRICAS': tipo_servicio_URGENCIA_PEDIATRICAS
                }
                
                data = []
                for feature in FEATURES:
                    data.append(data_dict[feature])
                
                df = pd.DataFrame([data], columns=FEATURES)
                
                categorical_columns = ['servicioalta', 'dx_de_ingreso', 'dx_principal_egreso', 
                                     'dxr_1', 'dxr_2', 'dxr_3', 'dxr_4', 'proc1']
                for col in categorical_columns:
                    if col in df.columns:
                        df[col] = df[col].astype('category')
                
                model = get_model()
                encoder = get_label_encoder()
                
                y_pred_encoded = model.predict(df)
                y_pred_original = encoder.inverse_transform(y_pred_encoded)
                
                try:
                    y_proba = model.predict_proba(df)
                    confidence = float(np.max(y_proba)) * 100
                except Exception:
                    confidence = None
                
                prediction_code = y_pred_original[0]
                
                # remover la x del resultado para mostrar al usuario
                if prediction_code.startswith('X'):
                    display_code = prediction_code[1:]
                else:
                    display_code = prediction_code
                
                prediction_result = {
                    'prediction': display_code,
                    'confidence': confidence
                }
                
                messages.success(request, 'Predicción realizada exitosamente!')
                
            except Exception as e:
                messages.error(request, f'Error al realizar la predicción: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'predictor/prediction_form.html', {
        'form': form,
        'prediction_result': prediction_result
    })

class PredictView(APIView):
    def post(self, request):
        serializer = PredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        try:
            processed_data = {}
            
            processed_data['edad'] = data['edad']
            processed_data['sexo'] = data['sexo']
            processed_data['tipo_ingreso'] = data['tipo_ingreso']
            processed_data['días_estancia'] = data['días_estancia']
            processed_data['cuidados_intensivos'] = data['cuidados_intensivos']
            processed_data['dias_uci'] = data['dias_uci']
            processed_data['situacion_al_alta'] = data['situacion_al_alta']
            processed_data['infecciones'] = data['infecciones']
            processed_data['infeccion_quirurgica'] = data['infeccion_quirurgica']
            
            processed_data['tipo_servicio_NO APLICA'] = data['tipo_servicio_NO_APLICA']
            processed_data['tipo_servicio_URGENCIA ADULTOS'] = data['tipo_servicio_URGENCIA_ADULTOS']
            processed_data['tipo_servicio_URGENCIA PEDIATRICAS'] = data['tipo_servicio_URGENCIA_PEDIATRICAS']
            
            servicioalta_value = str(data['servicioalta'])
            processed_data['servicioalta'] = f"X{servicioalta_value}"
            
            dx_de_ingreso_value = str(data['dx_de_ingreso'])
            processed_data['dx_de_ingreso'] = f"X{dx_de_ingreso_value}"
            
            processed_data['dx_principal_egreso'] = str(data['dx_principal_egreso'])
            
            # procesar dxr fields
            for dxr_field in ['dxr_1', 'dxr_2', 'dxr_3', 'dxr_4']:
                dxr_value = str(data[dxr_field])
                if dxr_value == '0' or dxr_value == '' or dxr_value.lower() == 'missing':
                    processed_data[dxr_field] = 'MIS'  # usar MIS en lugar de MISSING
                else:
                    processed_data[dxr_field] = dxr_value
            
            proc1_value = str(data['proc1'])
            if proc1_value == '0' or proc1_value == '' or proc1_value.lower() == 'missing':
                processed_data['proc1'] = 'XMISSING'
            else:
                processed_data['proc1'] = f"X{proc1_value}"
            
            data_list = []
            for feature in FEATURES:
                data_list.append(processed_data[feature])
            
            df = pd.DataFrame([data_list], columns=FEATURES)
            
            categorical_columns = ['servicioalta', 'dx_de_ingreso', 'dx_principal_egreso', 
                                 'dxr_1', 'dxr_2', 'dxr_3', 'dxr_4', 'proc1']
            for col in categorical_columns:
                if col in df.columns:
                    df[col] = df[col].astype('category')

            model = get_model()
            encoder = get_label_encoder()

            y_pred_encoded = model.predict(df)
            y_pred_original = encoder.inverse_transform(y_pred_encoded)
            
            try:
                y_proba = model.predict_proba(df)
                confidence = float(np.max(y_proba)) * 100
                proba_list = y_proba[0].tolist()
            except Exception:
                confidence = None
                proba_list = None

            prediction_code = y_pred_original[0]
            
            # remover la x del resultado para mostrar al usuario
            if prediction_code.startswith('X'):
                display_code = prediction_code[1:]
            else:
                display_code = prediction_code

            response = {
                "prediction": display_code,
                "prediction_full_code": prediction_code,
                "prediction_encoded": int(y_pred_encoded[0]) if len(y_pred_encoded) else None,
                "confidence": confidence,
                "probabilities": proba_list,
                "processed_input": processed_data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al predecir: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
