
import streamlit as st
import requests
from pathlib import Path

#base_url = 'https://raw.githubusercontent.com/Hezel2000/cosmogeochemdata/master/'


def upload_to_github(file_path, commit_message):
    # Replace these variables with your GitHub repository details
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
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Create a new commit with the updated file
    commit_data = {
        "message": commit_message,
        "content": file_content.decode("utf-8"),
        "sha": sha,
        "branch": branch_name
    }

    # Use your GitHub token here
    #github_token = st.secrets["GitHub_Token"]
    github_token = "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"
    response = requests.put(
        github_api_url,
        headers={"Authorization": f"Bearer {github_token}"},
        json=commit_data
    )

    if response.status_code == 200:
        st.success(f"File '{file_name}' uploaded to GitHub successfully!")
    else:
        st.error(f"Error uploading file to GitHub. Status Code: {response.status_code}, Response: {response.text}")

st.title("GitHub File Uploader")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "xlsx"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")

    # Save the uploaded file to the server in the uploads folder
    file_path = Path("uploads") / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved to {file_path}")

    # Commit and push changes to GitHub
    commit_message = st.text_input("Enter commit message:")
    if st.button("Upload to GitHub"):
        upload_to_github(file_path, commit_message)
