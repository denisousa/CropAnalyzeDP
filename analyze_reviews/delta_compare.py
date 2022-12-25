from deepdiff import DeepDiff
from time import time
from datetime import datetime
import json
import os
import pandas as pd
from config import metadata_path, current_path
import re
import itertools

# CHANGE DP, EMERGENCE DP, REMOVAL DP, INCREASES DP, DECREASES DP
def get_amount(amount_analyze, rev):
    amount_analyze[rev] = {}
    for dp_analyze in analyze_result[project][revision][rev]:
        amount_analyze[rev][list(dp_analyze.keys())[0]] = len(list(dp_analyze.values())[0])

def define_df_change(revsision_father, father, current): 
    diff = DeepDiff(father, current)
    geral_status = {}

    if 'dictionary_item_added' in diff:
        geral_status['EMERGENCE_DP'] = len(diff['dictionary_item_added'])
    elif 'dictionary_item_removed' in diff:
        geral_status['REMOVAL_DP'] = len(diff['dictionary_item_removed'])
    elif 'iterable_item_added' in diff:
        new_values = list(diff['iterable_item_added'].values())
        geral_status['INCREASES_DP'] = len(new_values)
    elif 'iterable_item_removed' in diff:
        new_values = list(diff['iterable_item_removed'].values())
        new_values = [list(value.values())[0] for value in new_values]
        geral_status['DECREASES_DP'] = len(list(itertools.chain(*new_values)))
    elif 'values_changed' in diff:
        new_values = list(diff['values_changed'].values())
        geral_status['CHANGE_DP'] = len(new_values)
    else:
        print('NEW PROBLEM')

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
    dp = {'partition_file': i, 'status': status, 'url_commit': revision_row['url'].iloc[0]}
    return {'father': revsision_father, 'design_pattern': dp}

compare_code_reviews = {}
print(f'CURRENT TIME: {datetime.now()}')
start_time = time()
# all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
all_crop_projects = ['couchbase-java-client', 'jgit', 'couchbase-jvm-core', 'org.eclipse.linuxtools']

for project in all_crop_projects:
    crop_metadata_path = f'{metadata_path}\\{project}'
    metada_df = pd.read_csv(f'{crop_metadata_path}.csv')
    project_path = f'C:\\Users\\Denis\\Downloads\\git_repos\\{project}'
    metada_merged_df = metada_df.loc[metada_df['status'] == 'MERGED']
    REVIEWS_MERGED_METADATA = metada_merged_df.shape[0]
    CODE_REVIEWS_MERGED_METADATA = len(metada_merged_df['review_number'].unique())
    print(f'TOTAL REVIEWS MERGED METADATA: {REVIEWS_MERGED_METADATA}')
    print(f'TOTAL CODE REVIEWS MERGED METADATA: {CODE_REVIEWS_MERGED_METADATA}')
    compare_code_reviews[project] = {}
    compare_code_reviews[project]['total_revisions'] = 0
    compare_code_reviews[project]['total_code_reviews'] = 0
    compare_code_reviews[project]['total_revisions_DP'] = 0
    compare_code_reviews[project]['total_code_review_DP'] = 0
    total_revisions = 0
    total_code_reviews = 0
    total_revisions_DP = 0
    total_code_review_DP = 0

    for i in range(100):
        try:
            dpd_json = open(f'.\\analyze_reviews\\{project}\\{i}_{project}-dpd.json', 'r').read()
        except:
            print('PROBLEM')
            continue
        analyze_result = json.loads(dpd_json)
        
        for review_number, code_review_list in analyze_result[project].items():
            total_code_reviews += 1
            compare_code_reviews[project][review_number] = {}
            for revision in code_review_list.items():
                total_revisions += 1
                revsision_father = list(revision[1].keys())[0]
                father_dp = list(revision[1].values())[0]
                current_dp = list(revision[1].values())[1]

                if father_dp != current_dp:
                    total_revisions_DP += 1
                    revision_row = metada_df.loc[metada_df['id'] == revision[0]]
                    # diff_rows = get_diff_rows()
                    status = define_df_change(revsision_father, father_dp, current_dp)
                    compare_code_reviews[project][review_number][revision[0]] = status
            
            if not bool(compare_code_reviews[project][review_number]):
                del compare_code_reviews[project][review_number]

    compare_code_reviews[project]['total_revisions'] = total_revisions
    compare_code_reviews[project]['total_code_reviews'] = total_code_reviews
    compare_code_reviews[project]['total_revisions_DP'] = total_revisions_DP
    compare_code_reviews[project]['total_code_review_DP'] = len(list(compare_code_reviews[project].keys())) - 4

    with open(f"compare_{project}.json", "w") as outfile:
        json.dump(compare_code_reviews, outfile, indent=4)

    end_time = time() - start_time
    print(f'{project} --- seconds: {end_time} --- minutes: {end_time/60}')