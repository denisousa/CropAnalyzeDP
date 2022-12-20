
from crop_query import get_review_by_revision
from deepdiff import DeepDiff
from time import time
from datetime import datetime
import json

# CHANGE DP, EMERGENCE DP, REMOVAL DP, INCREASES DP, DECREASES DP
def get_amount(amount_analyze, rev):
    amount_analyze[rev] = {}
    for dp_analyze in analyze_result[project][revision][rev]:
        amount_analyze[rev][list(dp_analyze.keys())[0]] = len(list(dp_analyze.values())[0])

def define_df_change(amount_analyze): 
    diff = DeepDiff(amount_analyze[delta[1]],amount_analyze[delta[0]])
    if len(diff) == 0:
        return 'CHANGE_DP'
    
    if 'dictionary_item_added' in diff:
        return 'EMERGENCE_DP'
    
    if 'dictionary_item_removed' in diff:
        return 'REMOVAL_DP'

    values_changed = list(diff['values_changed'].values())[0]

    if values_changed['new_value'] < values_changed['old_value']:
        return 'DECREASES_DP'

    if values_changed['new_value'] > values_changed['old_value']:
        return 'INCREASES_DP'

def aggregate_revision_son_father(code_review):
    code_review = analyze_result[project][revision]['code_review']
    revs = set([i.split('_')[-1] for i in code_review])
    compare_revision = {}
    for rev in revs:
        compare_revision[rev] = []
        [compare_revision[rev].append(review) for review in code_review if rev in review]
    return compare_revision

def analyze_delta(compare_code_reviews, project, revision, delta, count):
    before, after = get_before_after(delta)
        
    if analyze_result[project][revision][before] == analyze_result[project][revision][after]:
        return count
    else:            
        if revision not in compare_code_reviews[project]:
            compare_code_reviews[project][revision] = {}
        count += 1
        amount_analyze = {}
        
        get_amount(amount_analyze, before)
        get_amount(amount_analyze, after)
        status = define_df_change(amount_analyze)
        
        new_key = f'delta_{delta[0]}_{delta[1]}'
        amount_analyze['status'] = status
        compare_code_reviews[project][revision][new_key] = amount_analyze
        return count
    
compare_code_reviews = {}
print(f'CURRENT TIME: {datetime.now()}')
start_time = time()
# all_crop_projects = ['jgit', 'egit', 'couchbase-jvm-core', 'org.eclipse.linuxtools', 'spymemcached', 'eclipse.platform.ui', 'couchbase-java-client'] 
all_crop_projects = ['couchbase-java-client'] 

for project in all_crop_projects:
    review_by_revision = get_review_by_revision(project)
    compare_code_reviews[project] = {}
    no_compare_code_reviews = {}
    compare_code_reviews[project]['total_revisions'] = 0
    compare_code_reviews[project]['total_revisions_with_changes'] = 0
    compare_code_reviews[project]['total_code_review_with_changes'] = 0
    count = 0

    for i in range(20):
        try:
            dpd_json = open(f'.\\analyze_reviews\\results\\{i}_{project}-dpd.json', 'r').read()
        except:
            continue
        analyze_result = json.loads(dpd_json)
        
        for revision, rev_list in analyze_result[project].items():
            if revision not in analyze_result[project]:
                continue
            
            if len(rev_list['code_review']) % 2 != 0:
                no_compare_revision = rev_list['code_review']
                compare_code_reviews[project]['total_revisions'] += len(rev_list['code_review'])
                compare_code_reviews[project]['total_no_compare'] += len(rev_list['code_review'])
                no_compare_code_reviews[revision] = no_compare_revision
                continue
            
            code_review = rev_list['code_review']
            compare_revision = aggregate_revision_son_father(code_review)

            for _, delta in compare_revision.items():
                count = analyze_delta(compare_code_reviews, project, revision, delta, count)

            compare_code_reviews[project]['total_revisions'] += len(rev_list['code_review'])

                
    compare_code_reviews[project]['total_revisions_with_changes'] = count
    compare_code_reviews[project]['total_code_review_with_changes'] = len(list(compare_code_reviews[project].keys())) - 2

    with open(f"compare_{project}.json", "w") as outfile:
        json.dump(compare_code_reviews, outfile, indent=4)

    end_time = time() - start_time
    print(f'{project} --- seconds: {end_time} --- minutes: {end_time/60}')