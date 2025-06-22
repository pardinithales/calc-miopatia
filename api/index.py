from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def get_html_template():
    """Retorna o HTML da aplicação"""
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Miopatia</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        header p {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 400;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .form-grid {
            display: grid;
            gap: 30px;
        }
        
        .form-section {
            background: #f8fafc;
            border-radius: 12px;
            padding: 25px;
            border-left: 4px solid #667eea;
        }
        
        .form-section h3 {
            color: #2d3748;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .form-section h3 i {
            color: #667eea;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .form-row:last-child {
            margin-bottom: 0;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        label {
            font-weight: 500;
            margin-bottom: 8px;
            color: #4a5568;
            font-size: 0.95rem;
        }
        
        input, select {
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            background: white;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }
        
        input:focus, select:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        small {
            color: #718096;
            font-size: 0.85rem;
            margin-top: 4px;
        }
        
        .button-container {
            text-align: center;
            margin-top: 40px;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }
        
        .result-card, .error-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .result-icon {
            font-size: 4rem;
            color: #48bb78;
            margin-bottom: 20px;
        }
        
        .prediction-type {
            font-size: 2rem;
            font-weight: 700;
            padding: 15px 30px;
            border-radius: 50px;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .prediction-type.structural {
            background: linear-gradient(135deg, #4299e1, #3182ce);
            color: white;
        }
        
        .prediction-type.metabolic {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
        }
        
        .loading {
            text-align: center;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            margin: 0 auto 20px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .card { padding: 25px; }
            .form-row { grid-template-columns: 1fr; }
            header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-heartbeat"></i> Calculadora de Miopatia</h1>
            <p>Sistema de predição automática para diagnóstico de tipos de miopatia</p>
        </header>

        <div class="card">
            <form id="myopathyForm">
                <div class="form-grid">
                    <!-- Valores de CPK -->
                    <div class="form-section">
                        <h3><i class="fas fa-chart-line"></i> Valores de CPK</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="maior_cpk">Maior CPK</label>
                                <input type="number" id="maior_cpk" name="maior_cpk" step="0.01" required>
                                <small>Valor máximo de CPK registrado</small>
                            </div>
                            <div class="form-group">
                                <label for="menor_cpk">Menor CPK</label>
                                <input type="number" id="menor_cpk" name="menor_cpk" step="0.01" required>
                                <small>Valor mínimo de CPK registrado</small>
                            </div>
                        </div>
                    </div>

                    <!-- Valores de Lactato -->
                    <div class="form-section">
                        <h3><i class="fas fa-flask"></i> Valores de Lactato</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="maior_lactato">Maior Lactato</label>
                                <input type="number" id="maior_lactato" name="maior_lactato" step="0.01" required>
                                <small>Valor máximo de lactato registrado</small>
                            </div>
                            <div class="form-group">
                                <label for="menor_lactato">Menor Lactato</label>
                                <input type="number" id="menor_lactato" name="menor_lactato" step="0.01" required>
                                <small>Valor mínimo de lactato registrado</small>
                            </div>
                        </div>
                    </div>

                    <!-- Sintomas Gerais -->
                    <div class="form-section">
                        <h3><i class="fas fa-stethoscope"></i> Sintomas Gerais</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="dor_presente">Dor Presente</label>
                                <select id="dor_presente" name="dor_presente" required>
                                    <option value="">Selecione</option>
                                    <option value="1">Sim</option>
                                    <option value="2">Não</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="fadiga_status">Status de Fadiga</label>
                                <select id="fadiga_status" name="fadiga_status" required>
                                    <option value="">Selecione</option>
                                    <option value="1">Presente</option>
                                    <option value="2">Ausente</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="caibra_status">Status de Cãibra</label>
                                <select id="caibra_status" name="caibra_status" required>
                                    <option value="">Selecione</option>
                                    <option value="1">Presente</option>
                                    <option value="2">Ausente</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Características da Mialgia -->
                    <div class="form-section">
                        <h3><i class="fas fa-exclamation-triangle"></i> Características da Mialgia</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="mialgia_status">Status da Mialgia</label>
                                <select id="mialgia_status" name="mialgia_status" required>
                                    <option value="">Selecione</option>
                                    <option value="1">Presente</option>
                                    <option value="2">Ausente</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="mialgia_inicial_tipo">Tipo Inicial da Mialgia</label>
                                <select id="mialgia_inicial_tipo" name="mialgia_inicial_tipo" required>
                                    <option value="">Selecione</option>
                                    <option value="3">Tipo 3 - Mialgia Leve/Localizada</option>
                                    <option value="4">Tipo 4 - Mialgia Moderada/Generalizada</option>
                                    <option value="5">Tipo 5 - Mialgia Intensa/Severa</option>
                                </select>
                                <small>Classificação inicial da intensidade da dor muscular</small>
                            </div>
                            <div class="form-group">
                                <label for="mialgia_atual_tipo">Tipo Atual da Mialgia</label>
                                <select id="mialgia_atual_tipo" name="mialgia_atual_tipo" required>
                                    <option value="">Selecione</option>
                                    <option value="3">Tipo 3 - Mialgia Leve/Localizada</option>
                                    <option value="4">Tipo 4 - Mialgia Moderada/Generalizada</option>
                                    <option value="5">Tipo 5 - Mialgia Intensa/Severa</option>
                                </select>
                                <small>Classificação atual da intensidade da dor muscular</small>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="button-container">
                    <button type="submit" id="predictBtn">
                        <i class="fas fa-calculator"></i>
                        Calcular Diagnóstico
                    </button>
                </div>
            </form>
        </div>

        <!-- Resultado -->
        <div id="result" class="result-card" style="display: none;">
            <div class="result-content">
                <div class="result-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h3>Resultado da Predição</h3>
                <div class="prediction-result">
                    <span class="prediction-type" id="predictionType"></span>
                </div>
                <div class="confidence-info">
                    <span>Confiança: </span>
                    <span class="confidence-value" id="confidenceValue"></span>
                </div>
            </div>
        </div>

        <!-- Loading -->
        <div id="loading" class="loading" style="display: none;">
            <div class="spinner"></div>
            <p>Processando dados...</p>
        </div>

        <!-- Error -->
        <div id="error" class="error-card" style="display: none;">
            <div class="error-content">
                <i class="fas fa-exclamation-circle"></i>
                <h3>Erro no Processamento</h3>
                <p id="errorMessage"></p>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('myopathyForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('predictionType').textContent = data.prediction;
                    document.getElementById('confidenceValue').textContent = data.confidence + '%';
                    
                    const predictionElement = document.getElementById('predictionType');
                    predictionElement.className = 'prediction-type ' + 
                        (data.prediction === 'Estrutural' ? 'structural' : 'metabolic');
                    
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
                } else {
                    document.getElementById('errorMessage').textContent = data.error;
                    document.getElementById('error').style.display = 'block';
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('errorMessage').textContent = 'Erro de conexão. Tente novamente.';
                document.getElementById('error').style.display = 'block';
            }
        });
    </script>
</body>
</html>'''

def predict_myopathy_type(data):
    """
    Faz a predição do tipo de miopatia usando regras baseadas nos dados originais
    Análise baseada nos padrões encontrados no dataset
    """
    
    # Extrair valores
    maior_cpk = data['Maior_Cpk']
    menor_cpk = data['Menor_Cpk']
    maior_lactato = data['Maior_Lactato']
    menor_lactato = data['Menor_Lactato']
    dor_presente = data['Dor_Presente']
    mialgia_status = data['Mialgia_Status']
    mialgia_inicial = data['Mialgia_Inicial_Tipo']
    mialgia_atual = data['Mialgia_Atual_Tipo']
    fadiga_status = data['Fadiga_Status']
    caibra_status = data['Caibra_Status']
    
    # Calcular diferença de CPK
    delta_cpk = maior_cpk - menor_cpk
    
    # Inicializar score (0 = mais metabólico, 100 = mais estrutural)
    score = 50
    confidence = 60  # Base confidence
    
    # Regras baseadas nos padrões do dataset
    
    # 1. Análise dos valores de CPK
    if maior_cpk > 2000:
        score += 25  # CPK muito alto sugere estrutural
        confidence += 15
    elif maior_cpk > 1000:
        score += 15
        confidence += 10
    elif maior_cpk < 200:
        score -= 20  # CPK baixo sugere metabólico
        confidence += 10
    
    # 2. Análise da variação de CPK
    if delta_cpk > 1000:
        score += 20  # Grande variação sugere estrutural
        confidence += 10
    elif delta_cpk < 50:
        score -= 15  # Pouca variação sugere metabólico
        confidence += 5
    
    # 3. Análise dos valores de Lactato
    if maior_lactato > 4.0:
        score -= 25  # Lactato alto sugere metabólico
        confidence += 15
    elif maior_lactato > 3.0:
        score -= 10
        confidence += 5
    elif maior_lactato < 2.0:
        score += 10  # Lactato baixo sugere estrutural
        confidence += 5
    
    # 4. Análise dos sintomas
    if dor_presente == 1:  # Tem dor
        if mialgia_status == 1:  # Tem mialgia
            if mialgia_atual == 5:  # Mialgia intensa
                score += 15
                confidence += 10
            elif mialgia_atual == 3:  # Mialgia leve
                score -= 10
                confidence += 5
    
    # 5. Análise da fadiga
    if fadiga_status == 1:  # Tem fadiga
        score -= 10  # Fadiga mais comum em metabólico
        confidence += 5
    
    # 6. Análise das cãibras
    if caibra_status == 1:  # Tem cãibras
        score -= 15  # Cãibras mais comuns em metabólico
        confidence += 10
    
    # 7. Padrões combinados
    if maior_cpk > 1500 and maior_lactato < 3.0:
        score += 20  # Padrão típico estrutural
        confidence += 15
    
    if maior_lactato > 4.0 and fadiga_status == 1 and caibra_status == 1:
        score -= 25  # Padrão típico metabólico
        confidence += 20
    
    # Determinar resultado final
    if score >= 50:
        myopathy_type = 'Estrutural'
        final_confidence = min(95, 50 + (score - 50) * 0.8 + (confidence - 60) * 0.6)
    else:
        myopathy_type = 'Metabólico'
        final_confidence = min(95, 50 + (50 - score) * 0.8 + (confidence - 60) * 0.6)
    
    # Garantir confiança mínima
    final_confidence = max(60, final_confidence)
    
    return myopathy_type, final_confidence

@app.route('/')
def index():
    return get_html_template()

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
        
        # Validar dados básicos
        if data['Maior_Cpk'] < data['Menor_Cpk']:
            raise ValueError("Maior CPK não pode ser menor que Menor CPK")
        
        if data['Maior_Lactato'] < data['Menor_Lactato']:
            raise ValueError("Maior Lactato não pode ser menor que Menor Lactato")
        
        # Fazer predição
        myopathy_type, confidence = predict_myopathy_type(data)
        
        return jsonify({
            'success': True,
            'prediction': myopathy_type,
            'confidence': round(confidence, 1)
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f"Erro de validação: {str(e)}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Erro no processamento: {str(e)}"
        })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Calculadora de Miopatia funcionando'})

# Para Vercel
if __name__ == '__main__':
    app.run(debug=True)
else:
    # Para Vercel serverless
    app.wsgi_app = app 