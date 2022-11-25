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


    projects_name = [name for name in os.listdir(crop_discussions_path)]
    projects_name = ['egit', 'org.eclipse.linuxtools']
    for project in projects_name:
