from django.shortcuts import render

import numpy as np
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictRequestSerializer
from .model_loader import get_model
from .features import FEATURES

class PredictView(APIView):
    """
    Recibe JSON con las features y devuelve la predicción del modelo.
    """

    def post(self, request):
        serializer = PredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Datos validados
        data = serializer.validated_data

        try:
            # Convertir los datos a un DataFrame ordenado según FEATURES
            df = pd.DataFrame([[data[feature] for feature in FEATURES]], columns=FEATURES)

            model = get_model()

            # Realizar predicción
            y_pred = model.predict(df)
            try:
                y_proba = model.predict_proba(df).tolist()
            except Exception:
                y_proba = None

            response = {
                "prediction": int(y_pred[0]) if len(y_pred) else None,
                "proba": y_proba[0] if y_proba else None,
                "input": data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al predecir: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
