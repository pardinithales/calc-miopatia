from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

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
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) 