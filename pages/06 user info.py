import streamlit as st

# Display user info if authenticated
if st.session_state.is_authenticated:
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
