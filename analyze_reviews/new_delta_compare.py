from deepdiff import DeepDiff
from time import time
from datetime import datetime
import json
import os
import pandas as pd
from config import metadata_path, current_path
import re

# CHANGE DP, EMERGENCE DP, REMOVAL DP, INCREASES DP, DECREASES DP
def get_amount(amount_analyze, rev):
    amount_analyze[rev] = {}
    for dp_analyze in analyze_result[project][revision][rev]:
        amount_analyze[rev][list(dp_analyze.keys())[0]] = len(list(dp_analyze.values())[0])

def define_df_change(diff_rows, revsision_father, father, current): 
    diff = DeepDiff(father, current)
    geral_status = {}

    if 'dictionary_item_added' in diff:
        geral_status['EMERGENCE_DP'] = len(diff['dictionary_item_added'])
        #geral_status = dict_status_revision(revsision_father, geral_status)
    if 'dictionary_item_removed' in diff:
        geral_status['REMOVAL_DP'] = len(diff['dictionary_item_removed'])
        #geral_status = dict_status_revision(revsision_father, geral_status)
    if 'iterable_item_added' in diff:
        new_values = list(diff['iterable_item_added'].values())
        geral_status['INCREASES_DP'] = len(new_values)
        #geral_status = dict_status_revision(revsision_father, geral_status)
    if 'iterable_item_removed' in diff:
        new_values = list(diff['iterable_item_removed'].values())
        geral_status['DECREASES_DP'] = len(new_values)
        #geral_status = dict_status_revision(revsision_father, geral_status)
    if 'values_changed' in diff:
        new_values = list(diff['values_changed'].values())
        geral_status['CHANGE_DP'] = len(new_values)
        #geral_status = dict_status_revision(revsision_father, geral_status)

    return dict_status_revision(revsision_father, geral_status)

def get_diff_rows():
    father_commit = revision_row['before_commit_id'].iloc[0]
    current_commit = revision_row['after_commit_id'].iloc[0]
    os.system(f'cd {project_path} & git diff --name-only {father_commit} {current_commit} > {current_path}\\diff.txt')
    diff_rows = list(open('.\\analyze_reviews\\diff.txt', 'r').readlines())
    diff_rows = [re.sub('\s+', '', row) for row in diff_rows]
    diff_rows = [f'\\{project}\\{row}' for row in diff_rows]
    diff_rows = [row.replace('/', '\\') for row in diff_rows]
    return diff_rows

def dict_status_revision(revsision_father, status):
    dp = {'status': status, 'url_commit': revision_row['url'].iloc[0]}
    return {'father': revsision_father, 'design_pattern': dp}

compare_code_reviews = {}
print(f'CURRENT TIME: {datetime.now()}')
start_time = time()
# all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
all_crop_projects = ['couchbase-java-client']

crop_metadata_path = f'{metadata_path}\\{all_crop_projects[0]}'
metada_df = pd.read_csv(f'{crop_metadata_path}.csv')
project_path = 'C:\\Users\\Denis\\Downloads\\git_repos\\couchbase-java-client'

for project in all_crop_projects:
    compare_code_reviews[project] = {}
    compare_code_reviews[project]['total_revisions'] = 0
    compare_code_reviews[project]['total_revisions_with_changes'] = 0
    compare_code_reviews[project]['total_code_review_with_changes'] = 0
    count_total = 0
    count_revision = 0

    for i in range(100):
        try:
            dpd_json = open(f'.\\analyze_reviews\\results\\{i}_{project}-dpd.json', 'r').read()
        except:
            continue
        analyze_result = json.loads(dpd_json)
        
        for review_number, code_review_list in analyze_result[project].items():
            compare_code_reviews[project][review_number] = {}
            for revision in code_review_list.items():
                count_total =+ 1
                revsision_father = list(revision[1].keys())[0]
                father_dp = list(revision[1].values())[0]
                current_dp = list(revision[1].values())[1]

                if father_dp == current_dp:
                    pass
                else:
                    count_revision += 1
                    revision_row = metada_df.loc[metada_df['id'] == revision[0]]
                    diff_rows = get_diff_rows()
                    status = define_df_change(diff_rows, revsision_father, father_dp, current_dp)
                    compare_code_reviews[project][review_number][revision[0]] = status
            
            if not bool(compare_code_reviews[project][review_number]):
                del compare_code_reviews[project][review_number]

    compare_code_reviews[project]['total_revisions_with_changes'] = count_total
    compare_code_reviews[project]['total_code_review_with_changes'] = len(list(compare_code_reviews[project].keys())) - 2

    with open(f"compare_{project}.json", "w") as outfile:
        json.dump(compare_code_reviews, outfile, indent=4)

    end_time = time() - start_time
    print(f'{project} --- seconds: {end_time} --- minutes: {end_time/60}')