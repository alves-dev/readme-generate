from pathlib import Path

import yaml

FOLDER_DOCS = '.docs'
FILE_YML = 'repository.yml'
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

    if not docs_dir.is_dir():
        print("Repository doesn't have .docs")
        exit()

    if not data_file.is_file():
        print(f"Repository doesn't have {FILE_YML}")
        exit()

    print("All files or folders found")


def load_repository_metadata(path: Path) -> dict:
    cache_key = str(path.resolve())
    if cache_key in _repository_cache:
        return _repository_cache[cache_key]

    metadata_path = path.joinpath(FILE_YML)
    with open(metadata_path, "r") as f:
        data = yaml.safe_load(f)

    _repository_cache[cache_key] = data
    return data


def load_extra_md(path: Path) -> str:
    extra = path.joinpath(FOLDER_DOCS, "extra.md")
    try:
        with open(extra, "r") as f:
            content = f.read()
        return content
    except OSError:
        return ''
