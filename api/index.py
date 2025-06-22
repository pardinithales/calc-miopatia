from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
import os
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Variáveis globais para o modelo e scaler
rf_model = None
scaler = None

def load_and_train_model():
    """Carrega os dados e treina o modelo"""
    global rf_model, scaler
    
    try:
        # Caminho para o arquivo CSV (ajustado para Vercel)
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'df.csv')
        
        # Carregando o dataset  
        df = pd.read_csv(csv_path)
        
        # Substituindo valores inválidos por NaN e convertendo para numérico
        df.replace('#VALUE!', np.nan, inplace=True)
        df = df.apply(pd.to_numeric, errors='coerce')
        
        # Remover linhas onde Diagnostico_Tipo é igual a 3 (distrofia miotônica)
        df = df[df['Diagnostico_Tipo'] != 3]
        
        # Removendo colunas Delta e PacienteID
        df.drop(columns=[col for col in df.columns if 'Delta' in col or col == 'PacienteID'], inplace=True)
        
        # Preenchendo valores ausentes com a mediana
        df.fillna(df.median(), inplace=True)
        
        # Selecionando as colunas de interesse
        columns_of_interest = [
            'Maior_Cpk', 'Menor_Cpk', 'Maior_Lactato', 'Menor_Lactato',
            'Dor_Presente', 'Mialgia_Status', 'Mialgia_Inicial_Tipo', 'Mialgia_Atual_Tipo',
            'Fadiga_Status', 'Caibra_Status'
        ]
        df = df[columns_of_interest + ['Diagnostico_Tipo']]
        
        # Definindo características (X) e alvo (y)
        X = df.drop('Diagnostico_Tipo', axis=1)
        y = df['Diagnostico_Tipo']
        
        # Dividindo em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Padronizando as características
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        # Treinando o modelo
        rf_model = RandomForestClassifier(
            random_state=42,
            class_weight='balanced',
            n_estimators=100
        )
        rf_model.fit(X_train_scaled, y_train)
        
        return True
        
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return False

def predict_myopathy_type(data):
    """Faz a predição do tipo de miopatia"""
    global rf_model, scaler
    
    if rf_model is None or scaler is None:
        if not load_and_train_model():
            raise Exception("Não foi possível carregar o modelo")
    
    # Criar DataFrame com os dados do paciente
    patient_data = pd.DataFrame([data])
    
    # Padronizar os dados
    patient_data_scaled = scaler.transform(patient_data)
    
    # Fazer predição
    prediction = rf_model.predict(patient_data_scaled)
    probability = rf_model.predict_proba(patient_data_scaled)
    
    # Mapear resultado
    myopathy_type = 'Estrutural' if prediction[0] == 1 else 'Metabólico'
    confidence = max(probability[0]) * 100
    
    return myopathy_type, confidence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receber dados do formulário
        data = {
            'Maior_Cpk': float(request.form['maior_cpk']),
            'Menor_Cpk': float(request.form['menor_cpk']),
            'Maior_Lactato': float(request.form['maior_lactato']),
            'Menor_Lactato': float(request.form['menor_lactato']),
            'Dor_Presente': int(request.form['dor_presente']),
            'Mialgia_Status': int(request.form['mialgia_status']),
            'Mialgia_Inicial_Tipo': int(request.form['mialgia_inicial_tipo']),
            'Mialgia_Atual_Tipo': int(request.form['mialgia_atual_tipo']),
            'Fadiga_Status': int(request.form['fadiga_status']),
            'Caibra_Status': int(request.form['caibra_status'])
        }
        
        # Fazer predição
        myopathy_type, confidence = predict_myopathy_type(data)
        
        return jsonify({
            'success': True,
            'prediction': myopathy_type,
            'confidence': round(confidence, 1)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Inicializar o modelo na primeira chamada
load_and_train_model()

# Para Vercel
if __name__ == '__main__':
    app.run(debug=True)
else:
    # Para Vercel serverless
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) 