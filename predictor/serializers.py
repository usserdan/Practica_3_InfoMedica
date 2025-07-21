from rest_framework import serializers
from .features import FEATURES

class PredictRequestSerializer(serializers.Serializer):
    edad = serializers.IntegerField(required=True)
    sexo = serializers.IntegerField(required=True)
    tipo_ingreso = serializers.IntegerField(required=True)
    días_estancia = serializers.IntegerField(required=True)
    servicioalta = serializers.CharField(required=True)
    cuidados_intensivos = serializers.IntegerField(required=True)
    dias_uci = serializers.IntegerField(required=True)
    dx_de_ingreso = serializers.CharField(required=True)
    dx_principal_egreso = serializers.CharField(required=True)
    dxr_1 = serializers.CharField(required=True)
    dxr_2 = serializers.CharField(required=True)
    dxr_3 = serializers.CharField(required=True)
    dxr_4 = serializers.CharField(required=True)
    situacion_al_alta = serializers.IntegerField(required=True)
    proc1 = serializers.CharField(required=True)
    infecciones = serializers.IntegerField(required=True)
    infeccion_quirurgica = serializers.IntegerField(required=True)
    
    # campos one-hot encoding
    tipo_servicio_NO_APLICA = serializers.IntegerField(required=True, min_value=0, max_value=1)
    tipo_servicio_URGENCIA_ADULTOS = serializers.IntegerField(required=True, min_value=0, max_value=1)
    tipo_servicio_URGENCIA_PEDIATRICAS = serializers.IntegerField(required=True, min_value=0, max_value=1)
    
    def validate(self, data):
        # validar que solo uno de los tipo_servicio sea 1
        tipo_servicio_sum = (
            data['tipo_servicio_NO_APLICA'] + 
            data['tipo_servicio_URGENCIA_ADULTOS'] + 
            data['tipo_servicio_URGENCIA_PEDIATRICAS']
        )
        if tipo_servicio_sum != 1:
            raise serializers.ValidationError(
                "Exactamente uno de los campos tipo_servicio debe ser 1 y los otros 0"
            )
        
        return data
    
    def to_internal_value(self, data):
        # mapea campos con espacios a nombres sin espacios
        mapped_data = data.copy()
        
        field_mapping = {
            'tipo_servicio_NO APLICA': 'tipo_servicio_NO_APLICA',
            'tipo_servicio_URGENCIA ADULTOS': 'tipo_servicio_URGENCIA_ADULTOS', 
            'tipo_servicio_URGENCIA PEDIATRICAS': 'tipo_servicio_URGENCIA_PEDIATRICAS'
        }
        
        for old_key, new_key in field_mapping.items():
            if old_key in mapped_data:
                mapped_data[new_key] = mapped_data.pop(old_key)
        
        return super().to_internal_value(mapped_data)

