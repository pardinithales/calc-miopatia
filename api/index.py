from flask import Flask, request, jsonify
import os
import traceback

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
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error-icon {
            font-size: 4rem;
            color: #e53e3e;
            margin-bottom: 20px;
        }
        
        .confidence-bar {
            background: #e2e8f0;
            border-radius: 10px;
            height: 20px;
            margin: 20px 0;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(135deg, #48bb78, #38a169);
            border-radius: 10px;
            transition: width 0.5s ease;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 25px;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .prediction-type {
                font-size: 1.5rem;
                padding: 12px 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-heartbeat"></i> Calculadora de Miopatia</h1>
            <p>Sistema de Predição: Estrutural vs Metabólico</p>
        </header>
        
        <div class="card">
            <form id="myopathyForm">
                <div class="form-grid">
                    <!-- Seção 1: Valores de CPK -->
                    <div class="form-section">
                        <h3><i class="fas fa-chart-line"></i>Níveis de CPK (U/L)</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="maior_cpk">Maior CPK:</label>
                                <input type="number" id="maior_cpk" name="maior_cpk" min="0" step="0.1" required>
                                <small>Maior valor de CPK registrado</small>
                            </div>
                            <div class="form-group">
                                <label for="menor_cpk">Menor CPK:</label>
                                <input type="number" id="menor_cpk" name="menor_cpk" min="0" step="0.1" required>
                                <small>Menor valor de CPK registrado</small>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Seção 2: Valores de Lactato -->
                    <div class="form-section">
                        <h3><i class="fas fa-vial"></i>Níveis de Lactato (mmol/L)</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="maior_lactato">Maior Lactato:</label>
                                <input type="number" id="maior_lactato" name="maior_lactato" min="0" step="0.1" required>
                                <small>Maior valor de lactato registrado</small>
                            </div>
                            <div class="form-group">
                                <label for="menor_lactato">Menor Lactato:</label>
                                <input type="number" id="menor_lactato" name="menor_lactato" min="0" step="0.1" required>
                                <small>Menor valor de lactato registrado</small>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Seção 3: Sintomas Principais -->
                    <div class="form-section">
                        <h3><i class="fas fa-stethoscope"></i>Sintomas Clínicos</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="dor_presente">Presença de Dor:</label>
                                <select id="dor_presente" name="dor_presente" required>
                                    <option value="">Selecione...</option>
                                    <option value="0">Não</option>
                                    <option value="1">Sim</option>
                                </select>
                                <small>Paciente relata dor muscular</small>
                            </div>
                            <div class="form-group">
                                <label for="mialgia_status">Status da Mialgia:</label>
                                <select id="mialgia_status" name="mialgia_status" required>
                                    <option value="">Selecione...</option>
                                    <option value="0">Ausente</option>
                                    <option value="1">Presente</option>
                                </select>
                                <small>Presença de mialgia (dor muscular)</small>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Seção 4: Tipos de Mialgia -->
                    <div class="form-section">
                        <h3><i class="fas fa-exclamation-triangle"></i>Classificação da Mialgia</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="mialgia_inicial_tipo">Tipo Inicial da Mialgia:</label>
                                <select id="mialgia_inicial_tipo" name="mialgia_inicial_tipo" required>
                                    <option value="">Selecione...</option>
                                    <option value="0">Não se Aplica</option>
                                    <option value="3">Tipo 3 - Leve/Localizada</option>
                                    <option value="4">Tipo 4 - Moderada/Generalizada</option>
                                    <option value="5">Tipo 5 - Intensa/Severa</option>
                                </select>
                                <small>Intensidade inicial da mialgia</small>
                            </div>
                            <div class="form-group">
                                <label for="mialgia_atual_tipo">Tipo Atual da Mialgia:</label>
                                <select id="mialgia_atual_tipo" name="mialgia_atual_tipo" required>
                                    <option value="">Selecione...</option>
                                    <option value="0">Não se Aplica</option>
                                    <option value="3">Tipo 3 - Leve/Localizada</option>
                                    <option value="4">Tipo 4 - Moderada/Generalizada</option>
                                    <option value="5">Tipo 5 - Intensa/Severa</option>
                                </select>
                                <small>Intensidade atual da mialgia</small>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Seção 5: Outros Sintomas -->
                    <div class="form-section">
                        <h3><i class="fas fa-user-md"></i>Sintomas Associados</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="fadiga_status">Presença de Fadiga:</label>
                                <select id="fadiga_status" name="fadiga_status" required>
                                    <option value="">Selecione...</option>
                                    <option value="0">Ausente</option>
                                    <option value="1">Presente</option>
                                </select>
                                <small>Fadiga muscular relatada pelo paciente</small>
                            </div>
                            <div class="form-group">
                                <label for="caibra_status">Presença de Cãibras:</label>
                                <select id="caibra_status" name="caibra_status" required>
                                    <option value="">Selecione...</option>
                                    <option value="0">Ausente</option>
                                    <option value="1">Presente</option>
                                </select>
                                <small>Cãibras musculares relatadas pelo paciente</small>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="button-container">
                    <button type="submit">
                        <i class="fas fa-calculator"></i>
                        Calcular Predição
                    </button>
                </div>
            </form>
        </div>
        
        <!-- Loading -->
        <div id="loading" class="loading" style="display: none;">
            <div class="spinner"></div>
            <h3>Processando dados...</h3>
            <p>Analisando parâmetros clínicos</p>
        </div>
        
        <!-- Resultado -->
        <div id="result" class="result-card" style="display: none;">
            <div class="result-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            <h2>Resultado da Predição</h2>
            <div class="prediction-type" id="predictionType">ESTRUTURAL</div>
            <div class="confidence-bar">
                <div class="confidence-fill" id="confidenceFill"></div>
            </div>
            <p><strong>Nível de Confiança:</strong> <span id="confidenceValue">0</span></p>
            <p style="margin-top: 20px;">
                <small>Esta predição é baseada em análise de padrões clínicos e laboratoriais. 
                Sempre consulte um especialista para diagnóstico definitivo.</small>
            </p>
        </div>
        
        <!-- Erro -->
        <div id="error" class="error-card" style="display: none;">
            <div class="error-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <h2>Erro na Predição</h2>
            <p id="errorMessage">Ocorreu um erro no processamento.</p>
            <button type="button" onclick="document.getElementById('error').style.display='none'">
                <i class="fas fa-times"></i> Fechar
            </button>
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
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('predictionType').textContent = data.prediction;
                    document.getElementById('confidenceValue').textContent = data.confidence + '%';
                    
                    // Atualizar barra de confiança
                    document.getElementById('confidenceFill').style.width = data.confidence + '%';
                    
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
    try:
        # Extrair valores
        maior_cpk = float(data['Maior_Cpk'])
        menor_cpk = float(data['Menor_Cpk'])
        maior_lactato = float(data['Maior_Lactato'])
        menor_lactato = float(data['Menor_Lactato'])
        dor_presente = int(data['Dor_Presente'])
        mialgia_status = int(data['Mialgia_Status'])
        mialgia_inicial = int(data['Mialgia_Inicial_Tipo'])
        mialgia_atual = int(data['Mialgia_Atual_Tipo'])
        fadiga_status = int(data['Fadiga_Status'])
        caibra_status = int(data['Caibra_Status'])
        
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
        
    except Exception as e:
        raise ValueError(f"Erro no cálculo da predição: {str(e)}")

@app.route('/')
def index():
    """Página principal"""
    try:
        return get_html_template()
    except Exception as e:
        return f"Erro interno: {str(e)}", 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint de predição"""
    try:
        # Verificar se há dados
        if not request.form:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado recebido'
            })
        
        # Receber dados do formulário
        data = {}
        required_fields = [
            'maior_cpk', 'menor_cpk', 'maior_lactato', 'menor_lactato',
            'dor_presente', 'mialgia_status', 'mialgia_inicial_tipo',
            'mialgia_atual_tipo', 'fadiga_status', 'caibra_status'
        ]
        
        # Verificar campos obrigatórios
        for field in required_fields:
            if field not in request.form or request.form[field] == '':
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório não preenchido: {field}'
                })
        
        # Converter e validar dados
        try:
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
        except (ValueError, TypeError) as e:
            return jsonify({
                'success': False,
                'error': f'Erro na conversão dos dados: {str(e)}'
            })
        
        # Validar dados básicos
        if data['Maior_Cpk'] < 0 or data['Menor_Cpk'] < 0:
            return jsonify({
                'success': False,
                'error': 'Valores de CPK não podem ser negativos'
            })
            
        if data['Maior_Lactato'] < 0 or data['Menor_Lactato'] < 0:
            return jsonify({
                'success': False,
                'error': 'Valores de Lactato não podem ser negativos'
            })
        
        if data['Maior_Cpk'] < data['Menor_Cpk']:
            return jsonify({
                'success': False,
                'error': 'Maior CPK não pode ser menor que Menor CPK'
            })
        
        if data['Maior_Lactato'] < data['Menor_Lactato']:
            return jsonify({
                'success': False,
                'error': 'Maior Lactato não pode ser menor que Menor Lactato'
            })
        
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
            'error': str(e)
        })
    except Exception as e:
        # Log do erro completo para debug
        error_trace = traceback.format_exc()
        print(f"Erro na predição: {error_trace}")
        
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        })

@app.route('/api/health')
def health():
    """Endpoint de saúde"""
    try:
        return jsonify({
            'status': 'healthy', 
            'message': 'Calculadora de Miopatia funcionando',
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Endpoint de compatibilidade
@app.route('/predict', methods=['POST'])
def predict_compat():
    """Endpoint de compatibilidade - redireciona para /api/predict"""
    return predict()

@app.route('/health')
def health_compat():
    """Endpoint de compatibilidade - redireciona para /api/health"""
    return health()

# Handler para Vercel
def handler(event, context):
    """Handler para AWS Lambda/Vercel"""
    return app(event, context)

# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True, port=5000) 