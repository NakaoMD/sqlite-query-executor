class StateManager:
    def __init__(self):
        self.pull_request_cache = {}
        self.database_cache = {}

    def get_pr_count(self, repo_url):
        return self.pull_request_cache.get(repo_url, 0)

    def set_pr_count(self, repo_url, count):
        self.pull_request_cache[repo_url] = count

    def get_data(self, query):
        return self.database_cache.get(query)

    def set_data(self, query, data):
        self.database_cache[query] = data

    def clear_cache(self):
        self.pull_request_cache.clear()
        self.database_cache.clear()

# Criação de uma instância global do gerenciador de estado
state_manager = StateManager()
