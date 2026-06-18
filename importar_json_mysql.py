import json
import mysql.connector

print("🚀 Iniciando importação...")

# =========================
# 1. LER JSON
# =========================
try:
    with open("dados/transacoes_treino.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    print("📦 JSON carregado com sucesso")
    print("📊 Registros encontrados:", len(dados))
    print("🔎 Exemplo:", dados[0])

except Exception as e:
    print("❌ Erro ao ler JSON:")
    print(e)
    exit()

# =========================
# 2. CONECTAR MYSQL
# =========================
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="bancodobrasil",
        password="Lautaro@10",
        database="bancodobrasil"
    )

    cursor = conn.cursor()
    print("🔌 Conectado ao MySQL")

except Exception as e:
    print("❌ Erro ao conectar MySQL:")
    print(e)
    exit()

# =========================
# 3. SQL (COM dia_semana)
# =========================
sql = """
INSERT INTO transacoes (
    id, valor, data, hora, dia_semana, categoria, conta,
    cidade, estado, pais, latitude, longitude,
    tipo_transacao, dispositivo, estabelecimento,
    tentativas, ip_origem, is_fraude
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# =========================
# 4. INSERÇÃO
# =========================
try:
    for item in dados:
        print("➡ Inserindo ID:", item.get("id"))

        valores = (
            item.get("id"),
            item.get("valor"),
            item.get("data"),
            item.get("hora"),
            item.get("dia_semana", "N/A"),
            item.get("categoria"),
            item.get("conta"),
            item.get("cidade"),
            item.get("estado"),
            item.get("pais", "Brasil"),
            item.get("latitude"),
            item.get("longitude"),
            item.get("tipo_transacao"),
            item.get("dispositivo"),
            item.get("estabelecimento"),
            item.get("tentativas"),
            item.get("ip_origem"),
            item.get("is_fraude")
        )

        cursor.execute(sql, valores)

    conn.commit()
    print("✔ IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")

except Exception as e:
    print("❌ Erro durante inserção:")
    print(e)

finally:
    cursor.close()
    conn.close()
    print("🔒 Conexão fechada")