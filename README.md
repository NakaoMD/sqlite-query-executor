# SQLite Query Executor

Este projeto é um executor de consultas SQLite com atualização automática via GitHub Releases.

## Configuração do Ambiente

1. Crie um ambiente virtual (opcional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure o banco de dados:
    ```bash
    python database_setup.py
    ```

## Executando o Aplicativo

Para iniciar o aplicativo, execute:
```bash
python start_app.py
