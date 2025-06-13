from pathlib import Path

import requests
import yaml

from app.github.client import GitRepository

GITHUB_API = 'https://api.github.com'


def update_license(repo: GitRepository) -> bool:
    data = _load_metadata(repo.repo_path)
    license_key = data['project']['license']
    key = _get_standard_license(license_key)

    if license is None:
        return False

    repo.write_file('LICENSE', key)

    return True


def _get_standard_license(license_key: str) -> str | None:
    """
    Busca o texto padrão de uma licença (ex: 'mit', 'gpl-3.0') usando a API do GitHub.

    :param license_key: ID da licença (ex: 'mit', 'gpl-3.0', 'apache-2.0')
    :return: Texto da licença ou None se não encontrar
    """

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


def _load_metadata(path: Path) -> dict:
    metadata_path = path.joinpath('.docs', "data.yml")
    with open(metadata_path, "r") as f:
        return yaml.safe_load(f)
