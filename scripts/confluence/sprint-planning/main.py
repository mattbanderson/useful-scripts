#!/usr/bin/env python3

import argparse
import csv


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
                        help='JIRA CSV export to format as Confluence Markdown')
    args = parser.parse_args()
    with open(args.infile, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        features = []
        task_assignments = {}

        for row in reader:
            issue_type = row[header.index('Issue Type')]
            jira_number = row[header.index('Issue key')]
            summary = row[header.index('Summary')]
            assignee = row[header.index('Assignee')]
            jira_task = '{0}: {1}'.format(jira_number, summary)

            if issue_type == 'New Feature':
                features.append(jira_task)
            elif issue_type == 'Task' and assignee != '':
                if assignee not in task_assignments:
                    task_assignments[assignee] = []
                task_assignments[assignee].append(jira_task)

        print(features)
        print(task_assignments)
