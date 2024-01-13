import streamlit as st
from requests.auth import HTTPBasicAuth
import requests

# Orcid Auth
CLIENT_ID = st.secrets["Orcid_ID"]
CLIENT_SECRET = st.secrets["Orcid_Secret"]
#REDIRECT_URI = "https://orcid-app-u9tbyykcsuwozua46jf3hk.streamlit.app/"
REDIRECT_URI = "https://geo-cosmo-data-sharing-platform-bvniuih82j6l2aeq3jxfyb.streamlit.app/"
ORCID_API_URL = "https://pub.orcid.org/v3.0/"

# Function to get Orcid token
def get_orcid_token(authorization_response):
    token_url = "https://orcid.org/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_response,
        "redirect_uri": REDIRECT_URI,
    }
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.post(token_url, data=token_data, auth=auth)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

# Function to get Orcid user info
def get_orcid_user_info(orcid_token):
    if not orcid_token:
        return None

    headers = {"Authorization": f"Bearer {orcid_token}"}
    response = requests.get(ORCID_API_URL + "me", headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return {
            "name": user_info.get("name", {}).get("given-names", {}).get("value", ""),
            "orcid": user_info.get("orcid-identifier", {}).get("path", ""),
        }
    else:
        return None

# Streamlit app
st.title("Streamlit Orcid Authentication")
st.write('test 2')

# Check if the user is authenticated
st.session_state.is_authenticated = False #st.session_state.get("is_authenticated", False)

if not st.session_state.is_authenticated:
    # Orcid login button
    if st.button("Login with Orcid"):
        # Redirect user to Orcid for authorization
        authorization_url = f"https://orcid.org/oauth/authorize?client_id={CLIENT_ID}&response_type=code&scope=/authenticate&redirect_uri={REDIRECT_URI}"
        st.write(f"Click [here]({authorization_url}) to log in with Orcid.")

        # Check if the authorization code is present in the URL
        url = st.experimental_get_query_params() # should soon be: st.query_params()
        authorization_response = url.get("code", None)

        if authorization_response:
            # Get Orcid token
            orcid_token = get_orcid_token(authorization_response)

            if orcid_token:
                st.session_state.is_authenticated = True
                st.session_state.orcid_token = orcid_token
                st.success("Successfully logged in with Orcid!")


if st.sidebar.button('Logout'):
    st.session_state.is_authenticated = False


# Display user info if authenticated
if st.session_state.is_authenticated:
    st.sidebar.success("You are logged in with ORCID")

    # Display Orcid user info automatically
    orcid_user_info = get_orcid_user_info(st.session_state.orcid_token)
    if orcid_user_info:
        st.write("Orcid User Information:")
        st.write(f"Name: {orcid_user_info['name']}")
        st.write(f"Orcid ID: {orcid_user_info['orcid']}")

    # Your existing Streamlit content goes here
    st.title('Your uploaded files')
    st.write('A simply filtered table with your uploaded datasets, with a number of editing options: update, delete (restricted!)')
    st.write('orcid_user_info', orcid_user_info)
    st.write('st.session_state.orcid_token',t.session_state.orcid_token)
else:
    st.sidebar.info('not logged in')
    st.sidebar.error('You are not loged in to ORCID')