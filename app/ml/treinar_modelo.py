import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

with open('dados/transacoes_treino.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['hora_int'] = df['hora'].str.split(':').str[0].astype(int)

encoders = {}
for col in ['dispositivo', 'tipo_transacao', 'categoria']:
    le = LabelEncoder()
    df[f'{col}_enc'] = le.fit_transform(df[col])
    encoders[col] = le

features = [
    'valor', 'hora_int', 'tentativas', 'latitude', 'longitude',
    'dispositivo_enc', 'tipo_transacao_enc', 'categoria_enc'
]

X = df[features].fillna(0)
y = df['is_fraude']
fraude_rate = y.mean()
print(f'Taxa de fraude no treino: {fraude_rate:.2%}')

modelo = IsolationForest(
    n_estimators=100,
    contamination=fraude_rate,
    random_state=42
)
modelo.fit(X)


predicoes = modelo.predict(X)
predicoes_bin = (predicoes == -1).astype(int)

metricas = {
    "acuracia":  round(accuracy_score(y, predicoes_bin) * 100, 1),
    "precisao":  round(precision_score(y, predicoes_bin, zero_division=0) * 100, 1),
    "recall":    round(recall_score(y, predicoes_bin, zero_division=0) * 100, 1),
    "f1_score":  round(f1_score(y, predicoes_bin, zero_division=0) * 100, 1)
}

print(f'Acurácia:  {metricas["acuracia"]}%')
print(f'Precisão:  {metricas["precisao"]}%')
print(f'Recall:    {metricas["recall"]}%')
print(f'F1-Score:  {metricas["f1_score"]}%')

artefato = {
    'modelo':   modelo,
    'encoders': encoders,
    'features': features,
    'metricas': metricas
}

with open('app/ml/modelo.pkl', 'wb') as f:
    pickle.dump(artefato, f)

print('Salvo em app/ml/modelo.pkl ✓')