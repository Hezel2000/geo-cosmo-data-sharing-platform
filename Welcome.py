import streamlit as st
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

authorization_response = None

# Orcid Auth
# Install this package
# pip install oauthlib requests

# Your Orcid credentials
CLIENT_ID = st.secrets["Orcid_ID"]
CLIENT_SECRET = st.secrets["Orcid_Secret"]
ORCID_API_URL = "https://pub.orcid.org/v3.0/"
REDIRECT_URI = "https://geo-cosmo-data-sharing-platform-bvniuih82j6l2aeq3jxfyb.streamlit.app/"  # Update with your actual redirect URI

# Function to get Orcid authorization URL
# def get_orcid_authorization_url():
#     client = WebApplicationClient(client_id=CLIENT_ID)
#     oauth = OAuth2Session(client=client, redirect_uri=REDIRECT_URI)
#     authorization_url, state = oauth.authorization_url("https://orcid.org/oauth/authorize")
#     return authorization_url
def get_orcid_authorization_url():
    client = WebApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client, redirect_uri=REDIRECT_URI, scope=["openid", "profile", "email", "orcid"])
    authorization_url, state = oauth.authorization_url("https://orcid.org/oauth/authorize")
    return authorization_url
    #return REDIRECT_URI

# Function to get Orcid token
def get_orcid_token(authorization_response):
    client = WebApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client, redirect_uri=REDIRECT_URI)
    token_url = "https://orcid.org/oauth/token"
    token = oauth.fetch_token(
        token_url=token_url,
        authorization_response=authorization_response,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        include_client_id=True
    )
    return token

# Streamlit app
st.title("Streamlit Orcid Authentication")

# Check if the user is authenticated
is_authenticated = st.session_state.get("is_authenticated", False)
st.write('authenticated', is_authenticated)
st.write(authorization_response)

if not is_authenticated:
    # Orcid login button
    if st.button("Login with Orcid"):
        # Redirect user to Orcid for authorization
        authorization_url = get_orcid_authorization_url()
        st.write(f"Click [here]({authorization_url}) to log in with Orcid.")
        
        # After the user authorizes, they will be redirected back with the authorization code
        authorization_response = st.text_input("Enter the Orcid authorization code:")
        
        if authorization_response:
            # Get Orcid token
            orcid_token = get_orcid_token(authorization_response)
            st.session_state.is_authenticated = True
            st.session_state.orcid_token = orcid_token
            st.success("Successfully logged in with Orcid!")

# Display user info if authenticated
if is_authenticated:
    st.sidebar.info("You are logged in with Orcid.")
    
    # Your existing Streamlit content goes here
    st.title('Your uploaded files')
    st.write('A simply filtered table with your uploaded datasets, with a number of editing options: update, delete (restricted!)')
