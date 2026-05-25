# Sistema de Detecção de Anomalias em Transações Financeiras

Este repositório contém o Produto de Software desenvolvido pela equipe da **Residência em Software: Banco do Brasil - SQUAD 01**. O sistema consiste em uma API REST estruturada para o gerenciamento de transações financeiras e triagem automatizada de comportamentos suspeitos através de análises heurísticas e estatísticas descritivas.

---

## 🏗️ Arquitetura do Sistema

A aplicação adota o modelo cliente-servidor organizado em 5 camadas funcionais principais:

1. **Camada de Apresentação:** Interface interativa Swagger UI gerada de forma automática pelo FastAPI.
2. **Camada de Roteamento:** Módulos do FastAPI que recebem as requisições HTTP e as encaminham para os controladores adequados[cite: 1].
3. **Camada de Validação:** Esquemas do Pydantic que garantem a tipagem, obrigatoriedade e restrições dos dados recebidos antes da persistência ou análise[cite: 1].
4. **Camada de Persistência:** SQLAlchemy atuando como ORM para mapear o modelo de dados à base relacional MySQL[cite: 1].
5. **Camada Analítica:** Biblioteca Pandas para processamento estatístico de forma independente do banco relacional, utilizando o arquivo local `transacoes_treino.json`[cite: 1].

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem Principal:** Python 3.10 ou superior[cite: 1].
* **Framework Web:** FastAPI[cite: 1].
* **Servidor ASGI:** Uvicorn[cite: 1].
* **Mapeamento Objeto-Relacional (ORM):** SQLAlchemy com driver PyMySQL[cite: 1].
* **Validação e Schemas:** Pydantic[cite: 1].
* **Manipulação Analítica:** Pandas[cite: 1].
* **Banco de Dados:** MySQL[cite: 1].

---

## 📊 Modelo e Dicionário de Dados

A persistência do MVP do sistema é concentrada na tabela `transacoes`[cite: 1]. Veja abaixo a estrutura e a tipagem de cada campo[cite: 1]:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INT (PK) | Identificador único da transação[cite: 1]. |
| `valor` | FLOAT | Valor monetário da operação (deve ser maior que zero)[cite: 1]. |
| `data` | VARCHAR | Data da transação[cite: 1]. |
| `hora` | VARCHAR | Horário da transação[cite: 1]. |
| `dia_semana` | VARCHAR | Dia da semana em que ocorreu a operação[cite: 1]. |
| `categoria` | VARCHAR | Categoria da transação (usada para médias e comparação)[cite: 1]. |
| `conta` | VARCHAR | Conta associada à transação[cite: 1]. |
| `cidade` | VARCHAR | Cidade onde a transação foi registrada[cite: 1]. |
| `estado` | VARCHAR | Estado relacionado à localização da transação[cite: 1]. |
| `pais` | VARCHAR | País da transação[cite: 1]. |
| `latitude` | FLOAT | Coordenada geográfica de latitude[cite: 1]. |
| `longitude` | FLOAT | Coordenada geográfica de longitude[cite: 1]. |
| `tipo_transacao` | VARCHAR | Tipo de movimentação financeira[cite: 1]. |
| `dispositivo` | VARCHAR | Dispositivo utilizado na operação[cite: 1]. |
| `estabelecimento` | VARCHAR | Estabelecimento associado à transação[cite: 1]. |
| `tentativas` | INT | Número de tentativas relacionadas (deve ser maior ou igual a zero)[cite: 1]. |
| `ip_origem` | VARCHAR | Endereço IP de origem[cite: 1]. |
| `is_fraude` | INT | Indicador binário de fraude: 0 para normal, 1 para fraude[cite: 1]. |

---

## ⚙️ Regras de Negócio (RN)

As seguintes regras foram implementadas de acordo com as especificações do sistema[cite: 1]:

* **RN04 (Integridade):** Não é permitido cadastrar duas transações com o mesmo identificador (Gera Erro HTTP 400)[cite: 1].
* **RN05 (Validação):** Valores de transação devem ser estritamente maiores que zero, o número de tentativas não pode ser negativo e o indicador de fraude aceita apenas os valores inteiros 0 ou 1[cite: 1].
* **RN06 (Consulta por ID):** Consultas a IDs inexistentes na base devem retornar erro HTTP 404 (Not Found)[cite: 1].
* **Lógica de Anomalias (`GET /anomalies`):** Uma transação do banco MySQL é classificada como anômala caso atenda a um ou mais dos seguintes critérios objetivos[cite: 1]:
  1. *Valor Elevado:* valor superior a 3000[cite: 1].
  2. *Horário da Madrugada:* Realizada entre 0h e 5h59[cite: 1].
  3. *Múltiplas Tentativas:* número de tentativas maior que 2[cite: 1].

---

## 🛣️ Estrutura de Endpoints da API

Todos os retornos de endpoints seguem o padrão estruturado em formato JSON[cite: 1].

### Gerenciamento de Transações (CRUD) e Detecção
* `GET /transactions` - Lista transações com filtros cumulativos opcionais[cite: 1].
* `GET /transactions/{id}` - Busca uma transação específica pelo identificador único[cite: 1].
* `POST /transactions` - Cadastra uma nova transação financeira aplicando validações do schema[cite: 1].
* `PUT /transactions/{id}` - Atualiza os dados de uma transação existente[cite: 1].
* `DELETE /transactions/{id}` - Remove fisicamente uma transação do banco MySQL[cite: 1].
* `GET /anomalies` - Executa a lógica de detecção de anomalias sobre as transações[cite: 1].

### Rotas de Análise Complementar (Processadas via Pandas)
Estas rotas utilizam diretamente o arquivo `dados/transacoes_treino.json`[cite: 1]:
* `GET /analise/dispositivo-influencia` - Identifica o dispositivo com a maior taxa média de fraude[cite: 1].
* `GET /analise/tentativas-fraude` - Compara a média de tentativas entre transações normais e fraudes[cite: 1].
* `GET /analise/conta-mais-transacoes` - Identifica a conta com o maior volume de transações registradas[cite: 1].
* `GET /analise/fraude-horario` - Identifica o horário (hora do dia) com maior ocorrência de fraudes[cite: 1].
* `GET /analise/madrugada` - Conta o total de transações efetuadas entre 0h e 5h[cite: 1].
* `GET /analise/media-categoria` - Retorna a média de valor monetário agrupada por categoria[cite: 1].
* `GET /analise/cidade-fora-pe` - Identifica a cidade fora do estado de Pernambuco com maior ocorrência de transações[cite: 1].
* `GET /analise/comparacao-dispositivo` - Calcula a média de valor das transações por tipo de dispositivo utilizado[cite: 1].
* `GET /analise/valor-suspeito` - Conta transações cujo valor supera o dobro da média de sua respectiva categoria[cite: 1].

---

## 🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para implantar a aplicação em sua máquina local[cite: 1]:

1. **Navegue até a pasta raiz:** Acesse a pasta do projeto através do terminal[cite: 1]:
```bash
   cd caminho/do/projeto





# API de Transações

API REST desenvolvida com FastAPI para gerenciamento de transações financeiras.

## Como rodar

```bash
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload


Acessa:
http://127.0.0.1:8000/docs

--------------------------------------------------------------------------------------------------------

Após ter realizado as instruções acima execute "venv\Scripts\activate" e "python -m uvicorn app.main:app --reload" para iniciar o ambiente virtual e rodar a API
