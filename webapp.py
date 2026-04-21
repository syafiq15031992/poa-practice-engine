import streamlit as st
import time
from app import PoAGenerator

# --- 1. INITIALIZATION ---
if 'generator' not in st.session_state:
    st.session_state.generator = PoAGenerator()
    st.session_state.current_q = "Ready to start? Click the button above."
    st.session_state.dr_acc = []
    st.session_state.cr_acc = []
    st.session_state.topic = "General"
    st.session_state.score = 0

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="PoA Mastery Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .journal-table { width: 100%; border-collapse: collapse; background: #ffffff; border: 2px solid #2d3436; }
    .journal-table th { background-color: #2d3436; color: white; padding: 15px; font-size: 16px; }
    .journal-table td { padding: 15px; border-bottom: 1px solid #dfe6e9; font-size: 18px; color: #2d3436; }
    .dr-col, .cr-col { text-align: right; width: 120px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 22px; }
    .dr-col { color: #27ae60; }
    .cr-col { color: #c0392b; }
    .indent-cr { padding-left: 50px !important; }
    .narration-row { font-style: italic; color: #57606f; font-size: 16px; padding-top: 10px; padding-bottom: 15px; }
    .question-box { background-color: #ffffff; padding: 30px !important; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 8px solid #2e86de; margin-top: 20px; margin-bottom: 20px; }
    .scenario-label { color: #8395a7; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .big-font { font-size: 26px !important; font-weight: 600 !important; color: #2d3436; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["🚀 Practice Engine", "📖 Syllabus Reference", "📧 Contact"])
    st.divider()
    topic_list = ["All", "Inventory", "Revenue", "NCA", "Depreciation", "Disposal", "Accruals", "Prepayments", "Impairment", "Capital", "Loans", "Limited Co", "Bank Recon", "Errors", "Suspense", "Concepts"]
    selected_topic = st.selectbox("Select Syllabus Topic:", topic_list)
    st.metric(label="Questions Solved", value=st.session_state.score)
    st.progress(min(st.session_state.score * 10, 100))
    st.info("**Syafiq**\n\nNIE Student Teacher (PGDE)")

# --- 4. MAIN CONTENT ---
if page == "🚀 Practice Engine":
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>PoA Practice Engine</h1>
            <p style='color: #576574; font-size: 1.2rem; opacity: 0.8;'>Refining Double-Entry Precision</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("✨ Generate New Challenge", use_container_width=True):
        st.session_state.score += 1
        q, dr, cr, topic = st.session_state.generator.get_vault(selected_topic)
        st.session_state.current_q = q
        st.session_state.dr_acc = dr
        st.session_state.cr_acc = cr
        st.session_state.topic = topic

    # Display Question
    st.markdown(f"""
        <div class="question-box">
            <p class="scenario-label">Accounting Scenario ({st.session_state.topic})</p>
            <p class="big-font">{st.session_state.current_q}</p>
        </div>
    """, unsafe_allow_html=True)

    # Reveal Journal Entry
    if st.session_state.dr_acc: 
        with st.expander("🔍 Reveal General Journal Entry"):
            # DYNAMIC ROW GENERATION
            dr_rows_html = "".join([f"<tr><td><strong>{n}</strong></td><td class='dr-col'>{v:,}</td><td></td></tr>" for n, v in st.session_state.dr_acc])
            cr_rows_html = "".join([f"<tr><td class='indent-cr'><strong>{n}</strong></td><td></td><td class='cr-col'>{v:,}</td></tr>" for n, v in st.session_state.cr_acc])
            
            narration = st.session_state.current_q.split(' for')[0].lower()

            journal_html = f"""
            <table class="journal-table">
                <thead>
                    <tr><th>Particulars</th><th style="text-align: right;">Debit ($)</th><th style="text-align: right;">Credit ($)</th></tr>
                </thead>
                <tbody>
                    {dr_rows_html}
                    {cr_rows_html}
                    <tr><td colspan="3" class="narration-row">&nbsp;&nbsp;(Being {narration})</td></tr>
                </tbody>
            </table>
            """
            # THE FIX: Ensure this line exists and is outside the strings
            st.markdown(journal_html, unsafe_allow_html=True)
            st.balloons()

elif page == "📖 Syllabus Reference":
    st.title("Syllabus Guide")
    st.info("Study Tip: Use the DEAD LIC acronym for Double-Entry Rules.")

elif page == "📧 Contact":
    st.title("Contact")
    st.write("Reach out to Syafiq via the NIE portal.")
    st.write("Feedback? Reach out to Syafiq via the NIE portal.")
