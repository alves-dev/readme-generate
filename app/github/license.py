import requests

from app.github.client import GitRepository
from app.utils import folder_files as files
from app.utils import repo_data

GITHUB_API = 'https://api.github.com'


def update_license(repo: GitRepository) -> bool:
    data = files.load_repository_metadata(repo.repo_path)
    license_key = repo_data.get_license(data)
    license_text = _get_standard_license(license_key)

    if license_text is None:
        return False

    repo.write_file('LICENSE', license_text)

    return True


def _get_standard_license(license_key: str) -> str | None:
    """
    Busca o texto padrão de uma licença (ex: 'mit', 'gpl-3.0') usando a API do GitHub.

    :param license_key: ID da licença (ex: 'mit', 'gpl-3.0', 'apache-2.0')
    :return: Texto da licença ou None se não encontrar
    """

    if license_key == 'NO-LICENSE':
        return None

    my_keys = {
        'MIT': 'mit',
        'GPL-3': 'gpl-3.0'
    }

    license_key = my_keys[license_key]

    url = f"{GITHUB_API}/licenses/{license_key}"
    headers = {"Accept": "application/vnd.github+json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("body")

    return None
