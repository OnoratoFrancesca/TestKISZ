import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['createHash for password here', ':)']).generate()
print(hashed_passwords)
