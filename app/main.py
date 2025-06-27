import argparse

from app.github import detail
from app.github import license
from app.github.client import GitRepository
from app.readme import genetare
from app.utils import folder_files


def main():
    parser = argparse.ArgumentParser(description="Script que recebe argumento do repositório")
    parser.add_argument("repository", help="Caminho local ou URL do repositório")
    args = parser.parse_args()

    print(f"Repositório recebido: {args.repository}")

    repo = GitRepository(args.repository)
    folder_files.check_files(repo.repo_path)

    new_readme = genetare.full_readme(repo.repo_path)
    repo.write_file('README.md', new_readme)

    result = detail.update_repo_metadata(repo)
    print(f'Repository updated: {result}')

    license_ok = license.update_license(repo)
    print(f'LICENSE updated: {license_ok}')

    commit = repo.commit_and_push('New readme generated [skip actions]')
    print(f'README.md updated: {commit}')


if __name__ == "__main__":
    main()
