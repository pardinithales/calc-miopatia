from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Variáveis globais para o modelo
model_data = None

def load_model():
    """Carrega o modelo pré-treinado"""
    global model_data
    
    try:
        # Caminho para o arquivo do modelo
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.pkl')
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        print("Modelo carregado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return False

def predict_myopathy_type(data):
    """Faz a predição do tipo de miopatia"""
    global model_data
    
    if model_data is None:
        if not load_model():
            raise Exception("Não foi possível carregar o modelo")
    
    # Ordenar os dados na ordem correta
    feature_order = [
        'Maior_Cpk', 'Menor_Cpk', 'Maior_Lactato', 'Menor_Lactato',
        'Dor_Presente', 'Mialgia_Status', 'Mialgia_Inicial_Tipo', 'Mialgia_Atual_Tipo',
        'Fadiga_Status', 'Caibra_Status'
    ]
    
    # Criar array com os dados na ordem correta
    patient_data = np.array([[data[feature] for feature in feature_order]])
    
    # Padronizar os dados
    patient_data_scaled = model_data['scaler'].transform(patient_data)
    
    # Fazer predição
    prediction = model_data['model'].predict(patient_data_scaled)
    probability = model_data['model'].predict_proba(patient_data_scaled)
    
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

# Tentar carregar o modelo na inicialização
load_model()

# Para Vercel
if __name__ == '__main__':
    app.run(debug=True)
else:
    # Para Vercel serverless
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) 