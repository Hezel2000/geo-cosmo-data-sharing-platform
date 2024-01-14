
import streamlit as st
import requests
import json
from pathlib import Path
import base64
import pandas as pd
from datetime import datetime    

#st.session_state.is_authenticated=True

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
            base64_string = base64_bytes.decode('utf-8')
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

# -----------------------------
# ---------- Program ----------
# -----------------------------

st.title("File Upload to the mag4 Database")
st.header('Choose file to upload')

# Depends on whether a user is logged in to Orcid -> False when logged in
if st.session_state.is_authenticated:
    file_uploader_enable_parameter=False
else:
    file_uploader_enable_parameter=True

# File uploader widget
uploaded_file = st.file_uploader('', type=["csv", "xlsx"], label_visibility='collapsed', disabled=file_uploader_enable_parameter)

if uploaded_file is not None:
    # Save the uploaded file to the server in the datasets folder
    file_path_user_dataset = Path("datasets") / uploaded_file.name
    #st.write(file_path_user_dataset)
    with open(file_path_user_dataset, "wb") as f:
        f.write(uploaded_file.getbuffer())
    #st.success(f"File saved to {file_path}")


# ---------- Metadata Fields
    st.header('Metadata')
    st.subheader('Mandatory')
    meta_orcid = 'to be replaced with ->' #uploader_orcid
    meta_email = st.text_input('Email address', value=None, placeholder='Email addressyour email address')
    meta_title = st.text_input('Title', value=None, placeholder='Electron Transition Energies')
    meta_short_title = st.text_input('Short Title', value=None, placeholder='electransener')
    meta_keywords = st.text_input('Keywords (comma separted if more than one – which would be helpful)', value=None, placeholder='eV, absorption, edge, binding, x-ray', help='These are used in the search function. No need to repeat words that are already in the title or description.')
    meta_description = st.text_input('Description', value=None, placeholder='IMA–CNMNC approved mineral symbols')
    meta_type = st.selectbox('Type of dataset', ('basic', 'standard','example', 'other'), help='basic: e.g., element masses, element-oxide conversion factors, decay constants; standard: composition of (a) reference material(s); example: to be used for testing or education;  other: anything else – please indicate in the comments why you chose other')
    meta_usage_licence = st.selectbox('Licence how the uploaded dataset can be used', ('CCO', 'CC-BY', 'CC-BY SA'), help='cf. https://creativecommons.org/share-your-work/cclicenses/')

    st.subheader('Optional')
    meta_available_app = st.text_input('Available App', value=None, placeholder='app url (comma separated if more than one)', help='If you build an app around this dataset, you cann add the link to this app here. Information how to quickly build insight- and/or powerful apps around your dataset can be found on the navigation bar.')
    meta_creation_date = st.date_input('Date when dataset was created', value=None)
    meta_source = st.text_input('Source', value=None, placeholder='Karlsruhe Institute of Technology Chart of Nuclides', help='Add the source as name, weblink, ... so the origin of the dataset can be traced back, if it is not yours.')
    meta_references = st.text_input('Reference(s) (comma separated if more than one)', value=None, placeholder='10.1016/j.chemer.2017.05.003, 10.2138/gselements.16.1.73', help='as dois only. A doi is a **d**igital **o**bject **i**dentifier that is almost always provided with a publication or other digital object such as a database.')
    meta_comments = st.text_input('Comment(s)', value=None, placeholder='everything not coverd above')


# ---------- Metadata Preview
    st.subheader('Preview')
    json_metadata = {
        # , jupyter notebook
        "ORCID": "automatically filled with -> #uploader_orcid",
        "Email": meta_email if meta_email is not None else 'still required',
        "Title": meta_title if meta_title is not None else 'still required',
        "Short Title": meta_short_title if meta_short_title is not None else 'still required',
        "Description": meta_description if meta_description is not None else 'still required',
        "Keywords":  meta_keywords if meta_keywords is not None else 'still required',
        "Type": meta_type if meta_type is not None else 'still required',
        "Creation Date": meta_creation_date.strftime("%Y-%m-%d") if meta_creation_date is not None else None,
        "Upload Date": datetime.now().strftime("%Y-%m-%d"),
        "Source": meta_source if meta_source is not None else None,
        "References": meta_references if meta_references is not None else None,
        "Comments": meta_comments if meta_comments is not None else None
    }

    #Writing the json file
    metadata_json_file_name = uploaded_file.name.split('.')[0]+'.json'
    file_path_json_metadata = Path("datasets") / metadata_json_file_name
    #st.write(file_path_json_metadata)

    with open(file_path_json_metadata, "w") as f:
        json.dump(json_metadata, f)

    st.write(pd.read_json(file_path_json_metadata, typ="series"))


# ---------- Commit and push changes to GitHub
    if meta_orcid == 'still required' or meta_email == 'still required' or meta_title == 'still required' or meta_short_title =='still required' or meta_keywords == 'still required' or meta_description == 'still required' or meta_type == 'still required' or meta_usage_licence == 'still required'
        st.write('All required metadata need to be added (with sensible information).')
    else:
        if st.button("Upload to mag4"):
            response = upload_to_github(file_path_user_dataset, meta_orcid, 'csv')
            if response.status_code == 201:
                st.success(f"Dataset file was successfully uploaded to GitHub.")
            else:
                st.error(f"Error uploading file to GitHub. Status Code: {response.status_code}, Response: {response.text}")

            response = upload_to_github(file_path_json_metadata, meta_orcid, 'json')
            if response.status_code == 201:
                st.success(f"Metadata file was successfully uploaded to GitHub.")
            else:
                st.error(f"Error uploading file to GitHub. Status Code: {response.status_code}, Response: {response.text}")


if st.session_state.is_authenticated:
    st.sidebar.success("You are logged in with ORCID")
else:
    st.sidebar.error("ORCID login required for full functionality")
