# Motor Executor

Este projeto é um executor de consultas SQLite com uma interface gráfica para gerenciamento de repositórios e pull requests. Ele suporta funcionalidades para autenticação de usuários, gestão de repositórios e envio de feedback.

## Funcionalidades

- **Login de Usuário**
  - Autenticação de usuário com opções predefinidas (`admin` e `ih8`).
  - Sistema de autenticação com senha mascarada.

- **Admin Panel**
  - Painel de administração acessível pelo usuário `admin`.
  - Funcionalidade de listar, editar, excluir e adicionar repositórios.
  - Rolagem infinita na lista de repositórios.
  - Botão de logoff.

- **Repositórios**
  - Listagem de repositórios ativos para o usuário `ih8`.
  - Filtragem de repositórios por status (ativado/desativado).

- **Pull Requests**
  - Aba de Pull Requests com funcionalidade para listar e atualizar contagem de pull requests.
  - Botão de atualização e fechamento da janela de pull requests.

- **Interface do Usuário**
  - Melhorias na responsividade das janelas de edição e adição de repositórios.
  - Feedback visual para ações do usuário.
  - Tooltips e ícones para melhor usabilidade.

- **Banco de Dados**
  - Funções para manipulação de dados no banco de dados `people.db`.
  - Adição de colunas e atualizações de status.

## Pré-requisitos

- Python 3.x
- Tkinter
- Requests
- SQLite

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
python main.py

sqlite-query-executor/
│
├── data/
│   ├── __init__.py
│   ├── database.py
│   └── queries.py
│
├── icons/
│   ├── play.png
│   ├── search.png
│   ├── cloud-download.png
│   ├── git.png
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── repo_window.py
│   ├── pull_requests_window.py
│   ├── data_window.py
│   ├── feedback_window.py
│   ├── login_window.py
│   └── utils.py
│
├── main.py
├── README.md
├── requirements.txt
└── setup.py

Arquivos Principais
main.py: Arquivo principal para iniciar o aplicativo.
data/database.py: Conexão e operações com o banco de dados SQLite.
ui/main_window.py: Interface principal do usuário com abas para dados, repositórios e pull requests.
ui/repo_window.py: Janela de repositórios.
ui/pull_requests_window.py: Janela de pull requests.
ui/data_window.py: Janela de dados.
ui/feedback_window.py: Janela para envio de feedback (em desenvolvimento).
ui/login_window.py: Janela de login.