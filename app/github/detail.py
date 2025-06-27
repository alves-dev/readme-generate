import requests

from app.config.setting import setting
from app.github.client import GitRepository
from app.utils import folder_files as files
from app.utils import repo_data

GITHUB_API = 'https://api.github.com'


def update_repo_metadata(repo: GitRepository) -> bool:
    data = files.load_repository_metadata(repo.repo_path)

    description = repo_data.get_description(data)
    website = data.get('repository', {}).get('website', '')

    topics_ok = _update_topics(repo.repo_full_name, repo_data.get_topics(data))
    metadata_ok = _update_detail_metadata(repo.repo_full_name, description, website)

    return topics_ok and metadata_ok


def _update_topics(repo: str, topics: list[str]) -> bool:
    """
    Atualiza os tópicos de um repositório no GitHub.

    :param repo: Ex: 'alves-dev/posts'
    :param token: Personal Access Token com permissão pra editar o repo
    :param topics: Lista de tópicos (ex: ["java", "spring-boot", "posts"])
    :return: True se atualizar com sucesso, False se der erro
    """
    url = f"{GITHUB_API}/repos/{repo}/topics"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"Bearer {setting.GITHUB_TOKEN}"
    }
    data = {"names": topics}

    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200


def _update_detail_metadata(repo: str, description: str = "", homepage: str = "") -> bool:
    """
    Atualiza a descrição e homepage de um repositório no GitHub.

    :param repo: Ex: 'alves-dev/infra'
    :param token: Personal Access Token com permissões de repo
    :param description: Nova descrição
    :param homepage: Nova URL de homepage (ou string vazia)
    :return: True se sucesso, False se erro
    """
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {setting.GITHUB_TOKEN}"
    }
    data = {
        "description": description,
        "homepage": homepage
    }

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200
