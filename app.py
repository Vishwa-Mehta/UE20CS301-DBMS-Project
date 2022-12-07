import streamlit as st
from backend.database import check_login, add_login

def main():
    st.title("Inventory Management System")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Login")
        email0 = st.text_input("Email: ")
        password0 = st.text_input("Password: ", type = "password")
        if st.button("Login"):
            check_login(email0, password0)
    with col2:
        st.subheader("SignUp:")
        fname = st.text_input("First Name:")
        lname = st.text_input("Last Name")
        email = st.text_input("Email:")
        password = st.text_input("Password:", type = "password")
        if st.button("Signup"):
            add_login(fname, lname, email, password)

if __name__ == '__main__':
    main()
