import streamlit as st
import os
import json
import pandas as pd

st.title('Browse Datasets')

st.subheader('Read in files')

json_metadata_files_path = 'datasets/metadata'
json_data_files_path = 'datasets/data'

metadata_files = [f for f in os.listdir(json_metadata_files_path) if f.endswith('.json')]

metadata_info = {}

for metadata_file in metadata_files:
    with open(os.path.join(json_metadata_files_path, metadata_file), 'r') as file:
        res = json.load(file)
        metadata_info[metadata_file] = res

df = pd.DataFrame(metadata_info).T.reset_index(drop=True)

sel_dataset = st.selectbox('sel', df['Title'], label_visibility='collapsed')

st.dataframe(pd.read_csv(json_data_files_path + '/' + sel_dataset + '.csv'))


if st.session_state.is_authenticated:
    st.sidebar.success("You are logged in with ORCID")
else:
    st.sidebar.error("ORCID login required for full functionality")


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