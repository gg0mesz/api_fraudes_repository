# Sistema de Detecção de Anomalias em Transações Financeiras

[cite_start]Este repositório contém o Produto de Software desenvolvido pela equipe da **Residência em Software: Banco do Brasil - SQUAD 01**[cite: 11, 13]. [cite_start]O sistema consiste em uma API REST estruturada para o gerenciamento de transações financeiras e triagem automatizada de comportamentos suspeitos através de análises heurísticas e estatísticas descritivas[cite: 21, 22, 25].

---

## 🏗️ Arquitetura do Sistema

[cite_start]A aplicação adota o modelo cliente-servidor organizado em 5 camadas funcionais principais[cite: 327, 331]:

1. [cite_start]**Camada de Apresentação:** Interface interativa Swagger UI gerada de forma automática pelo FastAPI[cite: 331].
2. [cite_start]**Camada de Roteamento:** Módulos do FastAPI que recebem as requisições HTTP e as encaminham para os controladores adequados[cite: 332].
3. [cite_start]**Camada de Validação:** Esquemas do Pydantic que garantem a tipagem, obrigatoriedade e restrições dos dados recebidos antes da persistência ou análise[cite: 333].
4. [cite_start]**Camada de Persistência:** SQLAlchemy atuando como ORM para mapear o modelo de dados à base relacional MySQL[cite: 334].
5. [cite_start]**Camada Analítica:** Biblioteca Pandas para processamento estatístico de forma independente do banco relacional, utilizando o arquivo local `transacoes_treino.json`[cite: 335].

---

## 🛠️ Tecnologias Utilizadas

* [cite_start]**Linguagem Principal:** Python 3.10 ou superior [cite: 597, 697]
* [cite_start]**Framework Web:** FastAPI [cite: 597]
* [cite_start]**Servidor ASGI:** Uvicorn [cite: 597]
* [cite_start]**Mapeamento Objeto-Relacional (ORM):** SQLAlchemy com driver PyMySQL [cite: 598]
* [cite_start]**Validação e Schemas:** Pydantic [cite: 599]
* [cite_start]**Manipulação Analítica:** Pandas [cite: 599]
* [cite_start]**Banco de Dados:** MySQL [cite: 600]

---

## 📊 Modelo e Dicionário de Dados

[cite_start]A persistência do MVP do sistema é concentrada na tabela `transacoes`[cite: 550, 557]. [cite_start]Veja abaixo a estrutura e a tipagem de cada campo[cite: 592]:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INT (PK) | [cite_start]Identificador único da transação[cite: 592]. |
| `valor` | FLOAT | [cite_start]Valor monetário da operação (deve ser maior que zero)[cite: 126, 592]. |
| `data` | VARCHAR(20) | [cite_start]Data da transação no formato YYYY-MM-DD[cite: 592, 738]. |
| `hora` | VARCHAR(20) | [cite_start]Horário da transação no formato HH:MM:SS[cite: 592, 738]. |
| `dia_semana` | VARCHAR(20) | [cite_start]Dia da semana em que ocorreu a operação[cite: 592]. |
| `categoria` | VARCHAR(100) | [cite_start]Categoria da transação (usada para médias e comparação)[cite: 592]. |
| `conta` | VARCHAR(100) | [cite_start]Conta bancária de origem associada à transação[cite: 592]. |
| `cidade` | VARCHAR(100) | [cite_start]Cidade onde a transação foi registrada[cite: 592]. |
| `estado` | VARCHAR(50) | [cite_start]Estado relacionado à localização[cite: 592]. |
| `pais` | VARCHAR(50) | [cite_start]País da transação[cite: 592]. |
| `latitude` | FLOAT | [cite_start]Coordenada geográfica de latitude[cite: 592]. |
| `longitude` | FLOAT | [cite_start]Coordenada geográfica de longitude[cite: 592]. |
| `tipo_transacao` | VARCHAR(100) | [cite_start]Tipo de movimentação financeira (ex: transferência, pagamento)[cite: 592, 731]. |
| `dispositivo` | VARCHAR(100) | [cite_start]Dispositivo utilizado na operação (ex: mobile, desktop)[cite: 592, 731]. |
| `estabelecimento` | VARCHAR(150) | [cite_start]Estabelecimento associado à transação[cite: 592]. |
| `tentativas` | INT | [cite_start]Número de tentativas relacionadas (deve ser maior ou igual a zero)[cite: 126, 592]. |
| `ip_origem` | VARCHAR(50) | [cite_start]Endereço IP de origem da requisição[cite: 595]. |
| `is_fraude` | INT | [cite_start]Indicador binário de fraude: 0 para normal, 1 para fraude[cite: 595]. |

---

## ⚙️ Regras de Negócio (RN)

[cite_start]As seguintes regras foram implementadas de acordo com as especificações do sistema[cite: 125]:

* [cite_start]**RN04 (Integridade):** Não é permitido cadastrar duas transações com o mesmo identificador (Gera Erro HTTP 400)[cite: 126, 652].
* [cite_start]**RN05 (Validação):** Valores de transação devem ser estritamente maiores que zero, o número de tentativas não pode ser negativo e o indicador de fraude aceita apenas os valores inteiros 0 ou 1[cite: 126].
* [cite_start]**RN06 (Consulta por ID):** Consultas a IDs inexistentes na base devem retornar erro HTTP 404 (Not Found)[cite: 126, 649].
* [cite_start]**Lógica de Anomalias (`GET /anomalies`):** Uma transação do banco MySQL é classificada como anômala caso atenda a um ou mais dos seguintes critérios objetivos[cite: 411]:
  1. [cite_start]*Valor Elevado:* `valor > 3000` (Motivo: "high value") [cite: 411, 752]
  2. [cite_start]*Horário da Madrugada:* Realizada entre 00:00h e 05:59h (Motivo: "transaction at dawn") [cite: 620, 753]
  3. [cite_start]*Múltiplas Tentativas:* `tentativas > 2` (Motivo: "too many attempts") [cite: 411, 753]

---

## 🛣️ Estrutura de Endpoints da API

[cite_start]Todos os retornos de endpoints seguem o padrão estruturado em formato JSON[cite: 636].

### Gerenciamento de Transações (CRUD) e Detecção

* [cite_start]`GET /transactions` - Lista transações com filtros cumulativos opcionais (categoria, cidade, valores mínimos e máximos, tipo, dispositivo, data, is_fraude)[cite: 640, 731, 732].
* [cite_start]`GET /transactions/{id}` - Busca uma transação específica pelo identificador único[cite: 640].
* [cite_start]`POST /transactions` - Cadastra uma nova transação financeira aplicando validações do schema[cite: 640].
* [cite_start]`PUT /transactions/{id}` - Atualiza os dados de uma transação existente[cite: 640].
* [cite_start]`DELETE /transactions/{id}` - Remove fisicamente uma transação do banco MySQL[cite: 640, 748].
* [cite_start]`GET /anomalies` - Executa a lógica de detecção de anomalias sobre as transações persistidas no banco[cite: 640].

### Rotas de Análise Complementar (Processadas via Pandas)

[cite_start]Estas rotas utilizam diretamente o arquivo `dados/transacoes_treino.json` para as estatísticas e agrupamentos[cite: 624]:

* [cite_start]`GET /analise/dispositivo-influencia` - Identifica o dispositivo com a maior taxa média de fraude[cite: 625, 640].
* [cite_start]`GET /analise/tentativas-fraude` - Compara a média de tentativas entre transações normais e fraudes[cite: 626, 640].
* [cite_start]`GET /analise/conta-mais-transacoes` - Identifica a conta com o maior volume de transações registradas[cite: 627, 640].
* [cite_start]`GET /analise/fraude-horario` - Identifica o horário (hora do dia) com maior ocorrência de fraudes[cite: 628, 640].
* [cite_start]`GET /analise/madrugada` - Conta o total de transações efetuadas entre 0h e 5h[cite: 629, 640].
* [cite_start]`GET /analise/media-categoria` - Retorna a média de valor monetário agrupada por categoria[cite: 630, 640].
* [cite_start]`GET /analise/cidade-fora-pe` - Identifica a cidade fora do estado de Pernambuco com maior ocorrência de transações[cite: 631, 640].
* [cite_start]`GET /analise/comparacao-dispositivo` - Calcula a média de valor das transações por tipo de dispositivo utilizado[cite: 632, 640].
* [cite_start]`GET /analise/valor-suspeito` - Conta transações cujo valor supera o dobro da média de sua respectiva categoria[cite: 633, 640].

---

## 🚀 Como Executar o Projeto Localmente

[cite_start]Siga o passo a passo abaixo para implantar a aplicação em sua máquina local[cite: 696]:

1. [cite_start]**Instale o Python:** Certifique-se de ter o Python 3.10 ou superior instalado[cite: 697].
2. [cite_start]**Navegue até a pasta raiz:** Acesse a pasta do projeto através do terminal de sua preferência[cite: 699]:
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
