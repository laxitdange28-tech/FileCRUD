import streamlit as st
from pathlib import Path
import os

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Manager",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Sora:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0d0f1a 0%, #111827 60%, #0a0f1e 100%);
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0d1117 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Sora', sans-serif;
    font-size: 14px;
    color: #94a3b8;
    padding: 6px 0;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: #38bdf8;
}

/* Headings */
h1 { 
    font-family: 'JetBrains Mono', monospace !important;
    color: #38bdf8 !important;
    letter-spacing: -1px;
}
h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #e2e8f0 !important;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 16px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* File list item */
.file-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #7dd3fc;
    padding: 6px 12px;
    background: rgba(56,189,248,0.06);
    border-left: 3px solid #0ea5e9;
    border-radius: 0 8px 8px 0;
    margin: 4px 0;
}

/* Success / error boxes */
.msg-success {
    background: rgba(16,185,129,0.12);
    border: 1px solid #10b981;
    border-radius: 10px;
    padding: 12px 18px;
    color: #6ee7b7;
    font-weight: 600;
    margin-top: 10px;
}
.msg-error {
    background: rgba(239,68,68,0.12);
    border: 1px solid #ef4444;
    border-radius: 10px;
    padding: 12px 18px;
    color: #fca5a5;
    font-weight: 600;
    margin-top: 10px;
}
.msg-info {
    background: rgba(56,189,248,0.10);
    border: 1px solid #38bdf8;
    border-radius: 10px;
    padding: 12px 18px;
    color: #7dd3fc;
    margin-top: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    white-space: pre-wrap;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.5px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px rgba(14,165,233,0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14,165,233,0.45);
}

/* Text inputs */
.stTextInput > div > input, .stTextArea > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.15) !important;
}

/* Radio */
.stRadio > div { gap: 6px; }

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* Divider */
hr { border-color: rgba(56,189,248,0.15); }

/* Label colors */
label { color: #94a3b8 !important; font-size: 13px !important; }

/* Folder badge */
.badge-folder {
    display: inline-block;
    background: rgba(99,102,241,0.18);
    border: 1px solid #6366f1;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    color: #a5b4fc;
    font-family: 'JetBrains Mono', monospace;
    margin-left: 8px;
}
.badge-file {
    display: inline-block;
    background: rgba(14,165,233,0.18);
    border: 1px solid #0ea5e9;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    color: #7dd3fc;
    font-family: 'JetBrains Mono', monospace;
    margin-left: 8px;
}
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ──────────────────────────────────────────────────────────
def get_all_items():
    p = Path('.')
    return sorted(p.rglob('*'))

def get_files_only():
    return [i for i in get_all_items() if i.is_file()]

def get_folders_only():
    return [i for i in get_all_items() if i.is_dir()]

def render_file_browser():
    items = get_all_items()
    if not items:
        st.markdown('<div class="msg-info">📭 No files or folders found in current directory.</div>', unsafe_allow_html=True)
        return
    st.markdown("**📁 Current Directory Contents**")
    for item in items:
        icon = "📁" if item.is_dir() else "📄"
        badge = '<span class="badge-folder">folder</span>' if item.is_dir() else '<span class="badge-file">file</span>'
        st.markdown(
            f'<div class="file-item">{icon} {item} {badge}</div>',
            unsafe_allow_html=True
        )


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ File Manager")
    st.markdown("---")
    operation = st.radio(
        "Select Operation",
        [
            "📋 Browse Files",
            "➕ Create File",
            "📖 Read File",
            "✏️ Update File",
            "🗑️ Delete File",
            "🔄 Rename File",
            "📂 Create Folder",
            "🗂️ Remove Folder",
            "📝 Create File in Folder",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        '<div style="color:#475569;font-size:11px;font-family:\'JetBrains Mono\',monospace;">'
        'Working dir:<br><code style="color:#38bdf8">' + str(Path('.').resolve()) + '</code></div>',
        unsafe_allow_html=True
    )


# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("# 🗂️ File Manager")
st.markdown("---")

col_main, col_browser = st.columns([3, 2])

with col_browser:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    render_file_browser()
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ── Browse Files ──────────────────────────────────────────────────────────
    if operation == "📋 Browse Files":
        st.markdown("### 📋 Browse Files & Folders")
        st.info("The directory tree is visible on the right panel. Refresh the page to update.")

    # ── Create File ───────────────────────────────────────────────────────────
    elif operation == "➕ Create File":
        st.markdown("### ➕ Create New File")
        file_name = st.text_input("File Name (e.g. notes.txt)")
        content = st.text_area("File Content", height=150)
        if st.button("Create File"):
            if file_name.strip() == "":
                st.markdown('<div class="msg-error">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
            else:
                p = Path(file_name)
                if p.exists():
                    st.markdown('<div class="msg-error">⚠️ File already exists!</div>', unsafe_allow_html=True)
                else:
                    try:
                        with open(file_name, 'w') as f:
                            f.write(content)
                        st.markdown(f'<div class="msg-success">✅ File <b>{file_name}</b> created successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Read File ─────────────────────────────────────────────────────────────
    elif operation == "📖 Read File":
        st.markdown("### 📖 Read File")
        files = [str(f) for f in get_files_only()]
        if not files:
            st.markdown('<div class="msg-error">No files found.</div>', unsafe_allow_html=True)
        else:
            file_name = st.selectbox("Select File to Read", files)
            if st.button("Read File"):
                try:
                    with open(file_name, 'r') as f:
                        data = f.read()
                    st.markdown(f'<div class="msg-info">{data if data else "(empty file)"}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Update File ───────────────────────────────────────────────────────────
    elif operation == "✏️ Update File":
        st.markdown("### ✏️ Update File")
        files = [str(f) for f in get_files_only()]
        if not files:
            st.markdown('<div class="msg-error">No files found.</div>', unsafe_allow_html=True)
        else:
            file_name = st.selectbox("Select File to Update", files)
            mode = st.radio("Update Mode", ["Overwrite", "Append"], horizontal=True)
            content = st.text_area("New Content", height=130)
            if st.button("Update File"):
                try:
                    open_mode = 'w' if mode == "Overwrite" else 'a'
                    with open(file_name, open_mode) as f:
                        f.write(content)
                    action = "overwritten" if mode == "Overwrite" else "appended"
                    st.markdown(f'<div class="msg-success">✅ File <b>{file_name}</b> {action} successfully!</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Delete File ───────────────────────────────────────────────────────────
    elif operation == "🗑️ Delete File":
        st.markdown("### 🗑️ Delete File")
        files = [str(f) for f in get_files_only()]
        if not files:
            st.markdown('<div class="msg-error">No files found.</div>', unsafe_allow_html=True)
        else:
            file_name = st.selectbox("Select File to Delete", files)
            st.warning(f"⚠️ This will permanently delete **{file_name}**.")
            if st.button("🗑️ Delete File", type="primary"):
                try:
                    os.remove(file_name)
                    st.markdown(f'<div class="msg-success">✅ File <b>{file_name}</b> deleted successfully!</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Rename File ───────────────────────────────────────────────────────────
    elif operation == "🔄 Rename File":
        st.markdown("### 🔄 Rename File")
        files = [str(f) for f in get_files_only()]
        if not files:
            st.markdown('<div class="msg-error">No files found.</div>', unsafe_allow_html=True)
        else:
            old_name = st.selectbox("Select File to Rename", files)
            new_name = st.text_input("New File Name")
            if st.button("Rename File"):
                if new_name.strip() == "":
                    st.markdown('<div class="msg-error">⚠️ Please enter a new file name.</div>', unsafe_allow_html=True)
                else:
                    try:
                        os.rename(old_name, new_name)
                        st.markdown(f'<div class="msg-success">✅ Renamed <b>{old_name}</b> → <b>{new_name}</b></div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Create Folder ─────────────────────────────────────────────────────────
    elif operation == "📂 Create Folder":
        st.markdown("### 📂 Create New Folder")
        folder_name = st.text_input("Folder Name")
        if st.button("Create Folder"):
            if folder_name.strip() == "":
                st.markdown('<div class="msg-error">⚠️ Please enter a folder name.</div>', unsafe_allow_html=True)
            else:
                p = Path(folder_name)
                if p.exists():
                    st.markdown('<div class="msg-error">⚠️ Folder already exists!</div>', unsafe_allow_html=True)
                else:
                    try:
                        p.mkdir(parents=True)
                        st.markdown(f'<div class="msg-success">✅ Folder <b>{folder_name}</b> created successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Remove Folder ─────────────────────────────────────────────────────────
    elif operation == "🗂️ Remove Folder":
        st.markdown("### 🗂️ Remove Folder")
        folders = [str(f) for f in get_folders_only()]
        if not folders:
            st.markdown('<div class="msg-error">No folders found.</div>', unsafe_allow_html=True)
        else:
            folder_name = st.selectbox("Select Folder to Remove", folders)
            st.warning(f"⚠️ Folder must be **empty** to remove. This will delete **{folder_name}**.")
            if st.button("🗂️ Remove Folder"):
                try:
                    p = Path(folder_name)
                    p.rmdir()
                    st.markdown(f'<div class="msg-success">✅ Folder <b>{folder_name}</b> removed successfully!</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    # ── Create File in Folder ─────────────────────────────────────────────────
    elif operation == "📝 Create File in Folder":
        st.markdown("### 📝 Create File Inside a Folder")
        folders = [str(f) for f in get_folders_only()]
        if not folders:
            st.markdown('<div class="msg-error">No folders found. Create a folder first.</div>', unsafe_allow_html=True)
        else:
            folder_name = st.selectbox("Select Target Folder", folders)
            file_name = st.text_input("File Name (e.g. data.txt)")
            content = st.text_area("File Content", height=130)
            if st.button("Create File in Folder"):
                if file_name.strip() == "":
                    st.markdown('<div class="msg-error">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
                else:
                    p = Path(folder_name) / file_name
                    if p.exists():
                        st.markdown('<div class="msg-error">⚠️ File already exists in this folder!</div>', unsafe_allow_html=True)
                    else:
                        try:
                            with open(p, 'w') as f:
                                f.write(content)
                            st.markdown(f'<div class="msg-success">✅ File <b>{p}</b> created successfully!</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f'<div class="msg-error">❌ Error: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)