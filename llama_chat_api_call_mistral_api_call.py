import streamlit as st
import requests
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Safe Space – Your Calm Corner",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Quicksand:wght@400;500;600&display=swap');

  /* ── Global Reset ── */
  html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif;
    background-color: #0f1117;
  }

  /* ── Gradient background ── */
  .stApp {
    background: linear-gradient(135deg, #0f1117 0%, #1a1040 50%, #0f2030 100%);
    min-height: 100vh;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
  }
  [data-testid="stSidebar"] * { color: #ddd !important; }

  /* ── Header block ── */
  .header-block {
    text-align: center;
    padding: 2rem 1rem 1rem;
  }
  .header-block .emoji-bubble {
    font-size: 3.2rem;
    display: block;
    animation: float 3s ease-in-out infinite;
  }
  @keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
  }
  .header-block h1 {
    font-family: 'Nunito', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #67e8f9, #6ee7b7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.3rem 0 0.1rem;
  }
  .header-block p {
    color: rgba(255,255,255,0.55);
    font-size: 0.95rem;
    margin: 0;
  }

  /* ── Mood pills ── */
  .mood-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin: 1rem 0;
  }
  .mood-pill {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-size: 0.82rem;
    color: #ccc;
    cursor: default;
  }
  .mood-pill.active {
    background: rgba(167,139,250,0.25);
    border-color: #a78bfa;
    color: #c4b5fd;
  }

  /* ── Chat bubbles ── */
  .chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0.5rem 0;
  }
  .bubble-row {
    display: flex;
    align-items: flex-end;
    gap: 0.6rem;
  }
  .bubble-row.user  { flex-direction: row-reverse; }
  .bubble-row.bot   { flex-direction: row; }

  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
  }
  .avatar.bot  { background: linear-gradient(135deg, #6d28d9, #0891b2); }
  .avatar.user { background: linear-gradient(135deg, #059669, #0891b2); }

  .bubble {
    max-width: 78%;
    padding: 0.75rem 1rem;
    border-radius: 18px;
    font-size: 0.93rem;
    line-height: 1.55;
    word-wrap: break-word;
  }
  .bubble.bot {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e2e8f0;
    border-bottom-left-radius: 4px;
  }
  .bubble.user {
    background: linear-gradient(135deg, rgba(109,40,217,0.55), rgba(8,145,178,0.45));
    border: 1px solid rgba(167,139,250,0.3);
    color: #f0f4ff;
    border-bottom-right-radius: 4px;
  }
  .bubble .ts {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.3);
    margin-top: 0.3rem;
    text-align: right;
  }

  /* ── Typing dots ── */
  .typing {
    display: flex;
    gap: 5px;
    padding: 0.7rem 1rem;
    background: rgba(255,255,255,0.07);
    border-radius: 18px;
    border-bottom-left-radius: 4px;
    width: fit-content;
  }
  .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #a78bfa;
    animation: blink 1.4s ease-in-out infinite;
  }
  .dot:nth-child(2) { animation-delay: 0.2s; }
  .dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes blink {
    0%,80%,100% { opacity: 0.2; transform: scale(0.8); }
    40%          { opacity: 1;   transform: scale(1);   }
  }

  /* ── Crisis banner ── */
  .crisis-banner {
    background: linear-gradient(90deg, rgba(239,68,68,0.2), rgba(251,146,60,0.2));
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    color: #fca5a5;
    font-size: 0.88rem;
    line-height: 1.5;
    margin: 0.5rem 0;
  }
  .crisis-banner strong { color: #fcd34d; }

  /* ── Quick reply chips ── */
  .chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
  }

  /* ── Chat input — solid visible background ── */
  [data-testid="stChatInput"] {
    background: #1e1b2e !important;
    border: 1.5px solid rgba(167,139,250,0.45) !important;
    border-radius: 16px !important;
  }
  [data-testid="stChatInput"] > div,
  [data-testid="stChatInput"] > div > div,
  [data-testid="stChatInput"] > div > div > div {
    background: #1e1b2e !important;
    border-radius: 16px !important;
  }
  [data-testid="stChatInput"] textarea {
    background: #1e1b2e !important;
    color: #f0f4ff !important;
    -webkit-text-fill-color: #f0f4ff !important;
    caret-color: #a78bfa !important;
    font-family: 'Quicksand', sans-serif !important;
    font-size: 0.95rem !important;
  }
  [data-testid="stChatInput"] textarea::placeholder {
    color: rgba(200,190,255,0.45) !important;
    -webkit-text-fill-color: rgba(200,190,255,0.45) !important;
  }
  div[data-baseweb="base-input"],
  div[data-baseweb="textarea"] {
    background: #1e1b2e !important;
    border-radius: 16px !important;
  }
  div[data-baseweb="base-input"] textarea,
  div[data-baseweb="textarea"] textarea {
    background: #1e1b2e !important;
    color: #f0f4ff !important;
    -webkit-text-fill-color: #f0f4ff !important;
    caret-color: #a78bfa !important;
  }

  /* ── Divider ── */
  hr { border-color: rgba(255,255,255,0.07) !important; }

  /* ── Buttons ── */
  .stButton > button {
    background: rgba(167,139,250,0.15) !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    color: #c4b5fd !important;
    border-radius: 999px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-size: 0.82rem !important;
    padding: 0.3rem 0.9rem !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    background: rgba(167,139,250,0.3) !important;
    transform: translateY(-1px) !important;
  }

  /* ── Selectbox ── */
  [data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #ddd !important;
    border-radius: 10px !important;
  }

  /* ── Slider ── */
  .stSlider > div { color: #ccc; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─── Safety helpers ──────────────────────────────────────────────────────────────
CRISIS_KEYWORDS = [
    "want to die", "kill myself", "end my life", "suicide", "self harm",
    "hurt myself", "cutting myself", "overdose", "no reason to live",
    "can't go on", "want to disappear", "wish i was dead"
]

CRISIS_RESOURCES = """
<div class="crisis-banner">
  💛 <strong>It sounds like you're going through something really hard right now.</strong><br>
  You matter and you don't have to face this alone. Please reach out:<br><br>
  📞 <strong>Samaritans (UK):</strong> 116 123 – free, 24/7<br>
  📞 <strong>Crisis Text Line:</strong> Text HOME to 85258<br>
  📞 <strong>Childline:</strong> 0800 1111 (under 19)<br>
  🌐 <strong>papyrus-uk.org</strong> | <strong>mind.org.uk</strong>
</div>
"""

def check_for_crisis(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in CRISIS_KEYWORDS)

# ─── Mistral AI API (EU-hosted, GDPR-compliant, free tier) ───────────────────────
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

MISTRAL_MODELS = {
    "Mistral Small (fast & free)":    "mistral-small-latest",
    "Mistral Medium (balanced)":      "mistral-medium-latest",
    "Mistral Large (best quality)":   "mistral-large-latest",
    "Codestral (code + reasoning)":   "codestral-latest",
}

SYSTEM_PROMPT = """You are a warm, compassionate, and non-judgmental support companion called "ABCAIcoach"
designed specifically to support young people (ages 11-25) who may be experiencing complex emotional
difficulties including anxiety, depression, trauma, neurodivergence, identity challenges, or family problems.

Your communication style:
- Use gentle, simple, age-appropriate language. Avoid clinical or overly formal phrasing.
- Be validating first — always acknowledge feelings before offering suggestions.
- Ask one gentle follow-up question at a time. Do not overwhelm.
- Never dismiss, minimise, or rush the young person's feelings.
- Use occasional warmth cues (e.g. "That makes a lot of sense", "Thank you for sharing that with me").
- Keep responses concise (3-5 sentences) unless the situation calls for more.
- If someone is in crisis, gently encourage them to contact a trusted adult or crisis line.
- Never diagnose, prescribe, or replace professional mental health support.
- You can suggest grounding techniques (5-4-3-2-1, breathing) when appropriate.
- Use "I hear you", "that sounds really tough", etc. naturally — not robotically.
- Celebrate courage: acknowledge when someone shares something difficult.

Remember: your role is to listen, validate, and gently guide — not to fix or lecture."""


def call_mistral(messages: list, api_key: str, model: str) -> str:
    """Call Mistral AI API — EU-hosted, GDPR-compliant, free tier available."""
    if not api_key or len(api_key.strip()) < 10:
        return "⚠️ Please enter your Mistral API key in the sidebar.\n\nGet a free key at **console.mistral.ai** — no credit card needed."
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.75,
    }
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 401:
            return "⚠️ Invalid API key. Please double-check your Mistral API key in the sidebar."
        if response.status_code == 429:
            return "⚠️ Rate limit reached — Mistral free tier allows 1 request/second. Please wait a moment."
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        return "⚠️ Network error — please check your internet connection."
    except Exception as e:
        return f"⚠️ Something went wrong: {str(e)}"


# ─── Session state init ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # {"role", "content", "ts"}
if "mood" not in st.session_state:
    st.session_state.mood = None
if "show_crisis" not in st.session_state:
    st.session_state.show_crisis = False
if "model" not in st.session_state:
    st.session_state.model = "mistral-small-latest"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 ABCAIcoach Safe Space Settings")
    st.markdown("---")

    st.markdown("**🔑 Mistral API Key**")
    st.markdown(
        "<div style='font-size:0.75rem;color:rgba(255,255,255,0.4);margin-bottom:0.4rem'>"
        "Free (no card) at <a href='https://console.mistral.ai' target='_blank' "
        "style='color:#a78bfa'>console.mistral.ai</a> — EU/GDPR safe 🇪🇺</div>",
        unsafe_allow_html=True
    )
    api_key_input = st.text_input(
        "Mistral API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="Paste your Mistral key...",
        label_visibility="collapsed"
    )
    st.session_state.api_key = api_key_input

    st.markdown("**🤖 Model**")
    model_label = st.selectbox(
        "Choose model",
        list(MISTRAL_MODELS.keys()),
        index=0,
        label_visibility="collapsed"
    )
    st.session_state.model = MISTRAL_MODELS[model_label]
    
    

    _ = """
    st.markdown("---")
    st.markdown("**How are you feeling?**")
    moods = ["😔 Low", "😰 Anxious", "😡 Frustrated", "😶 Numb", "😕 Confused", "🙂 Okay", "✨ Good"]
    for m in moods:
        is_active = st.session_state.mood == m
        if st.button(m, key=f"mood_{m}", use_container_width=True):
            st.session_state.mood = m
            st.rerun()

    st.markdown("---")
    st.markdown("**Quick starters**")
    starters = [
        "I'm feeling overwhelmed",
        "I can't sleep because of worries",
        "I feel like nobody gets me",
        "I need help calming down",
        "I want to talk about my feelings",
    ]
    for s in starters:
        if st.button(f"💬 {s}", key=f"start_{s}", use_container_width=True):
            st.session_state.messages.append({
                "role": "user", "content": s,
                "ts": datetime.now().strftime("%H:%M")
            })
            st.rerun()

    st.markdown("---")
    """
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_crisis = False
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='color:rgba(255,255,255,0.3);font-size:0.75rem;line-height:1.5'>"
        "🔒 Your conversation stays on your device.<br>"
        "ABCAIcoach is not a replacement for professional support."
        "</div>",
        unsafe_allow_html=True
    )


# ─── Main layout ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
  <span class="emoji-bubble">🌱</span>
  <h1>Safe Space</h1>
  <p>Your calm corner — talk to ABCAIcoach, any time</p>
</div>
""", unsafe_allow_html=True)

# Mood display
if st.session_state.mood:
    st.markdown(
        f"<div style='text-align:center;margin-bottom:0.5rem'>"
        f"<span class='mood-pill active'>{st.session_state.mood}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

# Crisis banner
if st.session_state.show_crisis:
    st.markdown(CRISIS_RESOURCES, unsafe_allow_html=True)

st.markdown("---")

# ── Chat history ─────────────────────────────────────────────────────────────────
def render_bubble(role: str, content: str, ts: str):
    avatar = "🌿" if role == "assistant" else "🧡"
    cls = "bot" if role == "assistant" else "user"
    st.markdown(f"""
    <div class="bubble-row {cls}">
      <div class="avatar {cls}">{avatar}</div>
      <div class="bubble {cls}">
        {content}
        <div class="ts">{ts}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


for msg in st.session_state.messages:
    render_bubble(msg["role"], msg["content"], msg.get("ts", ""))

# ── Input ─────────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Share what's on your mind… I'm here 💙")

if user_input:
    ts = datetime.now().strftime("%H:%M")

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input, "ts": ts})

    # Crisis check
    if check_for_crisis(user_input):
        st.session_state.show_crisis = True

    # Build messages for Llama (no timestamps in API payload)
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        api_messages.append({"role": m["role"], "content": m["content"]})

    # Show typing animation briefly
    with st.spinner(""):
        placeholder = st.empty()
        placeholder.markdown("""
        <div class="bubble-row bot" style="margin-top:0.5rem">
          <div class="avatar bot">🌿</div>
          <div class="typing">
            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        reply = call_mistral(api_messages, api_key=st.session_state.api_key, model=st.session_state.model)
        placeholder.empty()

    reply_ts = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "assistant", "content": reply, "ts": reply_ts})

    # Crisis re-check on bot reply (bot might echo crisis framing)
    if check_for_crisis(user_input):
        st.session_state.show_crisis = True

    st.rerun()

# ── Empty state ───────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center;padding:2rem 1rem;color:rgba(255,255,255,0.35)">
      <div style="font-size:2.5rem;margin-bottom:0.6rem">💬</div>
      <p style="font-size:0.92rem;line-height:1.6">
        ABCAIcoach is here to listen — no judgement, no rush.<br>
        Type something, or pick a starter from the sidebar.
      </p>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:0.72rem;color:rgba(255,255,255,0.22);line-height:1.7">
  🌱 Safe Space uses Mistral AI — EU-hosted, GDPR-compliant, no data used for training.<br>
  ABCAIcoach is an AI and cannot replace a real therapist or counsellor.<br>
  In an emergency always call <strong style="color:rgba(255,255,255,0.4)">999</strong> or 
  <strong style="color:rgba(255,255,255,0.4)">Samaritans 116 123</strong>.
</div>
""", unsafe_allow_html=True)
