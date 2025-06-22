from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Uma página simples para confirmar que a rota principal funciona
    return """
    <h1>Olá, Mundo! A aplicação está no ar.</h1>
    <p>Este é um teste para diagnosticar o erro 500. Se você vê isso, o servidor Flask básico está funcionando.</p>
    <p>Agora, vamos testar o endpoint de predição com um formulário simples:</p>
    <form id="testForm">
        <button type="submit">Testar Predição</button>
    </form>
    <div id="result"></div>
    <script>
        document.getElementById('testForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = 'Enviando requisição...';
            try {
                const response = await fetch('/api/predict', { method: 'POST' });
                const data = await response.json();
                resultDiv.textContent = 'Resposta Recebida: ' + JSON.stringify(data);
            } catch (error) {
                resultDiv.textContent = 'Erro no fetch: ' + error;
            }
        });
    </script>
    """

@app.route('/api/predict', methods=['POST'])
def predict():
    # Uma resposta de predição falsa para testar o endpoint da API
    return jsonify({'success': True, 'prediction': 'Teste Bem-Sucedido', 'confidence': 100})

@app.route('/api/health')
def health():
    # Endpoint de saúde
    return jsonify({'status': 'healthy'})

# A instância 'app' do Flask é o que o runtime do Vercel espera encontrar.
# As rotas de compatibilidade e o handler antigo foram removidos para simplificar.

# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True, port=5000) 