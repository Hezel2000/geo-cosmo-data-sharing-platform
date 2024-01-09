import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

st.title('Your mag4 File Center')

st.write('Login with Orcid to actively use this webpage.')

st.write('ORCID login')


st.write('Orcid Auth')
# orcid Auth 
# install this package 
#pip install oauthlib requests

# Your Orcid credentials
CLIENT_ID = st.secrets["Orcid_User"] # "your_orcid_client_id"
CLIENT_SECRET = st.secrets["Orcid_PW"] # "your_orcid_client_secret"
ORCID_API_URL = "https://pub.orcid.org/v3.0/"

# Function to get Orcid token
def get_orcid_token():
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token_url = "https://orcid.org/oauth/token"
    token = oauth.fetch_token(
        token_url=token_url,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        include_client_id=True
    )
    return token

# Function to fetch Orcid user information
def get_orcid_user_info(orcid_token):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {orcid_token['access_token']}",
    }
    response = requests.get(f"{ORCID_API_URL}myself", headers=headers)
    user_info = response.json()
    return user_info


# Streamlit app
st.title("Streamlit Orcid Authentication")

# Check if the user is authenticated
is_authenticated = st.session_state.get("is_authenticated", False)

if not is_authenticated:
    # Orcid login button
    if st.button("Login with Orcid"):
        # Get Orcid token
        orcid_token = get_orcid_token()
        st.session_state.is_authenticated = True
        st.session_state.orcid_token = orcid_token
        st.success("Successfully logged in with Orcid!")

# Display user info if authenticated
if is_authenticated:
    st.sidebar.info("You are logged in with Orcid.")
    
    # Fetch and display user information
    user_info = get_orcid_user_info(st.session_state.orcid_token)
    st.sidebar.subheader("User Information:")
    st.sidebar.write(f"Name: {user_info['name']['given-names']['value']} {user_info['name']['family-name']['value']}")
    st.sidebar.write(f"Orcid ID: {user_info['orcid-identifier']['path']}")

    # Your existing Streamlit content goes here
    st.title('Your uploaded files')
    st.write('A simply filtered table with your uploaded datasets, with a number of editing options: update, delete (restricted!)')