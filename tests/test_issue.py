import unittest

import helper


class TestIssue(unittest.TestCase):
    def test_01(self):
        my_jira = helper.Jira()
        raw_issue = my_jira.get_raw_issues()[0]
        print(raw_issue.raw.keys())
        print(raw_issue.raw['self'])
        print(raw_issue.raw['key'])
        print(raw_issue.raw['fields']['duedate'])
        print(raw_issue.raw['fields'].keys())
        print(dir(raw_issue.raw))



if __name__ == '__main__':
    unittest.main()
