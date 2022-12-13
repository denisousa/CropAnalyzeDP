from crop_query import get_hash_by_commit_name
from dpd import detect_design_pattern
from crop_query import get_review_by_revision
from patterns_name import patterns
from config import crop_path
from time import time
from datetime import datetime
from itertools import islice
import json
import os

print(f'CURRENT TIME: {datetime.now()}')
start_time = time()
# all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
all_crop_projects = ['couchbase-java-client'] 

def add_review(detected_dp, project, revision, rev, dp_regex):
    dp_project = detect_design_pattern(project, dp_regex)
    if len(dp_project[dp_regex]) != 0:
        detected_dp[project][revision][rev].append(dp_project)

def partition(lst, n):
    division = len(lst) / float(n)
    return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

detected_dp = {}
for project in all_crop_projects:
    crop_repos_path = f'{crop_path}\\{project}'
    review_by_revision = get_review_by_revision(project)    
    hash_by_commit_name = get_hash_by_commit_name(project)
    code_review_partition_list = partition(list(review_by_revision.keys()), 20)
    
    count = 0
    for i, code_review_partition in enumerate(code_review_partition_list):
        detected_dp = {project: {}}
        for revision in code_review_partition:
            rev_list = review_by_revision[revision]
            detected_dp[project][revision] = {'code_review': rev_list}
            for rev in rev_list:
                count += 1
                print(f'revision: {revision} | rev: {rev} | COUNT: {count}')
                detected_dp[project][revision][rev] = []
                os.system(f'cd {crop_repos_path} & git checkout --force {hash_by_commit_name[rev]}')
                [add_review(detected_dp, project, revision, rev, dp_regex) for dp_regex in patterns]

        with open(f"{i}_{project}-dpd.json", "w") as outfile:
            json.dump(detected_dp, outfile, indent=4)

end_time = time() - start_time
print(f'{project} --- seconds: {end_time} --- minutes: {end_time/60}')