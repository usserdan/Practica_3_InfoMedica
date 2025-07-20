from django import forms
import json
import os
from .features import FEATURES

def load_codigo_choices():
    json_path = os.path.join(os.path.dirname(__file__), 'codigo_choices_final.json')
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

class FlexibleChoiceField(forms.ChoiceField):
    def validate(self, value):
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['required'], code='required')

class PredictionForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        codigo_data = load_codigo_choices()
        
        if 'servicioalta' in codigo_data:
            servicioalta_choices = [('', 'Seleccione...'), ('OTRO', 'Otro código (escribir manualmente)')] + [(str(code), str(code)) for code in codigo_data['servicioalta']]
            self.fields['servicioalta'].choices = servicioalta_choices
        
        if 'dx_de_ingreso' in codigo_data:
            dx_ingreso_choices = [('', 'Seleccione...')] + [(str(code), str(code)) for code in codigo_data['dx_de_ingreso']]
            self.fields['dx_de_ingreso'].choices = dx_ingreso_choices
        
        if 'dx_principal_egreso' in codigo_data:
            dx_principal_choices = [('', 'Seleccione...'), ('OTRO', 'Otro código (escribir manualmente)')] + [(code, code) for code in codigo_data['dx_principal_egreso'][:50]]
            self.fields['dx_principal_egreso'].choices = dx_principal_choices
        
        if 'proc1' in codigo_data:
            proc_choices = [('', 'Sin procedimiento'), ('MISSING', 'Sin procedimiento'), ('OTRO', 'Otro código (escribir manualmente)')] + [(code, code) for code in codigo_data['proc1'][:50]]
            self.fields['proc1'].choices = proc_choices
        
        for i in range(1, 5):
            field_name = f'dxr_{i}'
            if field_name in codigo_data:
                dxr_choices = [('', 'Sin diagnóstico'), ('MISSING', 'Sin diagnóstico'), ('OTRO', 'Otro código (escribir manualmente)')] + [(code, code) for code in codigo_data[field_name][:50]]
                self.fields[field_name].choices = dxr_choices
        
        self.all_codigo_data = codigo_data
    
    # campos del paciente
    edad = forms.IntegerField(
        label="Edad del paciente",
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 65'
        })
    )
    
    sexo = forms.ChoiceField(
        label="Sexo",
        choices=[
            ('F', "Femenino"),
            ('M', "Masculino")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_ingreso = forms.ChoiceField(
        label="Tipo de ingreso",
        choices=[
            ('URGENCIA', "Urgencia"),
            ('PROGRAMADO', "Programado")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    días_estancia = forms.IntegerField(
        label="Días de estancia",
        min_value=0,
        max_value=365,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 5'
        })
    )
    
    servicioalta = FlexibleChoiceField(
        label="Servicio de alta",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    cuidados_intensivos = forms.ChoiceField(
        label="¿Requirió cuidados intensivos?",
        choices=[
            ('NO', "No"),
            ('SI', "Sí")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    dias_uci = forms.IntegerField(
        label="Días en UCI",
        min_value=0,
        max_value=365,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 0'
        })
    )
    
    dx_de_ingreso = forms.ChoiceField(
        label="Diagnóstico de ingreso",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    dx_principal_egreso = FlexibleChoiceField(
        label="Diagnóstico principal de egreso",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    dxr_1 = FlexibleChoiceField(
        label="Diagnóstico relacionado 1",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    dxr_2 = FlexibleChoiceField(
        label="Diagnóstico relacionado 2",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    dxr_3 = FlexibleChoiceField(
        label="Diagnóstico relacionado 3",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    dxr_4 = FlexibleChoiceField(
        label="Diagnóstico relacionado 4",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    situacion_al_alta = forms.ChoiceField(
        label="Situación al alta",
        choices=[
            ('ALTA MÉDICA', "Alta médica"),
            ('FALLECIDO', "Fallecido")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    proc1 = FlexibleChoiceField(
        label="Procedimiento principal (código)",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    infecciones = forms.ChoiceField(
        label="¿Presentó infecciones?",
        choices=[
            ('NO', "No"),
            ('SI', "Sí")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    infeccion_quirurgica = forms.ChoiceField(
        label="¿Infección quirúrgica?",
        choices=[
            ('NO', "No"),
            ('SI', "Sí")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_servicio = forms.ChoiceField(
        label="Servicio que dio el alta",
        choices=[
            ('CIRUGIA', "Cirugía"),
            ('NO APLICA', "No aplica"),
            ('URGENCIA ADULTOS', "Urgencia adultos"),
            ('URGENCIA PEDIATRICAS', "Urgencia pediátricas")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # validar códigos manuales
        if hasattr(self, 'all_codigo_data'):
            manual_fields = {
                'servicioalta': 'servicioalta',
                'dx_principal_egreso': 'dx_principal_egreso', 
                'proc1': 'proc1',
                'dxr_1': 'dxr_1',
                'dxr_2': 'dxr_2', 
                'dxr_3': 'dxr_3',
                'dxr_4': 'dxr_4'
            }
            
            for field_name, data_key in manual_fields.items():
                value = cleaned_data.get(field_name)
                if value and value not in ['', 'MISSING', 'OTRO']:
                    if data_key in self.all_codigo_data:
                        valid_codes = [str(code) for code in self.all_codigo_data[data_key]]
                        if str(value) not in valid_codes:
                            self.add_error(field_name, f'El código "{value}" no está presente en los datos de entrenamiento. Use un código válido o seleccione de la lista.')
        
        # convertir campos vacíos a valores por defecto
        optional_char_fields = ['dxr_1', 'dxr_2', 'dxr_3', 'dxr_4', 'proc1']
        for field in optional_char_fields:
            if not cleaned_data.get(field) or cleaned_data.get(field) == '':
                cleaned_data[field] = 'MISSING'
        
        if not cleaned_data.get('dx_principal_egreso') or cleaned_data.get('dx_principal_egreso') == '':
            cleaned_data['dx_principal_egreso'] = 'MISSING'
        
        # validar días uci vs estancia
        dias_estancia = cleaned_data.get('días_estancia', 0)
        dias_uci = cleaned_data.get('dias_uci', 0)
        
        if dias_uci > dias_estancia:
            raise forms.ValidationError(
                "Los días en UCI no pueden superar los días de estancia total."
            )
        
        return cleaned_data
