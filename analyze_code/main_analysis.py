from patterns_name import patterns
from collections import Counter, OrderedDict
from operator import itemgetter
import json
import pandas as pd
import re
import os

patterns_join = '|'.join(patterns)
regex = f'({patterns_join})'
columns_df = ['project', 'match_by_line', 'match_count', 'number_lines','filename', 'path_filename']

all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
code_match_df = pd.DataFrame(columns=columns_df)
analyze_project_list = []


for project in all_crop_projects:
    crop_repos_path = f'C:\\Users\\Denis\\programming\\crop-git-repos\\git_repos\\{project}'
    print(f'\nANALYZE DESIGN PATTERNS IN CODE IN "{project}"\n')
    
    count_dp = 0
    amount_design_pattern_words = []

    for folder_path in os.walk(crop_repos_path):
        for filename in folder_path[2]:
            if '.java' in filename:
                filename_path = f'{folder_path[0]}/{filename}'
                try:
                    code_lines = open(filename_path, 'r', encoding='utf-8').readlines()
                except:
                    code_lines = open(filename_path, 'rb').readlines()
                    code_lines = [str(line) for line in code_lines]
                result = []
                lines = []
                for i,line in enumerate(code_lines):
                    new_result = re.findall(regex, line, re.IGNORECASE)
                    if len(new_result) > 0:
                        result.append(new_result)
                        lines.append(i+1)
                match_count = len(result)
                if len(result) > 0:
                    count_dp += 1
                    row = [[project, str(result), match_count, str(lines), filename, filename_path.split('crop/')[-1]]]
                    code_match_df = code_match_df.append(pd.DataFrame(row, columns=columns_df),ignore_index=True)
                    result = [dp.lower() for dp_list in result for dp in dp_list]
                    amount_design_pattern_words.append(result)

    amount_design_pattern_words = [dp for dp_list in amount_design_pattern_words for dp in dp_list]
    amount_design_pattern_words = dict(Counter(amount_design_pattern_words))
    analyze_project_list.append({
        'project': project,
        'amount_files': count_dp,
        'amount_design_pattern_words': OrderedDict(sorted(amount_design_pattern_words.items(), key=itemgetter(1), reverse=True))
    })

with open("analyze_code_match.json", "w") as outfile:
    json.dump(analyze_project_list, outfile, indent=4)
code_match_df.to_csv(f'code_match.csv', index=False)