import os
import re
from config import crop_path


def detect_design_pattern(project, dp_regex):
    filename_by_project = {dp_regex: []}
    crop_repos_path = f'{crop_path}\\{project}'
    for folder_path in os.walk(crop_repos_path):
        for filename in folder_path[2]:
            if '.java' in filename:
                filename_path = f'{folder_path[0]}\\{filename}'
                result = re.findall(dp_regex, filename, re.IGNORECASE)
                if len(result) > 0:
                    filename_by_project[dp_regex].append(filename_path.split('git_repos')[-1])
    return filename_by_project