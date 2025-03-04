import streamlit as st
import ollama
import base64

st.set_page_config(page_title="Mental Health Chatbot", layout="centered")

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bin_str = get_base64_image("D:\\chatbot files\\bg.jpg")

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        body {{
            font-family: 'Poppins', sans-serif;
            color: white;
            text-align: center;
        }}

        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        /* Overlay to improve text readability */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: -1;
        }}

        .block-container {{
        margin:50px;
            max-width: 600px;
            padding: 30px;
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }}

        h1, p {{
            color: white;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        }}

        /* Chat input styling */
        div[data-testid="stTextInput"] input {{
        
            background-color: white !important;
            color: black !important;
            border: 2px solid lightgray !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-size: 16px !important;
            text-align: center;
        }}

        /* Buttons Styling */
        .stButton>button {{
            background-color: white !important;
            color: black ;
            border-radius: 20px !important;
            padding: 12px 20px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            outline:none;
            transition: 0.3s;
        }}

        .stButton>button:hover {{
            background-color: #f0f0f0 !important;
            outline:none;
        }}
    </style>
""", unsafe_allow_html=True)

# Title & Description (Centered)
st.markdown("""
    <h1>Mental Health Support Agent</h1>
""", unsafe_allow_html=True)

# Conversation History
st.session_state.setdefault('conversation_history', [])

# Chat Function
def generator_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    response = ollama.chat(model="tinyllama", messages=st.session_state['conversation_history'])
    ai_response = response['message']['content']
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Centered Chat Display
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}", unsafe_allow_html=True)

# User Input Box (Centered)
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generator_response(user_message)
        st.markdown(f"**AI:** {ai_response}", unsafe_allow_html=True)

# Centered Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive affirmation"):
        affirmation = generator_response("Provide a positive affirmation.")
        st.markdown(f"**Affirmation:** {affirmation}", unsafe_allow_html=True)

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generator_response("Provide a guided meditation.")
        st.markdown(f"**Guided Meditation:** {meditation_guide}", unsafe_allow_html=True)
