import streamlit as st
import joblib
import json
import os

# Set page config (must be first Streamlit command)
st.set_page_config(page_title="SMS Spam Detector", layout="wide")

# Light bluish and cement-like CSS with classy navigation bar
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f4f8;
        }
        .navbar {
            background-color: #007acc;
            padding: 10px 30px;
            border-radius: 10px;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
        .navbar a {
            color: white;
            padding: 0 15px;
            text-decoration: none;
            font-weight: bold;
        }
        .navbar a:hover {
            text-decoration: underline;
        }
        div.stButton > button {
            background-color: #007acc;
            color: white;
            padding: 0.5em 1em;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }
        textarea, input[type="text"], input[type="password"] {
            background-color: #ffffff !important;
            border: 1px solid #b3d1ff !important;
            padding: 8px;
            border-radius: 5px;
        }
        section[data-testid="stSidebar"] > div:first-child {
            background-color: #dfe6ed;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
    <div class="navbar">
        💬 SMS Spam Detector App
    </div>
""", unsafe_allow_html=True)

# Load model and vectorizer
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# User database setup
USER_DB = "users.json"
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

with open(USER_DB, "r") as f:
    users = json.load(f)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Signup function
def signup():
    st.subheader("🆕 Signup")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    if st.button("Signup"):
        if new_user in users:
            st.error("❌ Username already exists.")
        elif new_user == "" or new_pass == "":
            st.warning("Please fill all fields.")
        else:
            users[new_user] = new_pass
            with open(USER_DB, "w") as f:
                json.dump(users, f)
            st.success("✅ Account created! Please login.")

# Login function
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

# Spam detection function
def spam_detector():
    st.subheader("📩 SMS Spam Detector")
    st.write(f"Welcome, *{st.session_state.username}*!")

    message = st.text_area("✉ Enter your SMS message:")
    if st.button("Predict"):
        if not message.strip():
            st.warning("Please enter a message.")
        else:
            vectorized = vectorizer.transform([message])
            prediction = model.predict(vectorized)[0]
            if prediction == "spam" or prediction == 1:
                st.error("🚫 This message is SPAM.")
            else:
                st.success("✅ This message is NOT Spam.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Sidebar navigation
menu = st.sidebar.radio("Navigate", ["Login", "Signup"])

if st.session_state.logged_in:
    spam_detector()
elif menu == "Login":
    login()
else:
    signup()