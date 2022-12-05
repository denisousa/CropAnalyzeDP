from dpd import detect_design_pattern
from crop_query import get_review_by_revision
from patterns_name import patterns
import os


# all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
all_crop_projects = ['jgit'] 


for project in all_crop_projects:
    review_by_revision = get_review_by_revision(project)    
    detected_dp = []
    [detected_dp.append(detect_design_pattern(project, dp_regex)) for dp_regex in patterns]

    # os.system(f'cd {crop_repos_path} & git --no-pager log > {current_path}\\{git_log_filename}')
    break
