from analyze_operation import create_folders, specific_analysis
from patterns_name import patterns

crop_metadata_path = '/home/denis/projects/crop/metadata'
crop_discussions_path = '/home/denis/projects/crop/discussion'
csv_header = 'review,revision,found_words,number_words,review_link'
patterns_join = '|'.join(patterns)

regex = f'({patterns_join})'


for pattern in patterns:
    print(f'\nREGEX TO CATCH IN DISCUSSIONS "{pattern}" WORDS\n')
    create_folders(pattern)
    specific_analysis(pattern, csv_header, pattern, crop_discussions_path, crop_metadata_path)
    

