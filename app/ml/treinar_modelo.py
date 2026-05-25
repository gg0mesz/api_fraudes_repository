import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

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
fraude_rate = df['is_fraude'].mean()
print(f'Taxa de fraude no treino: {fraude_rate:.2%}')

modelo = IsolationForest(
    n_estimators=100, contamination=fraude_rate, random_state=42)
modelo.fit(X)
print('Modelo treinado!')

artefato = {'modelo': modelo, 'encoders': encoders, 'features': features}

with open('app/ml/modelo.pkl', 'wb') as f:
    pickle.dump(artefato, f)

print('Salvo em app/ml/modelo.pkl ✓')
