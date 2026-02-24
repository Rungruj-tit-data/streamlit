import streamlit as st
import uuid
import time

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SVI AI Platform",
    page_icon="🤖",
    layout="wide"
)

# ─────────────────────────────────────────────
# Agent Definitions
# ─────────────────────────────────────────────
AGENTS = {
    "Dashy": {
        "label": "🥰 Dashy",
        "emoji": "🥰",
        "desc": "Your data-driven dashboard analyst. Great for KPIs, trends, and insights."
    },
    "Lexi": {
        "label": " 😁 Lexi",
        "emoji": "😁",
        "desc": "Your legal AI assistant. Specialized in contract comparison & risk review."
    }
}

# ─────────────────────────────────────────────
# Init Session State
# ─────────────────────────────────────────────
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    new_id = str(uuid.uuid4())[:8]
    st.session_state.sessions[new_id] = []
    st.session_state.current_session = new_id

if "agent" not in st.session_state:
    st.session_state.agent = "Dashy"

if "interrupt" not in st.session_state:
    st.session_state.interrupt = False

# ─────────────────────────────────────────────
# Sidebar (Sessions)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💬 Sessions")

    if st.button("➕ Start New Session", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        st.session_state.sessions[new_id] = []
        st.session_state.current_session = new_id
        st.session_state.interrupt = False
        st.rerun()

    st.divider()

    for sid in st.session_state.sessions.keys():
        if st.button(f"🗂 Session {sid}", use_container_width=True):
            st.session_state.current_session = sid
            st.session_state.interrupt = False
            st.rerun()

# ─────────────────────────────────────────────
# Top Header (No Emoji)
# ─────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("# SVI AI Platform")
    st.caption("Multi-Agent Conversational Platform")

with col2:
    selected_label = st.selectbox(
        "Choose Agent",
        [AGENTS[a]["label"] for a in AGENTS]
    )

    # Map label back to agent key
    for key, value in AGENTS.items():
        if value["label"] == selected_label:
            st.session_state.agent = key
            break

agent_info = AGENTS[st.session_state.agent]

st.markdown(
    f"""
    ### {agent_info['emoji']} {st.session_state.agent}
    *{agent_info['desc']}*
    """
)

st.divider()

# ─────────────────────────────────────────────
# Chat Display
# ─────────────────────────────────────────────
current_chat = st.session_state.sessions[st.session_state.current_session]

for msg in current_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# Interrupt Scenario
# ─────────────────────────────────────────────
if st.session_state.interrupt:
    with st.chat_message("assistant"):
        st.markdown("📎 **I detected a file reference (JPG/PDF).**")
        st.markdown("Would you like me to compare it with SVI standard?")

        col1, col2 = st.columns(2)

        if col1.button("✅ Yes, Compare"):
            current_chat.append({
                "role": "assistant",
                "content": "🔍 Starting intelligent contract comparison..."
            })
            st.session_state.interrupt = False
            st.rerun()

        if col2.button("❌ No, Continue Chat"):
            current_chat.append({
                "role": "assistant",
                "content": "👍 Got it. Continuing our conversation."
            })
            st.session_state.interrupt = False
            st.rerun()

# ─────────────────────────────────────────────
# Chat Input
# ─────────────────────────────────────────────
user_input = st.chat_input("💬 Type a message or paste JPG/PDF reference...")

if user_input:
    current_chat.append({
        "role": "user",
        "content": user_input
    })

    # Trigger interrupt
    if "JPG" in user_input.upper() or "PDF" in user_input.upper():
        st.session_state.interrupt = True
        st.rerun()

    # Mock response
    with st.spinner("🧠 Thinking..."):
        time.sleep(1)

    response = f"{agent_info['emoji']} **{st.session_state.agent}** says:\n\nYou said: `{user_input}`"

    current_chat.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

    # streamlit run demo_ui_v2.py