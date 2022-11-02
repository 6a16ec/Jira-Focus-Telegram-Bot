import copy
import os
from datetime import datetime

from dotenv import load_dotenv
from jira import JIRA

load_dotenv()


class Issue:
    def __init__(self, raw_issue):
        self.__key = raw_issue['key']
        self.__summary = raw_issue['fields']['summary']
        self.__description = raw_issue['fields']['description']
        self.__priority = raw_issue['fields']['priority']['id']
        self.__status_name = raw_issue['fields']['status']['name']
        self.__url = raw_issue['self']
        str_due_date = raw_issue['fields']['duedate']
        self.__due_date = datetime.strptime(str_due_date, '%Y-%m-%d') if str_due_date else None

    def get_key(self):
        return self.__key

    def get_summary(self):
        return self.__summary

    def get_description(self):
        return self.__description

    def get_priority(self):
        return self.__priority

    def get_status_name(self):
        return self.__status_name

    def get_url(self):
        return self.__url

    def get_due_date(self):
        return self.__due_date


class Jira:
    def __init__(self):
        jira_options = {'server': os.getenv('JIRA_SERVER')}
        jira_basic_auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_TOKEN'))
        self.__jira = JIRA(options=jira_options, basic_auth=jira_basic_auth)
        self.__project = self.__jira.project(os.getenv('JIRA_PROJECT_KEY'))
        self.__raw_issues = self.__parse_raw_issues()

    def __parse_raw_issues(self):
        all_issues = []
        i = 0
        chunk_size = 100
        while True:
            chunk = self.__jira.search_issues(f'project = {self.__project.key}', startAt=i, maxResults=chunk_size)
            i += chunk_size
            all_issues += chunk.iterable
            if i >= chunk.total:
                break
        return all_issues

    def get_raw_issues(self):
        return copy.deepcopy(self.__raw_issues)

    def get_issues(self):
        return [
            Issue(raw_issue.raw) for raw_issue in self.__raw_issues
        ]
