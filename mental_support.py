import streamlit as st
import ollama
import base64
st.set_page_config(page_title="Mental Health Chatbot")


def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("D:\\chatbot files\\bg.jpg")


st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
""", unsafe_allow_html=True)


# Initialize conversation history
st.session_state.setdefault('conversation_history', [])

def generator_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

#    
    response = ollama.chat(model="tinyllama", messages=st.session_state['conversation_history'])
    ai_response = response['message']['content']

#     # Correct role for AI response
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# App title
st.title(" Mental Health Support Agent")

# # Display conversation history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# # User input
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generator_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# # Two buttons for affirmations and meditation
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")