import streamlit as st
from requests.auth import HTTPBasicAuth
import requests

# Orcid Auth
# Your Orcid credentials
CLIENT_ID = st.secrets["Orcid_ID"]
CLIENT_SECRET = st.secrets["Orcid_Secret"]
ORCID_API_URL = "https://pub.orcid.org/v3.0/"
REDIRECT_URI = "https://mag4-data-sharing-platform.streamlit.app"
#REDIRECT_URI = "https://geo-cosmo-data-sharing-platform-bvniuih82j6l2aeq3jxfyb.streamlit.app/"

# Streamlit app
st.title("Streamlit Orcid Authentication")
st.write('test')

# Check if the user is authenticated
is_authenticated = st.session_state.get("is_authenticated", False)

if not is_authenticated:
    # Orcid login button
    if st.button("Login with Orcid"):
        # Redirect user to Orcid for authorization
        authorization_url = f"https://orcid.org/oauth/authorize?client_id={CLIENT_ID}&response_type=code&scope=/authenticate&redirect_uri={REDIRECT_URI}"
        st.write(f"Click [here]({authorization_url}) to log in with Orcid.")

        # Check if the authorization code is present in the URL
        url = st.experimental_get_query_params()
        authorization_response = url.get("code", None)

        if authorization_response:
            # Exchange authorization code for access token
            token_url = "https://orcid.org/oauth/token"
            token_data = {
                "grant_type": "authorization_code",
                "code": authorization_response,
                "redirect_uri": REDIRECT_URI,
            }
            auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
            response = requests.post(token_url, data=token_data, auth=auth)

            if response.status_code == 200:
                # Token successfully obtained
                token_info = response.json()
                st.session_state.is_authenticated = True
                st.session_state.orcid_token = token_info

                # Redirect to the main app with a success flag in the URL
                st.write('<meta http-equiv="refresh" content="0;URL=/?success=true">')

            else:
                # Token retrieval failed, display error message
                st.error(f"Token retrieval failed with status code {response.status_code}: {response.text}")
                st.write(f"Response Headers: {response.headers}")
                st.write(f"Response Content: {response.content}")

# Display user info if authenticated or success flag is present in the URL
if is_authenticated or st.experimental_get_query_params().get("success") == "true":
    st.sidebar.info("You are logged in with Orcid.")

    # Display success message
    st.success("Successfully logged in with Orcid!")

    # Your existing Streamlit content goes here
    st.title('Your uploaded files')
    st.write('A simply filtered table with your uploaded datasets, with a number of editing options: update, delete (restricted!)')

    # Hide the "Login with Orcid" button after successful login
    st.markdown("<style>div[data-testid='stButton']>button {display: none;}</style>", unsafe_allow_html=True)
