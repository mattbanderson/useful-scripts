#!/usr/bin/env python3

import argparse
import csv
import datetime


# ./main.py jira-features.csv jira-tasks.csv
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile_features', type=str,
                        help='JIRA CSV export containing list of features')
    parser.add_argument('infile_tasks', type=str,
                        help='JIRA CSV export containing list of tasks to associate with features')
    parser.add_argument('infile_bugs', type=str,
                        help='JIRA CSV export containing list of bugs')
    parser.add_argument('outfile_prefix', type=str,
                        help='Prefix to add to output file name')
    args = parser.parse_args()
    features = {}
    bugs = []

    with open(args.infile_features, newline='') as feature_file:
        with open(args.infile_tasks, newline='') as task_file:
            feature_reader = csv.reader(feature_file)
            header = next(feature_reader)

            for row in feature_reader:
                jira_number = row[header.index('Issue key')]
                summary = row[header.index('Summary')]
                created = row[header.index('Created')]
                labels = row[header.index('Labels')]
                time_estimate = row[header.index('Original Estimate')]
                time_estimate_hours = 0
                # convert seconds to hours
                if (time_estimate != ''):
                    time_estimate_hours = int(time_estimate) / 3600
                jira_task = '{0}: {1}'.format(jira_number, summary)

                features[jira_number] = {
                        'estimate': time_estimate_hours,
                        'tasks': 0,
                        'created': created
                        }

            task_reader = csv.reader(task_file)
            header = next(task_reader)
            for row in task_reader:
                parent_feature = row[header.index('Outward issue link (Child-Parent)')]
                time_estimate = row[header.index('Original Estimate')]
                time_estimate_hours = 0
                # convert seconds to hours
                if time_estimate != '':
                    time_estimate_hours = int(time_estimate) / 3600
                if parent_feature in features.keys():
                    features[parent_feature]['estimate'] += time_estimate_hours
                    features[parent_feature]['tasks'] += 1

    with open(args.infile_bugs, newline='') as bug_file:
        bug_reader = csv.reader(bug_file)
        header = next(bug_reader)

        for row in bug_reader:
            created = row[header.index('Created')]
            resolved = row[header.index('Resolved')]
            bugs.append({'created': created, 'resolved': resolved})

    with open('./output/{0}tasks-added.csv'.format(args.outfile_prefix), 'w') as outfile:
        outfile.write('"issuekey","estimate","tasks","created"\n')
        for k in sorted(list(features.keys())):
            outfile.write('"{0}", {1}, {2}, "{3}"\n'.format(
                    k, features[k]['estimate'], features[k]['tasks'], features[k]['created']))

    with open('./output/{0}scope-change.csv'.format(args.outfile_prefix), 'w') as outfile:
        outfile.write('"sprint","tasks","hours"\n')
        sprint_start = datetime.datetime(2018, 3, 12)
        sprint_number = 1
        while sprint_start < datetime.datetime.now():
            sprint_end = sprint_start + datetime.timedelta(14)
            tasks = 0
            hours = 0
            for k in features.keys():
                created_date = datetime.datetime.strptime(features[k]['created'], '%b %d, %Y %I:%M %p')
                if created_date >= sprint_start and created_date < sprint_end:
                    tasks += features[k]['tasks']
                    hours += features[k]['estimate']
            outfile.write('"S{0}",{1},{2}\n'.format(sprint_number, tasks, hours))
            sprint_start = sprint_end
            sprint_number += 1

    with open('./output/{0}bugs.csv'.format(args.outfile_prefix), 'w') as outfile:
        outfile.write('"sprint","opened","closed"\n')
        sprint_start = datetime.datetime(2018, 3, 12)
        sprint_number = 0
        while sprint_start < datetime.datetime.now():
            sprint_end = sprint_start + datetime.timedelta(14)
            opened = 0
            closed = 0
            for bug in bugs:
                created_date = datetime.datetime.strptime(bug['created'], '%b %d, %Y %I:%M %p')
                if created_date >= sprint_start and created_date < sprint_end:
                    opened += 1
                if bug['resolved'] != '':
                    resolved_date = datetime.datetime.strptime(bug['resolved'], '%b %d, %Y %I:%M %p')
                    if resolved_date >= sprint_start and resolved_date < sprint_end:
                        closed += 1
            outfile.write('"S{0}",{1},{2}\n'.format(sprint_number, opened, closed))
            sprint_start = sprint_end
            sprint_number += 1
