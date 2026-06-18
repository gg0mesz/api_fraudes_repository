import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

df = pd.read_json('dados/transacoes_treino.json')

url = URL.create(
	drivername='mysql+pymysql',
	username='bancodobrasil',
	password='Lautaro@10',
	host='localhost',
	port=3306,
	database='bancodobrasil'
)

engine = create_engine(url)

df.to_sql('transacoes', engine, if_exists='replace', index=False)

print("Banco criado com sucesso!")