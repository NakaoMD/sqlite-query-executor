import check_for_updates
import query_executor

def main():
    # Verificar e atualizar o aplicativo
    if check_for_updates.check_for_updates():
        print("Aplicativo atualizado para a versão mais recente.")
    else:
        print("Aplicativo já está na versão mais recente.")

    # Executar o executor de consultas com a versão mais recente
    query_executor.run_query_executor(check_for_updates.LATEST_VERSION)

if __name__ == "__main__":
    main()
