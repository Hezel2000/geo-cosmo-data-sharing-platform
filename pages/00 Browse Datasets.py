import streamlit as st
import pandas as pd

st.title('Browse Datasets')


import requests

def get_github_folder_contents(username, repository, path, branch='main'):
    api_url = f'https://api.github.com/repos/{username}/{repository}/contents/{path}?ref={branch}'
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        contents = response.json()
        return contents
    else:
        print(f"Failed to retrieve contents. Status code: {response.status_code}")
        return None

# Replace these with your GitHub username, repository name, and folder path
username = 'Hezel2000'
repository = 'GeoCosmoChemDataAndTools'
folder_path = 'csv'

contents = get_github_folder_contents(username, repository, folder_path)

if contents:
    dataset_name_list = []
    dataset_download_urls = []
    for item in contents:
        if item['name'].endswith('.csv'):
            dataset_name_list.append(item['name'].split('.')[0])
            dataset_download_urls.append(item['download_url'])

sel_dataset = st.selectbox('Select Dataset', dataset_name_list)

st.dataframe(pd.read_csv(dataset_download_urls[dataset_name_list.index(sel_dataset)]))
