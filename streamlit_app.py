import streamlit as st
import time
import os
import tempfile

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    for key, val in st.secrets.items():
        os.environ.setdefault(key, str(val))
except Exception:
    pass



# ─── MUST BE FIRST STREAMLIT CALL ────────────────────────────────────────────
st.set_page_config(
    page_title="MeetFlow - AI Video Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Fonts (link tags, NOT @import) ──────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* ── Root Variables ── */
:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface-2: #1a1a25;
    --border: #2a2a3a;
    --accent: #7c3aed;
    --accent-glow: #9f67ff;
    --accent-2: #06b6d4;
    --text: #e8e8f0;
    --text-muted: #7070a0;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
[data-testid="stAppViewContainer"] { background: var(--bg) !important; }
[data-testid="stMain"]             { background: var(--bg) !important; }
[data-testid="stHeader"]           { background: var(--bg) !important; }

/* Grid background */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(124,58,237,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124,58,237,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Headings ── */
h1,h2,h3,h4,h5,h6 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

/* ── Hero ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 2.5vw, 3rem);
    font-weight: 800; line-height: 1.1; margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 50%, var(--accent-2) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem; color: var(--text-muted);
    letter-spacing: 0.2em; text-transform: uppercase; margin-top: 0.5rem;
}

/* ── Cards ── */
.card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
    position: relative; overflow: hidden; transition: border-color 0.2s;
}
.card:hover { border-color: var(--accent); }
.card::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}
.card-title {
    font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 0.75rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.card-content { font-size: 0.875rem; line-height: 1.7; color: var(--text); }

/* ── Badges ── */
.badge {
    display: inline-block; padding: 0.2rem 0.6rem; border-radius: 4px;
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
}
.badge-purple { background: rgba(124,58,237,0.2); color: var(--accent-glow); border: 1px solid rgba(124,58,237,0.3); }
.badge-cyan   { background: rgba(6,182,212,0.15);  color: var(--accent-2);   border: 1px solid rgba(6,182,212,0.3); }
.badge-green  { background: rgba(16,185,129,0.15); color: var(--success);    border: 1px solid rgba(16,185,129,0.3); }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.875rem !important; letter-spacing: 0.05em !important;
    padding: 0.6rem 1.5rem !important; transition: all 0.2s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
}

/* File uploader */
.stFileUploader > div {
    background: var(--surface-2) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 10px !important; color: var(--text-muted) !important;
}
.stFileUploader > div:hover { border-color: var(--accent) !important; }
.stFileUploader label { color: var(--text-muted) !important; font-size: 0.78rem !important; }

/* Sidebar collapse/expand arrow */
[data-testid="collapsedControl"] { color: #ffffff !important; }
[data-testid="collapsedControl"] svg { fill: #ffffff !important; stroke: #ffffff !important; }
button[kind="header"] svg { fill: #ffffff !important; }
.st-emotion-cache-1dp5vir, [data-testid="stSidebarCollapseButton"] svg { fill: #ffffff !important; }

/* Radio */
.stRadio > label { display: none; }
.stRadio > div { display: flex !important; flex-direction: row !important; gap: 6px !important; }
.stRadio > div > label {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
    border-radius: 6px !important; padding: 5px 14px !important;
    font-size: 0.75rem !important; color: var(--text-muted) !important;
    cursor: pointer !important; transition: all 0.15s !important;
}
.stRadio > div > label:has(input:checked) {
    background: rgba(124,58,237,0.15) !important;
    border-color: var(--accent) !important; color: var(--accent-glow) !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
    color: var(--accent-2) !important; box-shadow: none !important;
    transform: none !important; font-size: 0.78rem !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent-2) !important;
    box-shadow: 0 4px 16px rgba(6,182,212,0.2) !important;
}

/* ── Pipeline status bars ── */
.status-bar {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.75rem 1rem; background: var(--surface-2);
    border-radius: 8px; margin: 0.4rem 0;
    border: 1px solid var(--border); font-size: 0.8rem;
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-active  { background: var(--accent-glow); box-shadow: 0 0 8px var(--accent-glow); animation: pulse 1.5s infinite; }
.dot-done    { background: var(--success); }
.dot-pending { background: var(--border); }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

/* ── Chat ── */
.chat-container {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.25rem;
    max-height: 420px; overflow-y: auto; margin-bottom: 1rem;
}
.chat-msg { margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.2rem; }
.chat-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; }
.chat-bubble {
    display: inline-block; padding: 0.6rem 1rem; border-radius: 10px;
    font-size: 0.85rem; line-height: 1.6; max-width: 90%;
}
.user-label  { color: var(--accent-glow); }
.bot-label   { color: var(--accent-2); }
.user-bubble { background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.25); align-self: flex-end; }
.bot-bubble  { background: rgba(6,182,212,0.1);  border: 1px solid rgba(6,182,212,0.2);  align-self: flex-start; }

/* ── Misc ── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
.transcript-box {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: 8px; padding: 1.25rem; font-size: 0.82rem;
    line-height: 1.8; max-height: 300px; overflow-y: auto;
    color: var(--text-muted); white-space: pre-wrap; word-break: break-word;
}
.stProgress > div > div > div { background: var(--accent) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--text-muted) !important; font-size: 0.8rem !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

</style>
""", unsafe_allow_html=True)

# ─── Lazy imports (errors show in UI, not blank page) ────────────────────────
try:
    from utils.audio_processor import process_input
    from core.transcriber import transcribe_all
    from core.summarize import summarize, generate_title
    from core.extractor import extract_action_items, extract_key_decisions, extract_questions
    from core.rag_engine import build_rag_chain, ask_question
    IMPORTS_OK = True
except Exception as _e:
    IMPORTS_OK = False
    _IMPORT_ERR = str(_e)

# ─── Session State ────────────────────────────────────────────────────────────
for _k, _v in {
    "result":         None,
    "chat_history":   [],
    "processing":     False,
    "pipeline_done":  False,
    "pipeline_steps": {},
    "uploaded_tmp":   None,
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─── Constants ────────────────────────────────────────────────────────────────
PIPELINE_STEPS = [
    ("audio",      "🔊", "Audio Processing"),
    ("transcript", "📝", "Transcription"),
    ("title",      "🏷️",  "Title Generation"),
    ("summary",    "📋", "Summarisation"),
    ("extract",    "🔍", "Extraction"),
    ("rag",        "🧠", "RAG Engine"),
]

# ─── Helpers ─────────────────────────────────────────────────────────────────
def render_step_bar(label, key, icon):
    s = st.session_state.pipeline_steps.get(key, "pending")
    css = {"active": "dot-active", "done": "dot-done"}.get(s, "dot-pending")
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot {css}"></div>
        <span>{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

def update_step(key, state):
    st.session_state.pipeline_steps[key] = state

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.9rem">🎬 MeetFlow</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI Video Intelligence with RAG</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="badge badge-purple">Input Source</span>', unsafe_allow_html=True)
    input_mode = st.radio("", ["YouTube URL", "Upload File"], key="input_mode")

    source_path = None

    if input_mode == "YouTube URL":
        yt_url = st.text_input("", placeholder="https://youtube.com/watch?v=...",
                               label_visibility="collapsed", key="yt_url")
        if yt_url.strip():
            source_path = yt_url.strip()
    else:
        uploaded = st.file_uploader("",
                                    type=["mp4","mkv","mov","webm","avi","mp3","wav","m4a"],
                                    label_visibility="collapsed", key="uploader")
        if uploaded:
            suffix = os.path.splitext(uploaded.name)[1]
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.read()); tmp.flush(); tmp.close()
            st.session_state.uploaded_tmp = tmp.name
            source_path = tmp.name
            st.markdown(f'<span class="badge badge-green">✓ {uploaded.name[:28]}</span>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="badge badge-cyan">Language</span>', unsafe_allow_html=True)
    language = st.selectbox("",
        ["english", "hinglish"],
        format_func=lambda x: "🇬🇧 English (Whisper)" if x == "english"
                              else "🇮🇳 Hindi / Hinglish (Sarvam)",
        label_visibility="collapsed", key="lang_select")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡  Analyse", use_container_width=True)

    if st.session_state.pipeline_steps:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">Pipeline Status</span>',
                    unsafe_allow_html=True)
        for step, icon, label in PIPELINE_STEPS:
            render_step_bar(label, step, icon)

    if st.session_state.result:
        st.markdown("---")
        if st.button("↺  New Analysis", use_container_width=True, type="secondary"):
            if st.session_state.uploaded_tmp and os.path.exists(st.session_state.uploaded_tmp):
                os.unlink(st.session_state.uploaded_tmp)
            st.session_state.update({
                "result": None, "chat_history": [],
                "pipeline_steps": {}, "pipeline_done": False, "uploaded_tmp": None,
            })
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:0.5rem">
        <span class="badge badge-purple">Whisper</span>
        <span class="badge badge-cyan">Sarvam</span>
        <span class="badge badge-green">RAG</span>
    </div>
    <div style="font-size:0.6rem;color:var(--text-muted);line-height:1.65">
        MP4 · MKV · MP3 · WAV · WebM<br>English via Whisper · Hindi via Sarvam AI
    </div>""", unsafe_allow_html=True)


# ─── Main ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title"> AI Assistance Panel</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub"> ▶ Transcribe ▶ Summarise your meetings/videos ▶ Chat with your meetings</div>',
            unsafe_allow_html=True)
st.markdown("---")

# ─── Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source_path:
        st.error("⚠️ Please provide a YouTube URL or upload a file first.")
    else:
        st.session_state.update({
            "pipeline_done": False, "result": None, "chat_history": [],
            "pipeline_steps": {k: "pending" for k, *_ in PIPELINE_STEPS},
        })
        banner = st.empty()
        bar    = st.empty()
        try:
            banner.info("⚙️ Pipeline running — see sidebar for live status…")

            update_step("audio", "active");      bar.progress(5,  "Extracting audio…")
            chunks = process_input(source_path)
            update_step("audio", "done")

            update_step("transcript", "active"); bar.progress(20, "Transcribing…")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active");      bar.progress(45, "Generating title…")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active");    bar.progress(58, "Summarising…")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active");    bar.progress(72, "Extracting insights…")
            action_items = extract_action_items(transcript)
            decisions    = extract_key_decisions(transcript)
            questions    = extract_questions(transcript)
            update_step("extract", "done")

            update_step("rag", "active");        bar.progress(88, "Building RAG chain…")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            bar.progress(100, "✓ Complete!")
            time.sleep(0.4)

            st.session_state.result = {
                "title": title, "transcript": transcript, "summary": summary,
                "action_items": action_items, "key_decisions": decisions,
                "open_questions": questions, "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            banner.success("✅ Analysis complete!")
            time.sleep(0.5)
            banner.empty(); bar.empty()
            st.rerun()

        except Exception as e:
            for k, *_ in PIPELINE_STEPS:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            banner.error(f"❌ Pipeline error: {e}")
            bar.empty()

# ─── Results ─────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    st.markdown(f"""
    <div class="card">
        <div class="card-title">📌 Session Title</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Summary</div>
            <div class="card-content">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        with st.expander("📝 Full Transcript", expanded=False):
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>',
                        unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button("⬇  Download Transcript (.txt)",
                data=r["transcript"],
                file_name=f"{r['title'][:40].replace(' ','_')}_transcript.txt",
                mime="text/plain", use_container_width=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">✅ Action Items</div>
            <div class="card-content">{r['action_items']}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">🔑 Key Decisions</div>
            <div class="card-content">{r['key_decisions']}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">❓ Open Questions</div>
            <div class="card-content">{r['open_questions']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;'
                'font-weight:700;margin-bottom:1rem">💬 Chat with your Meeting</div>',
                unsafe_allow_html=True)

    if not r.get("rag_chain"):
        st.warning("RAG chain unavailable — re-run the pipeline.")
    else:
        if st.session_state.chat_history:
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f"""
                    <div class="chat-msg" style="align-items:flex-end">
                        <span class="chat-label user-label">You</span>
                        <div class="chat-bubble user-bubble">{msg['content']}</div>
                    </div>"""
                else:
                    chat_html += f"""
                    <div class="chat-msg" style="align-items:flex-start">
                        <span class="chat-label bot-label">🤖 Assistant</span>
                        <div class="chat-bubble bot-bubble">{msg['content']}</div>
                    </div>"""
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2rem">
                <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
                <div style="color:var(--text-muted);font-size:0.85rem">
                    Ask anything about your meeting transcript
                </div>
            </div>""", unsafe_allow_html=True)

        cc1, cc2 = st.columns([5, 1], gap="small")
        with cc1:
            user_input = st.text_input("", placeholder="What were the main decisions made?",
                                       label_visibility="collapsed", key="chat_input")
        with cc2:
            send_btn = st.button("Send →", use_container_width=True, key="send_btn")

        if send_btn and user_input.strip():
            with st.spinner("Thinking…"):
                try:
                    answer = ask_question(r["rag_chain"], user_input.strip())
                except Exception as e:
                    answer = f"⚠️ Error: {e}"
            st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️  Clear Chat", type="secondary", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

# ─── Empty state ─────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;padding:5rem 2rem;text-align:center">
        <div style="font-size:4rem;margin-bottom:1rem">🎬</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;
                    color:var(--text);margin-bottom:0.5rem">Ready to Analyse ?</div>
        <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
            Paste a YouTube URL or upload a video/audio file in the sidebar,
            choose your language, and hit <strong>Analyse</strong> to get started.
        </div>
        <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-green">RAG Chat</span>
        </div>
    </div>""", unsafe_allow_html=True)