# Sistema de Detecção de Anomalias em Transações Financeiras

[cite_start]Este repositório contém o Produto de Software desenvolvido pela equipe da **Residência em Software: Banco do Brasil - SQUAD 01**[cite: 13]. [cite_start]O sistema consiste em uma API REST estruturada para o gerenciamento de transações financeiras e triagem automatizada de comportamentos suspeitos através de análises heurísticas e estatísticas descritivas[cite: 21, 22, 68].

## 🏗️ Arquitetura do Sistema

[cite_start]A aplicação adota o modelo cliente-servidor organizado em 5 camadas principais para garantir modularidade e manutenibilidade[cite: 327, 331]:

1. [cite_start]**Camada de Apresentação:** Interface interativa Swagger UI gerada de forma automática[cite: 331].
2. [cite_start]**Camada de Roteamento:** Módulos do FastAPI responsáveis por receber requisições HTTP e encaminhá-las[cite: 332].
3. [cite_start]**Camada de Validação:** Esquemas do Pydantic que validam os tipos e as restrições dos dados recebidos antes de persistir ou analisar[cite: 333].
4. [cite_start]**Camada de Persistência:** SQLAlchemy atuando como ORM para mapear o modelo à base de dados relacional MySQL[cite: 334].
5. [cite_start]**Camada Analítica:** Biblioteca Pandas para processamento estatístico independente do banco relacional, utilizando o arquivo `transacoes_treino.json`[cite: 335].

---

## 🛠️ Tecnologias Utilizadas

* [cite_start]**Linguagem Principal:** Python [cite: 597]
* [cite_start]**Framework Web:** FastAPI [cite: 597]
* [cite_start]**Servidor ASGI:** Uvicorn [cite: 597]
* [cite_start]**Mapeamento Objeto-Relacional (ORM):** SQLAlchemy com driver PyMySQL [cite: 598]
* [cite_start]**Validação e Schemas:** Pydantic [cite: 599]
* [cite_start]**Manipulação Analítica:** Pandas [cite: 599]
* [cite_start]**Banco de Dados:** MySQL [cite: 600]

---

## 📊 Modelo e Dicionário de Dados

[cite_start]Os dados são concentrados na tabela `transacoes`[cite: 550, 557]. [cite_start]A estrutura física da tabela no MySQL possui os seguintes campos[cite: 578, 592]:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INT (PK) | [cite_start]Identificador único da transação[cite: 579, 592]. |
| `valor` | FLOAT | [cite_start]Valor monetário da operação (deve ser maior que zero)[cite: 580, 643]. |
| `data` | VARCHAR(20) | [cite_start]Data da transação no formato YYYY-MM-DD[cite: 580, 731]. |
| `hora` | VARCHAR(20) | [cite_start]Horário da transação no formato HH:MM:SS[cite: 581, 738]. |
| `dia_semana` | VARCHAR(20)| [cite_start]Dia da semana em que ocorreu a operação[cite: 581, 592]. |
| `categoria` | VARCHAR(100)| [cite_start]Categoria da transação (usada para médias e comparação)[cite: 581, 592]. |
| `conta` | VARCHAR(100)| [cite_start]Conta bancária de origem associada à transação[cite: 581, 592]. |
| `cidade` | VARCHAR(100)| [cite_start]Cidade onde a transação foi registrada[cite: 581, 592]. |
| `estado` | VARCHAR(50) | [cite_start]Estado relacionado à localização[cite: 581, 592]. |
| `pais` | VARCHAR(50) | [cite_start]País da transação[cite: 582, 592]. |
| `latitude` | FLOAT | [cite_start]Coordenada geográfica de latitude[cite: 585, 592]. |
| `longitude` | FLOAT | [cite_start]Coordenada geográfica de longitude[cite: 586, 592]. |
| `tipo_transacao`| VARCHAR(100)| [cite_start]Tipo de movimentação financeira (ex: transferência, pagamento)[cite: 587, 731]. |
| `dispositivo` | VARCHAR(100)| [cite_start]Dispositivo utilizado na operação (ex: mobile, desktop)[cite: 587, 731]. |
| `estabelecimento`| VARCHAR(150)| [cite_start]Estabelecimento associado à transação[cite: 588, 592]. |
| `tentativas` | INT | [cite_start]Número de tentativas relacionadas (deve ser $\ge 0$)[cite: 588, 644]. |
| `ip_origem` | VARCHAR(50) | [cite_start]Endereço IP de origem da requisição[cite: 589, 592]. |
| `is_fraude` | INT | [cite_start]Indicador binário de fraude: 0 para normal, 1 para fraude[cite: 590, 595]. |

---

## ⚙️ Regras de Negócio (RN) e Detecção de Anomalias

[cite_start]O sistema deve implementar obrigatoriamente as seguintes regras lógicas[cite: 125]:
* [cite_start]**RN04 (Integridade):** Não é permitido cadastrar duas transações com o mesmo identificador (Erro 400 se duplicado)[cite: 126, 652].
* [cite_start]**RN05 (Validação):** Valores devem ser maiores que zero, tentativas não podem ser negativas e o indicador de fraude aceita apenas 0 ou 1[cite: 126].
* [cite_start]**RN06 (Consulta por ID):** Consultas a IDs inexistentes devem retornar erro HTTP 404[cite: 126, 649].
* [cite_start]**Lógica de Anomalias (`GET /anomalies`):** Uma transação do banco de dados é classificada como anômala se atender a um ou mais dos seguintes critérios fixos[cite: 618, 619, 622]:
  1. [cite_start]*Valor Elevado:* `valor > 3000` (motivo: "high value")[cite: 619, 752].
  2. [cite_start]*Horário Atípico:* Realizada na madrugada entre 00:00h e 05:59h (motivo: "transaction at dawn")[cite: 620, 753].
  3. [cite_start]*Múltiplas Tentativas:* `tentativas > 2` (motivo: "too many attempts")[cite: 621, 753].

---

## 🛣️ Estrutura de Endpoints da API

[cite_start]Todas as rotas analíticas e de gerenciamento respondem com dados estruturados em formato JSON[cite: 59, 636].

### Gerenciamento de Transações (CRUD)
* [cite_start]`GET /transactions` - Lista transações com suporte a filtros cumulativos (categoria, cidade, valores mín/máx, tipo, dispositivo, data, is_fraude)[cite: 640, 731, 732].
* [cite_start]`GET /transactions/{id}` - Busca uma transação específica pelo identificador único[cite: 640].
* [cite_start]`POST /transactions` - Cadastra uma nova transação financeira validada pelo esquema[cite: 133, 640].
* [cite_start]`PUT /transactions/{id}` - Atualiza os dados de uma transação existente[cite: 640].
* [cite_start]`DELETE /transactions/{id}` - Remove fisicamente uma transação pelo ID[cite: 640, 748].
* [cite_start]`GET /anomalies` - Executa a lógica de detecção heurística nas transações do banco e retorna os motivos[cite: 618, 640].

### Rotas de Análise Complementar (Módulo /analise com Pandas)
[cite_start]Essas rotas utilizam o arquivo `dados/transacoes_treino.json` de forma independente do banco MySQL[cite: 516, 624]:
* [cite_start]`GET /analise/dispositivo-influencia` - Identifica o dispositivo com a maior taxa média de fraude[cite: 625, 640].
* [cite_start]`GET /analise/tentativas-fraude` - Compara a média de tentativas entre transações normais e fraudes[cite: 626, 640].
* [cite_start]`GET /analise/conta-mais-transacoes` - Identifica a conta com o maior volume de transações registradas[cite: 627, 640].
* [cite_start]`GET /analise/fraude-horario` - Identifica o horário (hora do dia) com maior ocorrência de fraudes[cite: 628, 640].
* [cite_start]`GET /analise/madrugada` - Conta o total de transações efetuadas entre 0h e 5h[cite: 629, 640].
* [cite_start]`GET /analise/media-categoria` - Retorna a média de valor monetário agrupada por categoria[cite: 630, 640].
* [cite_start]`GET /analise/cidade-fora-pe` - Identifica a cidade fora do estado de Pernambuco com maior ocorrência de transações[cite: 631, 640].
* [cite_start]`GET /analise/comparacao-dispositivo` - Calcula a média de valor das transações por tipo de dispositivo[cite: 632, 640].
* [cite_start]`GET /analise/valor-suspeito` - Conta transações cujo valor supera o dobro da média de sua respectiva categoria[cite: 633, 640].

---

## 🚀 Como Executar o Projeto Localmente

[cite_start]Siga o passo a passo exato abaixo para implantar a aplicação no seu ambiente de desenvolvimento[cite: 684, 696]:

1. [cite_start]**Verificar os pré-requisitos:** Certifique-se de possuir o Python 3.10 ou superior instalado localmente[cite: 697].
2. **Navegar até a pasta raiz:** Acesse a pasta do projeto via terminal:
   ```bash
   cd caminho/do/projeto
   [cite_start]
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
http://googleusercontent.com/immersive_entry_chip/2
http://googleusercontent.com/immersive_entry_chip/3
http://googleusercontent.com/immersive_entry_chip/4
http://googleusercontent.com/immersive_entry_chip/5







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
