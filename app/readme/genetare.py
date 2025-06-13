from datetime import datetime
from pathlib import Path
from string import Template

import yaml

BASE_PATH_TEMPLATES = str(Path(__file__).parent.parent.parent.resolve()) + '/templates'
FOLDER_DOCS = '.docs'


def check_files(path: Path) -> bool:
    """
    Verifica se a pasta informada contém:
    - Um diretório '.docs'
    - Um arquivo 'data.yml' dentro de '.docs'

    :param path: Caminho da pasta base
    :return: True se ambos existirem, False caso contrário
    """
    docs_dir = path / FOLDER_DOCS
    data_file = docs_dir / "data.yml"

    return docs_dir.is_dir() and data_file.is_file()


def full_readme(path: Path) -> str:
    """
    Gera e retorna o README completo
    :param path:
    :return:
    """
    head = _generate_head(path)
    extra = _load_extra_md(path)
    footer = _generate_footer(path)

    return f'{head}\n{extra}\n{footer}'


def _generate_head(path: Path) -> str:
    data = _load_metadata(path)

    head_data: dict = data["head"]
    head_version: str = head_data["version"]
    head_template: str = f"{BASE_PATH_TEMPLATES}/head-{head_version}.md"

    tags_badges = '\n'.join(
        f'<img src="https://img.shields.io/badge/{_format_tag(tag)}-lightgrey">' for tag in head_data['topics']
    )

    tags_badges = '<img src="https://img.shields.io/badge/topics:-grey"> \n' + tags_badges
    head_data['topics_tags_badges'] = tags_badges

    return _render_template(head_template, head_data)


def _generate_footer(path: Path) -> str:
    data = _load_metadata(path)

    footer_data: dict = data["footer"]
    footer_version: str = footer_data["version"]
    footer_template: str = f"{BASE_PATH_TEMPLATES}/footer-{footer_version}.md"

    footer_data['license'] = _format_tag(footer_data['license'])
    footer_data['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    return _render_template(footer_template, footer_data)


def _load_metadata(path: Path) -> dict:
    metadata_path = path.joinpath(FOLDER_DOCS, "data.yml")
    with open(metadata_path, "r") as f:
        return yaml.safe_load(f)


def _format_tag(tag: str) -> str:
    return tag.replace('-', '%20').replace(' ', '%20')


def _render_template(template_path, context) -> str:
    with open(template_path, "r") as f:
        content = f.read()
    return Template(content).safe_substitute(context)


def _load_extra_md(path: Path) -> str:
    extra = path.joinpath(FOLDER_DOCS, "extra.md")
    try:
        with open(extra, "r") as f:
            content = f.read()
        return content
    except:
        return ''
