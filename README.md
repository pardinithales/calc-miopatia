# 🩺 Calculadora de Miopatia

Um aplicativo web moderno para predição automática de tipos de miopatia usando Machine Learning.

## 📋 Características

- **Interface moderna e responsiva** - Design clean e intuitivo
- **Predição automática** - Utiliza modelo Random Forest treinado
- **Classificação binária** - Distingue entre miopatia Estrutural e Metabólica
- **Confiança da predição** - Mostra o nível de confiança do resultado
- **Processamento em tempo real** - Resultados instantâneos

## 🚀 Como usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o aplicativo

```bash
python app.py
```

### 3. Acessar no navegador

Abra seu navegador e acesse: `http://localhost:5000`

## 📊 Dados necessários

O aplicativo requer os seguintes parâmetros do paciente:

### Valores Laboratoriais
- **Maior CPK** - Valor máximo de CPK registrado
- **Menor CPK** - Valor mínimo de CPK registrado  
- **Maior Lactato** - Valor máximo de lactato registrado
- **Menor Lactato** - Valor mínimo de lactato registrado

### Sintomas Gerais
- **Dor Presente** - Presença ou ausência de dor
- **Status de Fadiga** - Presença ou ausência de fadiga
- **Status de Cãibra** - Presença ou ausência de cãibras

### Características da Mialgia
- **Status da Mialgia** - Presença ou ausência de mialgia
- **Tipo Inicial da Mialgia** - Classificação inicial (tipos 3, 4, 5)
- **Tipo Atual da Mialgia** - Classificação atual (tipos 3, 4, 5)

## 🎯 Resultados

O sistema fornece:

- **Tipo de Miopatia** - Estrutural ou Metabólico
- **Nível de Confiança** - Percentual de certeza da predição

## 🔬 Modelo

- **Algoritmo**: Random Forest Classifier
- **Balanceamento**: SMOTE (Synthetic Minority Oversampling Technique)
- **Padronização**: StandardScaler
- **Validação**: Train/Test Split (80/20)

## 📁 Estrutura do projeto

```
CALC_MIOPATIA/
├── app.py              # Aplicação Flask principal
├── df.csv              # Dataset para treinamento
├── requirements.txt    # Dependências Python
├── templates/
│   └── index.html     # Interface web
├── static/
│   └── style.css      # Estilos CSS
└── README.md          # Documentação
```

## ⚠️ Importante

Este sistema é uma ferramenta de apoio ao diagnóstico e **não substitui** a avaliação médica profissional. Sempre consulte um especialista para diagnóstico definitivo.

## 🛠️ Tecnologias utilizadas

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, imbalanced-learn
- **Data Science**: pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript
- **UI/UX**: Design responsivo moderno

---

💡 **Desenvolvido para auxiliar profissionais da saúde no diagnóstico de miopatias** 