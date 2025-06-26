from datetime import datetime
from pathlib import Path
from string import Template

from app.utils import folder_files as files
from app.utils import repo_data

BASE_PATH_TEMPLATES = str(Path(__file__).parent.parent.parent.resolve()) + '/templates'


def full_readme(path: Path) -> str:
    """
    Gera e retorna o README completo
    :param path:
    :return:
    """
    head = _generate_head(path)
    extra = files.load_extra_md(path)
    footer = _generate_footer(path)

    return f'{head}\n{extra}\n{footer}'


def _generate_head(path: Path) -> str:
    metadata = files.load_repository_metadata(path)

    head_version: str = 'v1'
    template_name = 'default'

    head_data: dict = _head_data(metadata)
    repo_type = repo_data.get_type(metadata)

    if 'code' == repo_type:
        template_name = 'code'

    head_template: str = f"{BASE_PATH_TEMPLATES}/head-{template_name}-{head_version}.md"

    if head_data['topics'] is not None:
        tags_badges = '\n'.join(
            f'<img src="https://img.shields.io/badge/{_format_tag(tag)}-lightgrey">' for tag in head_data['topics']
        )

        tags_badges = '<img src="https://img.shields.io/badge/topics:-grey"> \n' + tags_badges
        head_data['topics_tags_badges'] = tags_badges
    else:
        head_data['topics_tags_badges'] = ''

    return _render_template(head_template, head_data)


def _generate_footer(path: Path) -> str:
    metadata = files.load_repository_metadata(path)

    template_version: str = 'v1'
    template_name = 'default'

    footer_data: dict = _footer_data(metadata)
    footer_template: str = f"{BASE_PATH_TEMPLATES}/footer-{template_name}-{template_version}.md"

    footer_data['license'] = _format_tag(footer_data['license'])
    footer_data['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    return _render_template(footer_template, footer_data)


def _format_tag(tag: str) -> str:
    return tag.replace('-', '%20').replace(' ', '%20')


def _render_template(template_path, context) -> str:
    with open(template_path, "r") as f:
        content = f.read()
    return Template(content).safe_substitute(context)


def _head_data(metadata: dict) -> dict:
    data = {
        'title': metadata.get('repository', {}).get('title', '...'),
        'description': repo_data.get_description(metadata),
        'topics': repo_data.get_topics(metadata)
    }

    if 'code' == repo_data.get_type(metadata):
        data['status'] = metadata.get('project', {}).get('status', '...')

    return data


def _footer_data(metadata: dict) -> dict:
    data = {
        'license': repo_data.get_license(metadata)
    }

    return data
