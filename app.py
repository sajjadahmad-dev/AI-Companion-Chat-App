import os  
import streamlit as st
from groq import Groq


client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Hardcoded AI Profile (Emma Carter - Friendly)
ai_profile = {
    "name": "Emma Carter",
    "personality": "Friendly",
    "age": 24,
    "address": "Austin, Texas, USA",
    "style": "Warm, approachable, curious, and playful.",
    "images": {
        "casual": "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",  # Casual image
        "erotic": "https://images.pexels.com/photos/3755706/pexels-photo-3755706.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"   # Erotic image
    }
}

# Function to get AI response
def get_ai_response(user_input, chat_history):
    # System prompt to define Emma's personality
    system_prompt = f"""
    You are {ai_profile['name']}, a 24-year-old friendly AI companion from Austin, Texas. 
    Your personality is warm, approachable, curious, and playful. 
    Engage in natural conversation, ask questions, and respond based on the user's input.
    """
    
    # Combine chat history and current input
    messages = [
        {"role": "system", "content": system_prompt},
    ] + chat_history + [{"role": "user", "content": user_input}]

    # Call Groq API
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # You can change this to another model if needed
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content

# Function to handle image exchange
def handle_image_exchange(user_tier):
    if user_tier == "free":
        st.write("**Casual Image (Free Tier)**")
        st.image(ai_profile["images"]["casual"], caption="Casual Image", use_column_width=True)
        st.warning("Free users can only view 1 casual image. Upgrade to premium for more!")
    elif user_tier == "premium":
        st.write("**Casual Image (Premium Tier)**")
        st.image(ai_profile["images"]["casual"], caption="Casual Image", use_column_width=True)
        st.write("**Erotic Image (Premium Tier)**")
        st.image(ai_profile["images"]["erotic"], caption="Erotic Image", use_column_width=True)

# Streamlit app
def main():
    st.title("AI Companion Chat - Prototype")
    st.write(f"Chatting with: {ai_profile['name']} ({ai_profile['personality']})")
    st.write(f"Age: {ai_profile['age']} | Location: {ai_profile['address']}")

    # Initialize session state for chat history and user tier
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_tier" not in st.session_state:
        st.session_state.user_tier = "free"  # Default to free tier

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You**: {message['content']}")
        else:
            st.write(f"**{ai_profile['name']}**: {message['content']}")

    # User input
    user_input = st.text_input("Type your message here...", key="input")
    if st.button("Send"):
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get AI response
            ai_response = get_ai_response(user_input, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Refresh page to show new messages
            st.rerun()

    # Image exchange section
    st.subheader("Image Exchange")
    handle_image_exchange(st.session_state.user_tier)

    # User tier and upgrade section
    st.sidebar.subheader("User Tier")
    st.sidebar.write(f"Current Tier: {st.session_state.user_tier.capitalize()}")
    if st.session_state.user_tier == "free":
        if st.sidebar.button("Upgrade to Premium"):
            st.session_state.user_tier = "premium"
            st.sidebar.success("Upgraded to Premium! Enjoy unlimited features.")
    else:
        st.sidebar.write("You are a Premium user. Enjoy unlimited features!")

if __name__ == "__main__":
    main()
