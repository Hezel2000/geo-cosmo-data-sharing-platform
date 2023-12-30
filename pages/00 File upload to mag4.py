
import streamlit as st
import requests
import json
from pathlib import Path
import base64
import pandas as pd
from datetime import datetime

def upload_to_github(file_path, commit_message, file_type):
    repo_owner = "Hezel2000"
    repo_name = "GeoCosmoChemDataAndTools"
    branch_name = "main"
    file_name = file_path.name

    # Get the content of the existing file on GitHub
    github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name}"
    response = requests.get(github_api_url)
    
    if response.status_code == 200:
        existing_content = response.json()
        sha = existing_content["sha"]
    else:
        existing_content = None
        sha = None

    # Read the local file content
    if file_type == 'csv':
        with open(file_path, "rb") as file:
            file_content = file.read()
            base64_bytes = base64.b64encode(file_content) 
            base64_string = base64_bytes.decode("utf-8")
    elif file_type == 'json':
        with open(file_path, "r") as file:
            file_content = file.read()
            base64_bytes = base64.b64encode(file_content.encode('utf-8'))
            base64_string = json_base64_bytes.decode('utf-8')
    else:
        return st.write('Something is wrong with the filetype')
    
    # Create a new commit with the updated file
    commit_data = {
        "message": commit_message,
        "content": base64_string,
        "sha": sha,
        "branch": branch_name
    }

    # Use your GitHub token here
    github_token = st.secrets["GitHub_Token"]
    response = requests.put(
        github_api_url,
        headers={"Authorization": f"Bearer {github_token}"},
        json=commit_data
    )

    return response


st.title("File Upload to the mag4 Database")
st.header('Choose file to upload')

# Depends on whether a user is logged in to Orcid -> False when logged in
file_uploader_enable_parameter=False

# File uploader widget
uploaded_file = st.file_uploader('', type=["csv", "xlsx"], label_visibility='collapsed', disabled=file_uploader_enable_parameter)

if uploaded_file is not None:
    # Save the uploaded file to the server in the uploads folder
    file_path = Path("uploads") / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    #st.success(f"File saved to {file_path}")


    st.header('Metadata')

    # Metadata
    st.subheader('Mandatory')
    commit_message = 'to be replaced with ->' #uploader_orcid
    meta_name = st.text_input('Name', value=None, placeholder='Dominik Hezel')
    meta_usage_licence = st.selectbox('Licence how the uploaded dataset can be used.', ('CCO', 'CC-BY', 'CC-BY SA'), help='cf. https://creativecommons.org/share-your-work/cclicenses/')

    st.subheader('Optional')
    meta_source = st.text_input('Source', value=None, placeholder='Karlsruhe Institute of Technologie Chart of Nuclides', help='Add the source as name, weblink, ... so the origin of the dataset can be traced back, if it is not yours.')
    meta_references = st.text_input('Reference(s) (comma separated if more than one)', value=None, placeholder='10.1016/j.chemer.2017.05.003, 10.2138/gselements.16.1.73', help='as dois only. A doi is a **d**igital **o**bject **i**dentifier that is almost always provided with a publication or other digital object such as a database.')

    st.subheader('Preview')
    json_metadata = {
        "ORCID": "to be replaced with -> #uploader_orcid",
        "Upload Date": datetime.now().strftime("%Y-%m-%d"),
        "Name": meta_name if meta_name is not None else 'still required',
        "Source": meta_source if meta_source is not None else None,
        "References": meta_references if meta_references is not None else None
    }

    #Writing the json file
    file_path_json_metadata = 'metadata.json'

    with open(file_path_json_metadata, "w") as f:
        json.dump(json_metadata, f)

    st.write(pd.read_json(file_path_json_metadata, typ="series"))


    # Commit and push changes to GitHub
    if st.button("Upload to GitHub"):
        response = upload_to_github(file_path_user_dataset, commit_message, 'csv')

        if response.status_code == 201:
            st.success(f"File was was uploaded to GitHub successfully!")
            #st.write(response.text.content.name)
        else:
            st.error(f"Error uploading file to GitHub. Status Code: {response.status_code}, Response: {response.text}")

        response = upload_to_github(file_path_json_metadata, commit_message, 'json')

        if response.status_code == 201:
            st.success(f"File was was uploaded to GitHub successfully!")
            #st.write(response.text.content.name)
        else:
            st.error(f"Error uploading file to GitHub. Status Code: {response.status_code}, Response: {response.text}")
