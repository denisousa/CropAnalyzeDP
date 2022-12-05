from patterns_name import patterns
from config import crop_path, current_path
import pandas as pd
import pathlib
import re
import os


def get_review_by_revision(project):
    crop_repos_path = f'{crop_path}\\{project}'

    git_log_filename = 'git-log.txt'
    os.system(f'cd {crop_repos_path} & git --no-pager log > {current_path}\\{git_log_filename}')
    git_log_txt = open(f'{current_path}\\{git_log_filename}', 'r').read()

    commit_name_result = re.findall('First commited as .*\n', git_log_txt, re.IGNORECASE)
    review_list = [item.replace('\n', '').split(' ')[-1] for item in commit_name_result]
    
    commit_hash_result = re.findall('commit .*\n', git_log_txt, re.IGNORECASE)
    hash_list = [item.replace('\n', '').split(' ')[-1] for item in commit_hash_result]
    
    revision_list = list(set([item.split('_')[1] for item in review_list]))

    review_by_revision = {f'{revision}_revision' : [] for revision in revision_list}

    for revision in revision_list:
        [review_by_revision[f'{revision}_revision'].append(review) for review in review_list if revision in review]
    
    return review_by_revision

def detect_dp_by_commit(project, commit):
    crop_repos_path = f'{crop_path}\\{project}'

    os.system(f'cd {crop_repos_path} & git checkout First commited as {commit}')

