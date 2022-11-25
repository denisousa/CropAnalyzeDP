from patterns_name import patterns
import pandas as pd
import re
import os

patterns_join = '|'.join(patterns)
regex = f'({patterns_join})'
columns_df = ['project', 'match', 'math_count','filename', 'path_filename']

all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
code_match_df = pd.DataFrame(columns=columns_df)

for project in all_crop_projects:
    crop_repos_path = f'/home/denis/projects/crop/git_repos/{project}'
    print(f'\nANALYZE DESIGN PATTERNS IN CODE IN "{project}"\n')
    for folder_path in os.walk(crop_repos_path):
        for filename in folder_path[2]:
            if '.java' in filename:
                result = re.findall(regex, filename, re.IGNORECASE)
                match_count = len(result)
                if len(result) > 0:
                    row = [[project, str(result), filename, match_count, f'{folder_path[0]}/{filename}']]
                    code_match_df = code_match_df.append(pd.DataFrame(row, columns=columns_df),ignore_index=True)

code_match_df.to_csv(f'filename_match.csv', index=False)