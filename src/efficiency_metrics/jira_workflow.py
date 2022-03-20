import json
from base64 import b64encode
from collections import defaultdict
from datetime import datetime

import requests


class JiraWorkflow:
    issue_types = {'10000': 'Epic', '10004': 'Task',
                   '10005': 'Story', '10006': 'Epic', '10007': 'Subtask'}

    def __init__(self, nickname: str, email: str, token: str, project: str):
        self.url = f"https://{nickname}.atlassian.net/rest/api/2/search?jql=project={project}"
        auth_header = b64encode(
            f'{email}:{token}'.encode('ascii')).decode('ascii')
        self.headers = {'Authorization': f'Basic {auth_header}',
                        'Accept': 'application/json'}
        self.issues = None

    def get_data(self) -> None:
        """
        Get current state of project board.
        """

        resp = requests.get(self.url, headers=self.headers)
        self.issues = json.loads(resp.content.decode('utf-8'))

    def empty(self) -> bool:
        """
        Check if data retrieval was unsuccessful.
        """

        return len(self.issues) < 5

    def type_count(self) -> dict:
        """
        Count types of all issues.
        """

        if self.issues is None:
            raise ValueError("No board data! Run get_data()")
        issue_type_count = defaultdict(int)
        for issue in self.issues['issues']:
            issue_type_id = issue['fields']['issuetype']['id']
            issue_type = self.issue_types[issue_type_id]
            issue_type_count[issue_type] += 1
        return dict(issue_type_count)

    def status_count(self) -> dict:
        """
        Count statuses of all issues.
        """

        if self.issues is None:
            raise ValueError("No board data! Run get_data()")
        issue_status_count = defaultdict(int)
        for issue in self.issues['issues']:
            issue_status = issue['fields']['status']['name']
            issue_status_count[issue_status] += 1
        return dict(issue_status_count)

    def delay_minutes(self) -> int:
        """
        Calculate total delay on finished tasks (in minutes).
        """

        if self.issues is None:
            raise ValueError("No board data! Run get_data()")
        total_delay_minutes = 0
        for issue in self.issues['issues']:

            issue_type_id = issue['fields']['issuetype']['id']
            issue_type = self.issue_types[issue_type_id]
            if issue['fields']['status']['name'] != 'Done' or issue_type != 'Task':
                continue

            time_estimate = None
            if issue['fields']['timeestimate'] is not None:
                if issue['fields']['timeoriginalestimate'] is not None:
                    time_estimate = max(
                        issue['fields']['timeestimate'], issue['fields']['timeoriginalestimate'])
                else:
                    time_estimate = issue['fields']['timeestimate']
            elif issue['fields']['timeoriginalestimate'] is not None:
                time_estimate = issue['fields']['timeoriginalestimate']

            if time_estimate is not None and issue['fields']['timespent'] is not None:
                total_delay_minutes += (issue['fields']
                                        ['timespent'] - time_estimate) // 60
                continue

            if issue['fields']['duedate'] is not None:
                duedate = datetime.strptime(
                    issue['fields']['duedate'], '%Y-%m-%d')
                resolutiondate = datetime.strptime(
                    issue['fields']['resolutiondate'][:-9], '%Y-%m-%dT%H:%M:%S')
                diff = resolutiondate - duedate
                total_delay_minutes += diff.days * 1440 + diff.seconds // 60

        return total_delay_minutes

    def spent_minutes(self) -> int:
        """
        Calculate time spent by now on all tasks (in minutes).
        """

        if self.issues is None:
            raise ValueError("No board data! Run get_data()")
        total_spent_minutes = 0
        for issue in self.issues['issues']:

            issue_type_id = issue['fields']['issuetype']['id']
            if self.issue_types[issue_type_id] != 'Task':
                continue

            if issue['fields']['timespent'] is not None:
                total_spent_minutes += issue['fields']['timespent'] // 60
                continue

            created = datetime.strptime(
                issue['fields']['created'][:-9], '%Y-%m-%dT%H:%M:%S')
            if issue['fields']['resolutiondate'] is not None:
                resolutiondate = datetime.strptime(
                    issue['fields']['resolutiondate'][:-9], '%Y-%m-%dT%H:%M:%S')
                curr_timedelta = resolutiondate - created
            else:
                curr_timedelta = datetime.now() - created

            curr_minutes = curr_timedelta.days * 1440 + curr_timedelta.seconds // 60
            total_spent_minutes += int(curr_minutes / 7 * 5 / 3)

        return total_spent_minutes
