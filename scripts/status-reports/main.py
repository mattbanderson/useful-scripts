#!/usr/bin/env python3

import argparse
import csv


MONTHS = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def write_sprint_plan(date, features, task_assignments):
    month = MONTHS[int(date[4:6])]
    with open('./output/sprint-planning-{}.txt'.format(date), 'w') as outfile:
        outfile.write('h2. Date: {0} {1} {2}\n\n'.format(date[6:8], month[0:3], date[0:4]))
        outfile.write('h2. Features\n\n')
        for f in features:
            outfile.write('# {}\n'.format(f))
        outfile.write('\nh2. Task Assignments: \n\n')
        for k in task_assignments.keys():
            name = [c[0].upper() + c[1:] for c in k.split('.')]
            outfile.write('h3. {0} {1}\n'.format(name[0], name[1]))
            for value in task_assignments[k]:
                    outfile.write('# {}\n'.format(value))
            outfile.write('\n')


def write_msr(date, component_tasks):
    month = MONTHS[int(date[4:6])]
    with open('./output/msr-{}.md'.format(date), 'w') as outfile:
        outfile.write('# P&E Characterization Monthly Status Report - {0} {1}\n\n'.format(month, date[0:4]))
        for k in component_tasks.keys():
            outfile.write('## {}\n\n'.format(k))
            for value in component_tasks[k]:
                    outfile.write('* {}\n'.format(value))

# ./main.py sprint jira.csv 20180326
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_type', type=str, choices=['msr', 'sprint'],
                        help='Confluence document type')
    parser.add_argument('infile', type=str,
                        help='JIRA CSV export to format as Confluence Markdown')
    parser.add_argument('date', type=str,
                        help='Date associated with the document')
    args = parser.parse_args()
    with open(args.infile, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        features = []
        task_assignments = {}
        component_tasks = {}

        for row in reader:
            issue_type = row[header.index('Issue Type')]
            jira_number = row[header.index('Issue key')]
            summary = row[header.index('Summary')]
            assignee = row[header.index('Assignee')]
            component = row[header.index('Component/s')]
            jira_task = '{0}: {1}'.format(jira_number, summary)

            if issue_type == 'New Feature':
                features.append(jira_task)
            elif (issue_type == 'Task' or issue_type == 'Bug') and assignee != '':
                if assignee != '':
                    if assignee not in task_assignments:
                        task_assignments[assignee] = []
                    task_assignments[assignee].append(jira_task)
                if component != '':
                    if component not in component_tasks:
                        component_tasks[component] = []
                    component_tasks[component].append(jira_task)

    if args.output_type == 'msr':
        write_msr(args.date, component_tasks)
    elif args.output_type == 'sprint':
        write_sprint_plan(args.date, features, task_assignments)
