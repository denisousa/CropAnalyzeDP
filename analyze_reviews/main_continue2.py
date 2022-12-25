from dpd import detect_design_pattern
from patterns_name import patterns
from config import repos_path, metadata_path, current_path
from time import time
from datetime import datetime
from itertools import islice
import re
import pandas as pd
import json
import gc
import os

print(f'CURRENT TIME: {datetime.now()}')
start_time = time()
# all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
all_crop_projects = ['jgit'] 

def add_review(detected_dp, project, review_number, revision, relationship, dp_regex):
    dp_project = detect_design_pattern(project, dp_regex)
    if len(dp_project[dp_regex]) != 0:
        detected_dp[project][review_number][revision][relationship].append(dp_project)

def partition(lst, n):
    division = len(lst) / float(n)
    return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

detected_dp = {}
continue_partition = 18 # last file is 29_****
for project in all_crop_projects:
    crop_repos_path = f'{repos_path}\\{project}'
    crop_metadata_path = f'{metadata_path}\\{project}'
    metada_df = pd.read_csv(f'{crop_metadata_path}.csv', index_col=0)
    print(f'COMPLETE - shape: {metada_df.shape}')
    metada_df = metada_df.loc[metada_df['status'] == 'MERGED']
    print(f'MERGED - shape: {metada_df.shape}')
    
    review_number_list = list(metada_df['review_number'].unique())
    review_number_partition_list = partition(review_number_list, 100)
    
    detected_dp = {project: {}}
    for i, review_number_partition in enumerate(review_number_partition_list[continue_partition:]):
        i += continue_partition
        for review_number in review_number_partition:
            code_review_rows = metada_df.loc[metada_df['review_number'] == review_number]
            review_number = str(review_number)
            detected_dp[project][review_number] = {}
            for revision, row in code_review_rows.iterrows():
                father_commit = row['before_commit_id']
                current_commit = row['after_commit_id']
                detected_dp[project][review_number][revision] = {}

                commit_name_path = f'{current_path}\\commit-name.txt'
                os.system(f'cd {crop_repos_path} & git checkout --force {father_commit} & git log -1 --pretty=%B > {current_path}\\commit-name.txt')
                father_revision = re.sub('\s+', '', open(commit_name_path, 'r').read().split(' ')[-1])
                detected_dp[project][review_number][revision][father_revision] = []
                [add_review(detected_dp, project, review_number, revision, father_revision, dp_regex) for dp_regex in patterns]

                os.system(f'cd {crop_repos_path} & git checkout --force {current_commit}')
                current_revision = f'current_{revision}'
                detected_dp[project][review_number][revision][current_revision] = []
                [add_review(detected_dp, project, review_number, revision, current_revision, dp_regex) for dp_regex in patterns]

        with open(f"{i}_{project}-dpd.json", "w") as outfile:
            json.dump(detected_dp, outfile, indent=4)
            print(f"GENERATE: {i}_{project}-dpd.json")

            del detected_dp
            gc.collect()
            detected_dp = {project: {}}


end_time = time() - start_time
print(f'{project} --- seconds: {end_time} --- minutes: {end_time/60}')