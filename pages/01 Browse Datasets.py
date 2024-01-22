import streamlit as st
import os
import json
import pandas as pd

st.title('Browse Datasets')

json_metadata_files_path = 'datasets/metadata'
json_data_files_path = 'datasets/data'

metadata_files = [f for f in os.listdir(json_metadata_files_path) if f.endswith('.json')]

metadata_info = {}

for metadata_file in metadata_files:
    with open(os.path.join(json_metadata_files_path, metadata_file), 'r') as file:
        res = json.load(file)
        metadata_info[metadata_file] = res

#df = pd.DataFrame(metadata_info).T.reset_index(drop=True)
df = pd.DataFrame(metadata_info).T

sel_dataset = st.selectbox('sel', df['Title'].sort_values(), label_visibility='collapsed')

st.dataframe(pd.read_csv(json_data_files_path + '/' + sel_dataset + '.csv'))
st.table(metadata_info[df[df['Title'] == sel_dataset].index[0]])

st.write(metadata_info[df[df['Title'] == sel_dataset].index[0]]['Comment'])



my_dict = {
    'key1': 'This is a normal string.',
    'key2': '''This string
has a line break.
And another line break.''',
    'key3': '''last update of the dataset: 08.06.2021 by L. N. Warr
    based largely on IMA list (http://cnmnc.main.jp/) May 2021 version
    Symbol rules
    1: The first two or three letters of the mineral name (e.g. Saponite = Sap) if not common to many mineral phases.
    2: A combination of three or four letters that are characteristic of the mineral name (e.g. Chamosite = Chm)
    3: A selection of three or four letters representing components of the name (commonly syllables), if not already in use (e.g. Brammalite = Bml).
    4: As four or five-letter abbreviations when  prefixes are present and related mineral symbols have previously been defined (e.g. ferroaluminoceladonite is abbreviated to Facel, whereby the Kretz symbol for celadonite is cel.)
    
    IMA status (information from http://cnmnc.main.jp/)
    A: approved
    D: discredited
    G: grandfathered
    GROUP: name of group of mineral species
    Rd: redefined
    Rn: renamed
    Q: questioned
    I: informal
    NL: not listed
    ML: mixed layer
    
    Common prefixes
    A: Alumino-, Alumo-, Antho-, André-, Ammonio, Argento- (or Ag), Arsen-, Arseno-,  Auri (or Au)
    B: Baryto-, Blue-, Bob-, Bario-, Bismuto-
    C: Chloro-, Cupro-, Calcio-, Calc-, Chalco- (or cc), Crypto- (or Cp), Clino- (or Cl), Cobalt (or Cb)
    E: Epi-
    F: Ferro-, Ferric-, Fluor-, Fluro-
    G: Galeno-
    H: Hydro-, Hydroxy (or Hy), Hydroxyl-
    L: Lithio- (or Lh), Lothar-
    M: Lithio- (or Lh), Lothar-
    N: Natro-, Nikel-, Nitro-, Naba-, Niobo- (or Nb)
    O: Ortho-, Oxo-
    P: Para-, Pallado- (or Pd), Para-, Phospho (or Ph), Para-, Phospho- (or Ph), Plumbo- (or Pb), Potassic-
    S: Stibo-, Strontio- (or St)
    T: Telluro- (or Tl), Titano- (or Tt), Tung- (or Tg)
    U: Telluro- (or Tl), Titano- (or Tt), Tung- (or Tg)
    V: Viandio-
    Z: Zinc- (or Zn), Zinco- (or Zn)

    Common name components'''
}

st.subheader('Comment')
st.text(my_dict['key3'])

# ------ Siedbar

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