import streamlit as st
import cohere
import requests
import os

# ── Setup ──────────────────────────────
st.set_page_config(
    page_title="JARVIS — Manik ka AI",
    page_icon="🤖"
)
API_KEY = os.environ.get("COHERE_API_KEY", "")
co      = cohere.ClientV2(API_KEY)

# ── Weather Tool ───────────────────────
def get_weather(city="Delhi"):
    try:
        r    = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10
        )
        data = r.json()
        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"🌤️ {city}: {temp}°C, {desc}"
    except:
        return "Weather nahi mila"

# ── AI Call ────────────────────────────
def ai_call(prompt):
    try:
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role"   : "system",
                    "content": "Tu JARVIS hai — Manik ka personal AI agent. Hindi/Hinglish mein baat kar! Helpful aur friendly reh!"
                },
                {
                    "role"   : "user",
                    "content": prompt
                }
            ]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"Error: {e}"

# ── UI ─────────────────────────────────
st.title("🤖 JARVIS — Manik ka AI Agent")
st.caption("Koi bhi sawaal poocho — Hindi/Hinglish mein!")

# City input
city = st.text_input("🌤️ Tumhara Sheher", value="Delhi")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhao
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Naya message
if prompt := st.chat_input("Koi bhi sawaal poocho..."):
    
    # User message dikhao
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({
        "role"   : "user",
        "content": prompt
    })
    
    # Weather check
    if any(w in prompt.lower() for w in ["mausam","weather","garmi","thandi"]):
        weather  = get_weather(city)
        full_prompt = f"Weather: {weather}\nUser: {prompt}"
    else:
        full_prompt = prompt
    
    # JARVIS jawab
    with st.chat_message("assistant"):
        with st.spinner("JARVIS soch raha hai..."):
            jawab = ai_call(full_prompt)
        st.write(jawab)
    
    st.session_state.messages.append({
        "role"   : "assistant",
        "content": jawab
    })

# Clear button
if st.button("🗑️ Chat Clear Karo"):
    st.session_state.messages = []
    st.rerun()
