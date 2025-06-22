import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import warnings
warnings.filterwarnings('ignore')

def train_and_save_model():
    """Treina o modelo e salva como arquivo pickle"""
    print("Carregando dados...")
    
    # Carregando o dataset
    df = pd.read_csv('df.csv')
    
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
    
    print("Treinando modelo...")
    
    # Dividindo em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Padronizando as características
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Treinando o modelo
    rf_model = RandomForestClassifier(
        random_state=42,
        class_weight='balanced',
        n_estimators=50,  # Reduzido para economizar espaço
        max_depth=10      # Limitando profundidade
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Avaliando o modelo
    score = rf_model.score(X_test_scaled, y_test)
    print(f"Acurácia do modelo: {score:.2f}")
    
    # Salvando o modelo e scaler
    print("Salvando modelo...")
    with open('model.pkl', 'wb') as f:
        pickle.dump({
            'model': rf_model,
            'scaler': scaler,
            'feature_names': X.columns.tolist()
        }, f)
    
    print("Modelo salvo como 'model.pkl'")
    return True

if __name__ == '__main__':
    train_and_save_model() 