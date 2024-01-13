import streamlit as st

st.title('Your uploaded files')

st.write('A simply filtered table with your uploaded datasets, with a number of editing options: update, delete (restricted!)')

if st.session_state.is_authenticated:
    st.sidebar.success("You are logged in with ORCID")
else:
    st.sidebar.success("ORCID login required for full functionality")
