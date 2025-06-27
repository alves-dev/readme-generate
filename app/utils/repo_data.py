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
        topics.append(metadata.get('project', {}).get('language', ''))
        topics.append(metadata.get('project', {}).get('framework') or '')
        topics.append(metadata.get('project', {}).get('database') or '')

        protocols = metadata.get('project', {}).get('protocols') or []
        tools = metadata.get('project', {}).get('tools') or []
        [topics.append(e) for e in protocols]
        [topics.append(e) for e in tools]

    topics = [s for s in topics if s]

    return topics
