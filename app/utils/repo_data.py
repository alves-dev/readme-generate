def get_type(metadata: dict) -> str:
    return metadata.get('repository', {}).get('type', '...')


def get_description(metadata: dict) -> str:
    return metadata.get('repository', {}).get('description', '...')


def get_license(metadata: dict) -> str:
    return metadata.get('repository', {}).get('license', '...')


def get_topics(metadata: dict) -> list:
    topics = metadata.get('repository', {}).get('topics') or []

    repo_type = get_type(metadata)
    if 'code' == repo_type:
        topics.append(metadata.get('project', {}).get('stack', {}).get('language', ''))
        topics.append(metadata.get('project', {}).get('stack', {}).get('framework') or '')
        topics.append(metadata.get('project', {}).get('stack', {}).get('database') or '')

        protocols = metadata.get('project', {}).get('stack', {}).get('protocols') or []
        tools = metadata.get('project', {}).get('stack', {}).get('tools') or []
        [topics.append(e) for e in protocols]
        [topics.append(e) for e in tools]

    topics = [s for s in topics if s]

    return list(dict.fromkeys(topics))  # Remove duplicados preservando ordem


def get_project_language(metadata: dict) -> str | None:
    repo_type = get_type(metadata)
    if 'code' == repo_type:
        return metadata.get('project', {}).get('stack', {}).get('language', None)

    return None


def get_project_framework(metadata: dict) -> str | None:
    repo_type = get_type(metadata)
    if 'code' == repo_type:
        return metadata.get('project', {}).get('stack', {}).get('framework') or None

    return None


def get_project_database(metadata: dict) -> str | None:
    repo_type = get_type(metadata)
    if 'code' == repo_type:
        return metadata.get('project', {}).get('stack', {}).get('database') or None

    return None


def get_project_protocols(metadata: dict) -> list:
    repo_type = get_type(metadata)
    if 'code' == repo_type:
        return metadata.get('project', {}).get('stack', {}).get('protocols') or []

    return []


def get_project_tools(metadata: dict) -> list:
    repo_type = get_type(metadata)
    if 'code' == repo_type:
        return metadata.get('project', {}).get('stack', {}).get('tools') or []

    return []
