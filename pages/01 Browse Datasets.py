import streamlit as st
import requests
import os
import json
import pandas as pd

st.title('Browse Datasets')

def get_files_from_github(repo_owner, repo_name, folder):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder}'
    github_token = st.secrets['GitHub_Token']
    headers = {'Authorization': f'Bearer {github_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        files = [file['download_url'] for file in response.json()]
        return files
    else:
        return f"Error: Unable to fetch files. Status code: {response.status_code}"

repo_owner = "Hezel2000"
repo_name = "mag4datasets"
folder = "data"
# github_token = st.secrets['GitHub_Token']

st.write(get_files_from_github(repo_owner, repo_name, folder))

# json_metadata_files_path = 'datasets/metadata'
# json_data_files_path = 'datasets/data'

# metadata_files = [f for f in os.listdir(json_metadata_files_path) if f.endswith('.json')]

# metadata_info = {}

# for metadata_file in metadata_files:
#     with open(os.path.join(json_metadata_files_path, metadata_file), 'r') as file:
#         res = json.load(file)
#         metadata_info[metadata_file] = res

# #df = pd.DataFrame(metadata_info).T.reset_index(drop=True)
# df = pd.DataFrame(metadata_info).T

# sel_dataset = st.selectbox('sel', df['Title'].sort_values(), label_visibility='collapsed')

# st.dataframe(pd.read_csv(json_data_files_path + '/' + sel_dataset + '.csv'))
# st.table(metadata_info[df[df['Title'] == sel_dataset].index[0]])

# st.write(metadata_info[df[df['Title'] == sel_dataset].index[0]]['Comment'])


# # ------ Siedbar

# if st.session_state.is_authenticated:
#     st.sidebar.success("You are logged in with ORCID")
# else:
#     st.sidebar.error("ORCID login required for full functionality")




# Use the following, if the data are in a different repo

# import requests

# def get_github_folder_contents(username, repository, path, branch='main'):
#     api_url = f'https://api.github.com/repos/{username}/{repository}/contents/{path}?ref={branch}'
#     github_token = st.secrets['GitHub_Token']
#     headers = {"Authorization": f"Bearer {github_token}"}
#     response = requests.get(api_url, headers=headers)
    
#     if response.status_code == 200:
#         contents = response.json()
#         return contents
#     else:
#         return st.write(f"Failed to retrieve contents. Status code: {response.status_code}")

# # Replace these with your GitHub username, repository name, and folder path
# username = 'Hezel2000'
# repository = 'GeoCosmoChemDataAndTools'
# folder_path = 'csv'

# contents = get_github_folder_contents(username, repository, folder_path)

# if contents:
#     dataset_name_list = []
#     dataset_download_urls = []
#     for item in contents:
#         if item['name'].endswith('.csv'):
#             dataset_name_list.append(item['name'].split('.')[0])
#             dataset_download_urls.append(item['download_url'])

# sel_dataset = st.selectbox('Select Dataset', dataset_name_list)

# st.dataframe(pd.read_csv(dataset_download_urls[dataset_name_list.index(sel_dataset)]))