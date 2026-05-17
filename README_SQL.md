README_SQL.md (VERSÃO BÁSICA)
# Setup do Banco de Dados (MySQL)

## 1. Criar banco

```sql
CREATE DATABASE bancodobrasil; 

USE bancodobrasil;

2. Criar tabela
CREATE TABLE transacoes (
    id INT PRIMARY KEY,
    valor FLOAT,
    data DATE,
    hora TIME,
    dia_semana VARCHAR(20),
    categoria VARCHAR(50),
    conta VARCHAR(20),
    cidade VARCHAR(50),
    estado VARCHAR(10),
    pais VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    tipo_transacao VARCHAR(50),
    dispositivo VARCHAR(50),
    estabelecimento VARCHAR(100),
    tentativas INT,
    ip_origem VARCHAR(50),
    is_fraude INT
);
3. Importar dados

No terminal:

python importar_json_mysql.py


4. Testar banco
SELECT id, valor, cidade, tipo_transacao
FROM transacoes
LIMIT 10;

5. Confirmar quantidade de dados
SELECT COUNT(*) FROM transacoes;