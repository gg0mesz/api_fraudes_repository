import pandas as pd
from sqlalchemy import create_engine

df = pd.read_json('dados/transacoes_treino.json')

engine = create_engine('mysql+pymysql://bancodobrasil:12345@localhost:3306/bancodobrasil')

df.to_sql('transacoes', engine, if_exists='replace', index=False)

print("Banco criado com sucesso!")