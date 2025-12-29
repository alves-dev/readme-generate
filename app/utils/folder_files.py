import logging
from pathlib import Path

import yaml

FOLDER_DOCS = '.docs'
FILE_YML = '.repo.yml'
BASE_MD = 'README.base.md'
_repository_cache = {}  # cache simples em memória


def check_files(path: Path):
    """
    Verifica se a pasta informada contém:
    - Um diretório '.docs'
    - Um arquivo 'FILE_YML' na raiz do repositorio

    Encerra o script caso não ache.

    :param path: Caminho da pasta base
    """
    docs_dir = path / FOLDER_DOCS
    data_file = path / FILE_YML
    readme_base = docs_dir / BASE_MD

    if not docs_dir.is_dir():
        logging.error('Repository does not have .docs directory')
        exit()

    if not data_file.is_file():
        logging.error(f'Repository does not have {FILE_YML} file')
        exit()

    if not readme_base.is_file():
        logging.error(f'Repository does not have {BASE_MD} file')
        exit()

    logging.info("All files or folders found")


def load_repository_metadata(path: Path) -> dict:
    cache_key = str(path.resolve())
    if cache_key in _repository_cache:
        return _repository_cache[cache_key]

    metadata_path = path.joinpath(FILE_YML)
    with open(metadata_path, "r") as f:
        data = yaml.safe_load(f)

    _repository_cache[cache_key] = data
    return data


def load_base_md(path: Path) -> str:
    extra = path.joinpath(FOLDER_DOCS, BASE_MD)
    try:
        with open(extra, "r") as f:
            content = f.read()
        return content
    except OSError:
        return ''
