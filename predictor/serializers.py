from rest_framework import serializers
from .features import FEATURES

def build_fields():
    fields = {}
    for feature in FEATURES:
        fields[feature] = serializers.FloatField(required=True)
    return fields

# Crear dinámicamente el serializer con todos los campos
PredictRequestSerializer = type(
    "PredictRequestSerializer",
    (serializers.Serializer,),
    build_fields()
)

