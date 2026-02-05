from datetime import datetime
from pathlib import Path
from string import Template

from app.utils import folder_files as files
from app.utils import repo_data

BASE_PATH_TEMPLATES = str(Path(__file__).parent.parent.parent.resolve()) + '/templates'


def full_readme(path: Path) -> str:
    """
    Gera e retorna o README completo a partir do README.base.md e dos templates.
    """

    base = files.load_base_md(path)

    header = _generate_head(path)
    footer = _generate_footer(path)

    base = base.replace('<!-- TEMPLATE:header -->', header)
    base = base.replace('<!-- TEMPLATE:footer -->', footer)

    return base


def _generate_head(path: Path) -> str:
    metadata = files.load_repository_metadata(path)

    head_version: str = 'v1'
    template_name = 'default'

    head_data: dict = _head_data(metadata)
    repo_type = repo_data.get_type(metadata)

    if 'code' == repo_type:
        template_name = 'code'

    head_template: str = f"{BASE_PATH_TEMPLATES}/header-{template_name}-{head_version}.md"

    head_data['topics_tags_badges'] = _build_topics_badges(head_data['topics'])

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
    status_description = {
        'development': {
            'emoji': '🛠️',
            'text': 'Actively worked on. New features may come and things can change.',
            'color': '10B981'
        },
        'maintenance': {
            'emoji': '🔧',
            'text': 'No new features planned. Bugs and small fixes only.',
            'color': '38BDF8'
        },
        'deprecated': {
            'emoji': '⚠️',
            'text': 'Still works, but no longer developed and may be removed in the future.',
            'color': 'F59E0B'
        },
        'archived': {
            'emoji': '🪦',
            'text': 'Abandoned project. Not maintained and kept only for reference.',
            'color': '64748B'
        }
    }

    data = {
        'title': metadata.get('repository', {}).get('title', '...'),
        'description': repo_data.get_description(metadata),
        'topics': repo_data.get_topics(metadata)
    }

    if 'code' == repo_data.get_type(metadata):
        data['status'] = metadata.get('project', {}).get('status', '...')

        status_info = status_description.get(data['status'], {
            'emoji': '❔',
            'text': 'Unknown status.',
            'color': '94A3B8'
        })

        data['status_description'] = f"{status_info['emoji']} {status_info['text']}"
        data['status_color'] = status_info['color']

    return data


def _footer_data(metadata: dict) -> dict:
    data = {
        'license': repo_data.get_license(metadata)
    }

    return data


def _build_topics_badges(topics: list[str]) -> str:
    if not topics:
        return ""

    badges = " ".join(
        f'<img src="https://img.shields.io/badge/{_format_tag(tag)}-1E293B?style=flat-square&logoColor=white"/>'
        for tag in topics
    )

    header = (
        '<img src="https://img.shields.io/badge/topics-10B981?style=flat-square&logoColor=white"/>'
    )

    return f'{header} {badges}'
