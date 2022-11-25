import os
import re

def delete_file(file_path):
    try:
        os.remove(file_path)
    except:
        pass

def create_folders(folder_name):
    try:
        os.mkdir(folder_name)
        os.mkdir(f'{folder_name}/geral')
        os.mkdir(f'{folder_name}/title')
        os.mkdir(f'{folder_name}/description')
        os.mkdir(f'{folder_name}/comments')
    except:
        pass

def get_review_link(revision, crop_metadata_path, project):
    revision_correct_name = revision.split('_discussion')[0] 
    metadata_text = open(f'{crop_metadata_path}/{project}.csv', 'r').read()
    line = re.findall(f'{revision_correct_name}.*', metadata_text)
    if not line:
        return 'DO NOT HAVE LINK'
    return line[0].split(',')[6]

def specific_analysis(regex, csv_header, csv_folder, crop_discussions_path, crop_metadata_path):
    count_geral = 0
    total_geral = 0

    count_title = 0
    total_title = 0

    count_description = 0
    total_description = 0

    count_comment = 0
    total_comment = 0

    projects_name = [name for name in os.listdir(crop_discussions_path)]
    projects_name = ['egit', 'org.eclipse.linuxtools']
    for project in projects_name:
        delete_file(f'{csv_folder}/geral/{project}.csv')
        delete_file(f'{csv_folder}/title/{project}.csv')
        delete_file(f'{csv_folder}/description/{project}.csv')
        delete_file(f'{csv_folder}/comments/{project}.csv')

        project_geral = open(f'{csv_folder}/geral/{project}.csv', 'a')
        project_geral.write(csv_header)

        project_title = open(f'{csv_folder}/title/{project}.csv', 'a')
        project_title.write(csv_header)

        project_description = open(f'{csv_folder}/description/{project}.csv', 'a')
        project_description.write(csv_header)

        project_comments = open(f'{csv_folder}/comments/{project}.csv', 'a')
        project_comments.write(csv_header)

        reviews = [name for name in os.listdir(f'{crop_discussions_path}/{project}')]
        for review in reviews:
            revisions = [name for name in os.listdir(f'{crop_discussions_path}/{project}/{review}')]
            for revision in revisions:
                review_link = get_review_link(revision, crop_metadata_path, project)
                complete_path = f'{crop_discussions_path}/{project}/{review}/{revision}'
                discussion = open(complete_path, 'r').read()
                title_text = discussion.split('\n')[2]
                description_text = ''.join(discussion.split('COMMENTS')[0].split('\n')[4:]) 
                comment_text = ''.join(discussion.split('COMMENTS')[1])

                found_word_geral = re.findall(regex, discussion, re.IGNORECASE)
                word_title = re.findall(regex, title_text, re.IGNORECASE)
                word_description = re.findall(regex, description_text, re.IGNORECASE)
                word_comment = re.findall(regex, comment_text, re.IGNORECASE)

                evidence_line_csv = f'{review},{revision},{found_word_geral},{len(found_word_geral)},{review_link}\n'
                if found_word_geral:
                    project_geral.write(evidence_line_csv)
                    count_geral += 1
                    total_geral += 1

                if word_title:
                    project_title.write(evidence_line_csv)
                    count_title += 1
                    total_title += 1

                if word_description:
                    project_description.write(evidence_line_csv)
                    count_description += 1
                    total_description += 1

                if word_comment:
                    project_comments.write(evidence_line_csv)
                    count_comment += 1
                    total_comment += 1
 
        print(project)
        print('GERAL:', count_geral)
        print('TITLE:', count_title)
        print('DESCRIPTION:', count_description)
        print('COMMENTS:', count_comment)
        print('\n')
        count_geral = 0
        count_title = 0
        count_description = 0
        count_comment = 0

    print('TOTAL (GERAL): ', total_geral)
    print('TOTAL (TITLE): ', total_title)
    print('TOTAL (DESCRIPTION): ', total_description)
    print('TOTAL (COMMENTS): ', total_comment)

def complete_analysis(regex, csv_header, crop_discussions_path):
    count_geral = 0
    total_geral = 0

    count_title = 0
    total_title = 0

    count_description = 0
    total_description = 0

    count_comment = 0
    total_comment = 0

    projects_name = [name for name in os.listdir(crop_discussions_path)]
    for project in projects_name:
        delete_file(f'{complete_csv}/geral/{project}.csv')
        delete_file(f'{complete_csv}/title/{project}.csv')
        delete_file(f'{complete_csv}/description/{project}.csv')
        delete_file(f'{complete_csv}/comments/{project}.csv')

        project_geral = open(f'{complete_csv}/geral/{project}.csv', 'a')
        project_geral.write(f'{csv_header}\n')

        project_title = open(f'{complete_csv}/title/{project}.csv', 'a')
        project_title.write(f'{csv_header},title\n')

        project_description = open(f'{complete_csv}/description/{project}.csv', 'a')
        project_description.write(f'{csv_header},description\n')

        project_comments = open(f'{complete_csv}/comments/{project}.csv', 'a')
        project_comments.write(f'{csv_header},comments\n')

        reviews = [name for name in os.listdir(f'{crop_discussions_path}/{project}')]
        for review in reviews:
            revisions = [name for name in os.listdir(f'{crop_discussions_path}/{project}/{review}')]
            for revision in revisions:
                complete_path = f'{crop_discussions_path}/{project}/{review}/{revision}'
                discussion = open(complete_path, 'r').read()
                title_text = discussion.split('\n')[2]
                description_text = ''.join(discussion.split('COMMENTS')[0].split('\n')[4:]) 
                comment_text = ''.join(discussion.split('COMMENTS')[1])

                found_word_geral = re.findall(regex, discussion, re.IGNORECASE)
                word_title = re.findall(regex, title_text, re.IGNORECASE)
                word_description = re.findall(regex, description_text, re.IGNORECASE)
                word_comment = re.findall(regex, comment_text, re.IGNORECASE)

                if found_word_geral:
                    project_geral.write(evidence_line_csv)
                    count_geral += 1
                    total_geral += 1

                if word_title:
                    project_title.write(f'{review},{revision},{found_word_geral},{len(found_word_geral)},{title_text}\n')
                    count_title += 1
                    total_title += 1

                if word_description:
                    project_description.write(f'{review},{revision},{found_word_geral},{len(found_word_geral)},{description_text}\n')
                    count_description += 1
                    total_description += 1

                if word_comment:
                    project_comments.write(f'{review},{revision},{found_word_geral},{len(found_word_geral)},{comment_text}\n')
                    count_comment += 1
                    total_comment += 1
 
        print(project)
        print('GERAL:', count_geral)
        print('TITLE:', count_title)
        print('DESCRIPTION:', count_description)
        print('COMMENTS:', count_comment)
        print('\n')
        count_geral = 0
        count_title = 0
        count_description = 0
        count_comment = 0

    print('TOTAL (GERAL): ', total_geral)
    print('TOTAL (TITLE): ', total_title)
    print('TOTAL (DESCRIPTION): ', total_description)
    print('TOTAL (COMMENTS): ', total_comment)