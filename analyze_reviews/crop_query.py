from patterns_name import patterns
from config import repos_path, current_path
import pandas as pd
import pathlib
import re
import os


def get_review_by_revision(project):
    crop_repos_path = f'{repos_path}\\{project}'

    git_log_filename = 'git-log.txt'
    os.system(f'cd {crop_repos_path} & git --no-pager log --all > {current_path}\\{git_log_filename}')
    git_log_txt = open(f'{current_path}\\{git_log_filename}', 'r').read()

    commit_name_result = re.findall('First commited as .*\n', git_log_txt, re.IGNORECASE)
    review_list = [item.replace('\n', '').split(' ')[-1] for item in commit_name_result]
    
    revision_list = list(set([item.split('_')[1] for item in review_list]))

    review_by_revision = {f'{revision}_revision' : [] for revision in revision_list}

    for revision in revision_list:
        [review_by_revision[f'{revision}_revision'].append(review) for review in review_list if revision in review]
    
    return review_by_revision

def get_hash_by_commit_name(project):
    crop_repos_path = f'{repos_path}\\{project}'

    git_log_filename = 'git-log.txt'
    os.system(f'cd {crop_repos_path} & git --no-pager log --all > {current_path}\\{git_log_filename}')
    git_log_txt = open(f'{current_path}\\{git_log_filename}', 'r').read()

    commit_name_result = re.findall('First commited as .*\n', git_log_txt, re.IGNORECASE)
    commit_list = [item.replace('\n', '').split(' ')[-1] for item in commit_name_result]
    
    commit_hash_result = re.findall('commit .*\n', git_log_txt, re.IGNORECASE)
    hash_list = [item.replace('\n', '').split(' ')[-1] for item in commit_hash_result]
    
    hash_by_commit_name = {}
    for i in range(len(commit_list)):
        hash_by_commit_name[commit_list[i]] = hash_list[i]
    
    return hash_by_commit_name
    