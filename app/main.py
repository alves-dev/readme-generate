import argparse
import logging

from app.config.setting import setting
from app.github import license
from app.github.client import GitRepository
from app.readme import genetare
from app.utils import folder_files


def process_repository(repository_path):
    """Processa um único repositório"""
    try:
        logging.info(f'Processando repositório: {repository_path}')

        repo: GitRepository = GitRepository(repository_path)
        folder_files.check_files(repo.repo_path)

        new_readme = genetare.full_readme(repo.repo_path)
        repo.write_file('README.md', new_readme)

        license_ok = license.update_license(repo)
        logging.info(f'LICENSE updated: {license_ok}')

        if setting.COMMIT_PUSH:
            commit = repo.commit_and_push('New readme generated [skip actions]')
            logging.info(f'README.md updated: {commit}')

        return True
    except Exception as e:
        logging.error(f'Erro ao processar repositório {repository_path}: {str(e)}')
        return False


def main():
    parser = argparse.ArgumentParser(description="Script que processa um ou mais repositórios")
    parser.add_argument("repositories", nargs='+', help="URL(s) do(s) repositório(s) contendo o nome do usuário")
    args = parser.parse_args()

    total = len(args.repositories)
    successful = 0
    failed = 0

    logging.info(f'Total de repositórios a processar: {total}')

    for repository in args.repositories:
        if process_repository(repository):
            successful += 1
        else:
            failed += 1

    logging.info(f'Processamento concluído: {successful} sucesso(s), {failed} falha(s) de {total} total')


if __name__ == "__main__":
    main()
