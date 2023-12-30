import streamlit as st
import requests
import base64
import json

st.title('Your mag4 File Center')

st.write('Login with Orcid to actively use this webpage.')

st.write('ORCID login')


file_path = "uploads/fq176 copy 2.csv"
commit_message = 'test'

repo_owner = "Hezel2000"
repo_name = "GeoCosmoChemDataAndTools"
branch_name = "main"
file_name = "GCCdata.csv" #file_path.name

# Get the content of the existing file on GitHub
github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name}"
response = requests.get(github_api_url)
st.write(response.json())

if response.status_code == 200:
    existing_content = response.json()
    sha = existing_content["sha"]
else:
    existing_content = None
    sha = None

st.write(sha)

# Read the local file content
with open(file_path, "rb") as file:
    file_content = file.read()
    base64_bytes = base64.b64encode(file_content) 
    base64_string = base64_bytes.decode("utf-8")

# Read the local file content
with open(file_path, "r") as file:
    file_content = file.read()
    json_base64_bytes = base64.b64encode(file_content.encode('utf-8'))
    json_base64_string = json_base64_bytes.decode('utf-8')

# Create a new commit with the updated file
commit_data = {
    "message": commit_message,
    "content": base64_string,
    "sha": sha,
    "branch": branch_name
}

st.write(commit_data)

# Use your GitHub token here
github_token = st.secrets["GitHub_Token"]
response = requests.put(
    github_api_url,
    headers={"Authorization": f"Bearer {github_token}"},
    json=commit_data
)

st.write(response)