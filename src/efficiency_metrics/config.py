import json
from typing import Optional

from efficiency_metrics.jira_workflow import JiraWorkflow

CONFIG = "config.json"


def write_parser(nickname, email, token, project):
    with open(CONFIG) as f:
        config = json.load(f)
    config['nickname'] = nickname
    config['email'] = email
    config['token'] = token
    config['project'] = project
    with open(CONFIG, 'w') as f:
        json.dump(config, f)


def write_cocomo(cocomo):
    with open(CONFIG) as f:
        config = json.load(f)
    config['cocomo'] = cocomo
    with open(CONFIG, 'w') as f:
        json.dump(config, f)


def get_parser() -> Optional[JiraWorkflow]:
    with open(CONFIG) as f:
        config = json.load(f)
    if config['nickname'] is None:
        return None
    jira_parser = JiraWorkflow(config['nickname'],
                               config['email'],
                               config['token'],
                               config['project'])
    jira_parser.get_data()
    return None if jira_parser.empty() else jira_parser


def get_cocomo():
    with open(CONFIG) as f:
        config = json.load(f)
        return config['cocomo']
