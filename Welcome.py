import streamlit as st
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

# Orcid Auth
# Install this package
# pip install oauthlib requests

# Your Orcid credentials
CLIENT_ID = "your_orcid_client_id"
CLIENT_SECRET = "your_orcid_client_secret"
ORCID_API_URL = "https://pub.orcid.org/v3.0/"
REDIRECT_URI = "https://geo-cosmo-data-sharing-platform-bvniuih82j6l2aeq3jxfyb.streamlit.app" #/oauth/callback"  # Update with your actual redirect URI

# Function to get Orcid authorization URL
def get_orcid_authorization_url():
    client = WebApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client, redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url("https://orcid.org/oauth/authorize")
    return authorization_url

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


# import streamlit as st
# from requests_oauthlib import OAuth2Session

# # OAuth configuration
# client_id = "your_client_id"
# client_secret = "your_client_secret"
# authorization_base_url = "https://oauth.provider.com/authorize"
# token_url = "https://oauth.provider.com/token"
# redirect_uri = "http://localhost:8501/oauth_callback"  # Update with your redirect URI

# # Create an OAuth session
# oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

# def main():
#     st.title("OAuth Streamlit App")

#     # Check if the user is already authenticated
#     if "token" not in st.session_state:
#         # If not authenticated, provide a button for the user to initiate OAuth flow
#         if st.button("Login with OAuth"):
#             authorization_url, state = oauth.authorization_url(authorization_base_url)
#             st.session_state.oauth_state = state
#             st.redirect(authorization_url)
#     else:
#         # User is authenticated, display information or perform authorized actions
#         st.success("Authenticated successfully!")
#         user_info = oauth.get("https://api.oauth.provider.com/userinfo").json()
#         st.json(user_info)

# if __name__ == "__main__":
#     main()
