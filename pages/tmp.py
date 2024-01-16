import streamlit as st
from requests.auth import HTTPBasicAuth
import requests

# Orcid Auth
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "https://orcid-app-u9tbyykcsuwozua46jf3hk.streamlit.app/"
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
            # Get Orcid token
            orcid_token = get_orcid_token(authorization_response)

            if orcid_token:
                st.session_state.is_authenticated = True
                st.session_state.orcid_token = orcid_token
                st.success("Successfully logged in with Orcid!")

# Display user info if authenticated
if is_authenticated:
    st.sidebar.info("You are logged in with Orcid.")

    # Display Orcid user info automatically
    orcid_user_info = get_orcid_user_info(st.session_state.orcid_token)
    if orcid_user_info:
        st.write("Orcid User Information:")
        st.write(f"Name: {orcid_user_info['name']}")
        st.write(f"Orcid ID: {orcid_user_info['orcid']}")

    # Your existing Streamlit content goes here
    st.title('Your uploaded files')
    st.write('A simply filtered table with your uploaded datasets, with a number of editing options: update, delete (restricted!)')