import streamlit as st
import time, random, os, base64
from gtts import gTTS

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(page_title="FahimAI - Age-Aware Virtual Assistant", layout="centered")

# ----------------------------
# SPLASH / INTRO PAGE
# ----------------------------
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
        st.rerun()
    st.stop()

# ----------------------------
# SIDEBAR INPUT
# ----------------------------
st.sidebar.header("👤 User Profile")
age_group = st.sidebar.selectbox("Select your age group:",
                                 ["18–24","25–34","35–44","45–54","55–64","65 and above"])
purpose = st.sidebar.selectbox("What would you like help with?",
                               ["Productivity","AI Adoption Guidance","Motivation","General Support"])
enable_voice = st.sidebar.checkbox("🔊 Enable Voice Responses", value=False)

# ----------------------------
# STYLE BY AGE
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
# SMART LOCAL RESPONSE ENGINE
# ----------------------------
def fahimai_response(user_input, tone):
    text = user_input.lower()
    if any(w in text for w in ["motivate","encourage","tired","lazy","demotivated","burnout"]):
        intent = "motivation"
    elif any(w in text for w in ["ai","assistant","automation","artificial intelligence"]):
        intent = "ai"
    elif any(w in text for w in ["productivity","focus","task","work","time management","deadline"]):
        intent = "productivity"
    elif any(w in text for w in ["stress","mental","anxious","relax"]):
        intent = "wellbeing"
    else:
        intent = "general"

    responses = {
        "motivation": {
            "friendly": ["🌟 You’re doing amazing — every small step counts!","✨ Keep going, your consistency matters!"],
            "balanced": ["Progress builds gradually — focus on steady effort.","Stay consistent and believe in your process."],
            "professional": ["Resilience defines leadership. Stay composed and move forward.","Challenges refine capability; maintain focus."]
        },
        "ai": {
            "friendly": ["🤖 AI can help you simplify tasks and boost creativity!","AI is your digital teammate — explore, learn, grow!"],
            "balanced": ["AI improves productivity and decision-making when used responsibly.","Adopting AI gradually ensures confident integration."],
            "professional": ["AI supports strategic efficiency and informed decision-making.","Responsible AI use enhances performance across industries."]
        },
        "productivity": {
            "friendly": ["💪 Try short focus sprints with breaks — it works wonders!","🚀 Start with one major goal and celebrate small wins."],
            "balanced": ["Plan your day with priorities — clarity boosts productivity.","Avoid multitasking; single-tasking enhances quality."],
            "professional": ["Structured scheduling and delegation improve outcomes.","Strategic focus ensures timely delivery and accountability."]
        },
        "wellbeing": {
            "friendly": ["🌸 Take a pause — your wellbeing fuels success!","🧘 Deep breath. Rest helps you reset and recharge."],
            "balanced": ["Balance and composure sustain performance.","A short pause can restore focus and mental clarity."],
            "professional": ["Wellbeing underpins sustainable performance.","Balanced routines support sound decision-making."]
        },
        "general": {
            "friendly": ["Hey there 👋 How can I help you today?","Tell me more — happy to assist!"],
            "balanced": ["I’m here to support with productivity or AI insights.","Please share your question for tailored advice."],
            "professional": ["Good day. How may I assist with your inquiry?","Please provide context so I can offer structured guidance."]
        }
    }
    return random.choice(responses[intent][tone])

# ----------------------------
# CHAT INTERFACE
# ----------------------------
st.subheader(f"{theme['icon']} Chat with FahimAI")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Type your question or task:")

if st.button("Ask FahimAI"):
    if user_input.strip():
        with st.spinner("FahimAI is thinking... 🤔"):
            time.sleep(1)
        reply = fahimai_response(user_input, theme["tone"])
        st.session_state["history"].append(("You", user_input))
        st.session_state["history"].append(("FahimAI", reply))

        if enable_voice:
            tts = gTTS(reply)
            tts.save("voice.mp3")
            with open("voice.mp3","rb") as f:
                audio = base64.b64encode(f.read()).decode()
            st.markdown(f"<audio autoplay controls src='data:audio/mp3;base64,{audio}'></audio>", unsafe_allow_html=True)
            os.remove("voice.mp3")
    else:
        st.warning("Please enter a question.")

for sender,msg in st.session_state["history"]:
    color = "#fff" if sender=="You" else "#FDFEFE"
    border = "none" if sender=="You" else f"5px solid {theme['accent']}"
    st.markdown(f"<div style='padding:10px;background:{color};border-left:{border};border-radius:8px;margin:5px;'><b>{theme['icon'] if sender!='You' else '👤'} {sender}:</b> {msg}</div>", unsafe_allow_html=True)

# ----------------------------
# FEEDBACK
# ----------------------------
st.markdown("---")
st.markdown("#### Was this response helpful?")
c1,c2 = st.columns(2)
with c1:
    if st.button("👍 Yes"): st.info("Thank you! FahimAI appreciates your feedback.")
with c2:
    if st.button("👎 No"): st.error("Got it. FahimAI will try to improve!")
st.caption("FahimAI adapts tone and visuals by age group — demonstrating inclusive, accessible AI design.")


