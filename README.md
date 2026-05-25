[cite: 2]





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
