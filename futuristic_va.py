import streamlit as st
import time, os, base64, random
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv

# ----------------------------
# Load API key
# ----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="FahimAI - Age-Aware Virtual Assistant", layout="centered")

# Splash / intro
if "launched" not in st.session_state:
    st.session_state["launched"] = False
if not st.session_state["launched"]:
    st.markdown("""
        <div style='text-align:center; padding:80px;'>
            <h1 style='font-size:50px; color:#1976D2;'>🧠 FahimAI</h1>
            <h3 style='color:#555;'>The Age-Aware Virtual Assistant for the UAE Workforce</h3>
            <p>Developed by <b>Renella Andrade</b> | MSc Data Science & AI (UCAM, 2025)</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Launch FahimAI"):
        with st.spinner("Starting assistant..."):
            time.sleep(1.5)
        st.session_state["launched"] = True
        st.experimental_rerun()
    st.stop()

# ----------------------------
# Sidebar inputs
# ----------------------------
st.sidebar.header("👤 User Profile")
age_group = st.sidebar.selectbox("Select your age group:",
                                 ["18–24","25–34","35–44","45–54","55–64","65 and above"])
purpose = st.sidebar.selectbox("What would you like help with?",
                               ["Productivity","AI Adoption Guidance","Motivation","General Support"])
enable_voice = st.sidebar.checkbox("🔊 Enable Voice Responses", value=False)

# ----------------------------
# Theme by age
# ----------------------------
def style_by_age(a):
    if a in ["18–24","25–34"]:
        return {"grad":"linear-gradient(to bottom right,#E3F2FD,#BBDEFB)",
                "accent":"#0D47A1","font":"'Poppins',sans-serif","icon":"🌟","tone":"friendly"}
    elif a in ["35–44","45–54"]:
        return {"grad":"linear-gradient(to bottom right,#E8F5E9,#C8E6C9)",
                "accent":"#2E7D32","font":"'Segoe UI',sans-serif","icon":"💼","tone":"balanced"}
    else:
        return {"grad":"linear-gradient(to bottom right,#E1BEE7,#D1C4E9)",
                "accent":"#4A148C","font":"'Georgia',serif","icon":"🎓","tone":"professional"}

theme = style_by_age(age_group)
st.markdown(f"""
<style>
.main {{background:{theme['grad']};font-family:{theme['font']};}}
h1,h2,h3,h4,h5,h6{{color:{theme['accent']};text-shadow:1px 1px 2px #999;}}
.stTextInput input{{border:2px solid {theme['accent']};border-radius:10px;}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# GPT response via Responses API
# ----------------------------
def fahimai_gpt_response(prompt, tone):
    try:
        tone_note = {
            "friendly": "Use warm, positive, emoji-friendly phrasing.",
            "balanced": "Use clear, professional but conversational language.",
            "professional": "Use formal, concise business language."
        }[tone]

        full_input = f"You are FahimAI, an age-aware UAE assistant. {tone_note}\nUser: {prompt}"

        r = client.responses.create(
            model="gpt-4o-mini",     # or gpt-3.5-turbo if your key supports
            input=full_input,
            temperature=0.8,
            max_output_tokens=250
        )
        return r.output_text.strip()
    except Exception as e:
        return f"⚠️ GPT error: {e}"

# ----------------------------
# Chat UI
# ----------------------------
st.subheader(f"{theme['icon']} Chat with FahimAI")
if "history" not in st.session_state: st.session_state["history"] = []

user_input = st.text_input("Type your question or task:")
if st.button("Ask FahimAI"):
    if user_input.strip():
        with st.spinner("FahimAI is thinking... 🤔"):
            time.sleep(1.2)
        reply = fahimai_gpt_response(user_input, theme["tone"])
        st.session_state["history"].extend([("You", user_input), ("FahimAI", reply)])

        if enable_voice:
            tts = gTTS(reply)
            tts.save("voice.mp3")
            with open("voice.mp3","rb") as f:
                audio = base64.b64encode(f.read()).decode()
            st.markdown(f"<audio autoplay controls src='data:audio/mp3;base64,{audio}'></audio>", unsafe_allow_html=True)
            os.remove("voice.mp3")
    else:
        st.warning("Please enter a message.")

for sender,msg in st.session_state["history"]:
    color = "#fff" if sender=="You" else "#FDFEFE"
    border = "none" if sender=="You" else f"5px solid {theme['accent']}"
    st.markdown(f"<div style='padding:10px;background:{color};border-left:{border};border-radius:8px;margin:5px;'><b>{theme['icon'] if sender!='You' else '👤'} {sender}:</b> {msg}</div>", unsafe_allow_html=True)

# ----------------------------
# Feedback
# ----------------------------
st.markdown("---")
st.markdown("#### Was this response helpful?")
c1,c2 = st.columns(2)
with c1:
    if st.button("👍 Yes"): st.info("Thank you! FahimAI appreciates your feedback.")
with c2:
    if st.button("👎 No"): st.error("Got it. FahimAI will work on being more helpful!")
st.caption("FahimAI adapts tone and interface by age group — demonstrating inclusive AI design.")
