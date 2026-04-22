import streamlit as st
import time
from app import PoAGenerator

# --- 1. INITIALIZATION ---
# Initialize the generator and session state once
if 'generator' not in st.session_state:
    st.session_state.generator = PoAGenerator()
    st.session_state.current_q = "Ready to start? Click the button below."
    st.session_state.dr_acc = []
    st.session_state.cr_acc = []
    st.session_state.topic = "General"
    st.session_state.score = 0
    st.session_state.analysis = []
    st.session_state.concept = ""

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="PoA Mastery Engine", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: var(--background-color);
        background-image: radial-gradient(circle at 2px 2px, rgba(128,128,128,0.15) 1px, transparent 0);
        background-size: 40px 40px;
    }
    .journal-table { 
        width: 100%; 
        border-collapse: collapse; 
        background: var(--secondary-background-color); 
        border: 2px solid var(--text-color); 
        border-radius: 10px;
        overflow: hidden;
    }
    .journal-table th { background-color: #2d3436; color: #ffffff; padding: 15px; }
    .journal-table td { 
        padding: 15px; 
        border-bottom: 1px solid rgba(128,128,128,0.2); 
        font-size: 18px; 
        color: var(--text-color); 
    }
    .dr-col { color: #2ecc71; text-align: right; width: 120px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 22px; }
    .cr-col { color: #e74c3c; text-align: right; width: 120px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 22px; }
    .indent-cr { padding-left: 50px !important; }
    .question-box { 
        background-color: var(--secondary-background-color); 
        padding: 30px !important; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); 
        border-left: 8px solid #2e86de; 
        margin-top: 20px; 
        margin-bottom: 20px;
        color: var(--text-color);
    }
    .scenario-label { color: #8395a7; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .big-font { font-size: 26px !important; font-weight: 600 !important; line-height: 1.4; }
    .rule-debit { color: #54a0ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CALLBACKS ---
def handle_change():
    """Generates a new question whenever the user changes difficulty or topic."""
    # This prevents the app from crashing if the keys haven't been created yet
    if 'selected_topic' in st.session_state and 'selected_level' in st.session_state:
        res = st.session_state.generator.get_vault(
            st.session_state.selected_topic, 
            st.session_state.selected_level
        )
        st.session_state.current_q = res[0]
        st.session_state.dr_acc = res[1]
        st.session_state.cr_acc = res[2]
        st.session_state.topic = res[3]
        st.session_state.analysis = res[4]
        st.session_state.concept = res[5]

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
    
    page = st.radio("Navigation", ["🚀 Practice Engine", "📖 Syllabus Reference", "📧 Contact"], key="page")
    
    st.divider()

    st.select_slider(
        "Select Difficulty (AO Level):",
        options=["Easy", "Medium", "Hard"],
        value="Medium",
        key="selected_level",
        on_change=handle_change,
        help="Easy: AO1 Knowledge | Medium: AO2 Application | Hard: AO3 Analysis"
    )

    topic_list = ["All", "Inventory", "Revenue", "NCA", "Depreciation", "Disposal", "Accruals", "Prepayments", "Impairment", "Capital", "Loans", "Limited Co", "Bank Recon", "Errors", "Suspense", "Concepts"]
    
    st.selectbox(
        "Select Syllabus Topic:", 
        topic_list,
        key="selected_topic",
        on_change=handle_change
    )
    
    st.metric(label="Questions Solved", value=st.session_state.score)
    st.progress(min(st.session_state.score * 10, 100))
    st.info("**Syafiq**\n\nNIE Student Teacher (PGDE)")

# --- 5. MAIN CONTENT ---
if page == "🚀 Practice Engine":
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>PoA Practice Engine</h1>
            <p style='color: #576574; font-size: 1.2rem; opacity: 0.8;'>Refining Double-Entry Precision</p>
        </div>
    """, unsafe_allow_html=True)

    # FIXED: Using st.session_state instead of local variables
    if st.button("✨ Generate New Challenge", use_container_width=True):
        st.session_state.score += 1
        handle_change() # Use the callback logic to keep it consistent

    # Display Question
    st.markdown(f"""
        <div class="question-box">
            <p class="scenario-label">Accounting Scenario ({st.session_state.topic})</p>
            <p class="big-font">{st.session_state.current_q}</p>
        </div>
    """, unsafe_allow_html=True)

    # REVEAL SECTION
    if st.session_state.dr_acc and st.session_state.current_q != "Ready to start? Click the button below.": 
        with st.expander("🔍 Reveal General Journal Entry & Analysis", expanded=True):
            st.subheader("📓 General Journal")
            
            dr_rows = "".join([f"<tr><td><strong>{n}</strong></td><td class='dr-col'>{v:,}</td><td></td></tr>" for n, v in st.session_state.dr_acc])
            cr_rows = "".join([f"<tr><td class='indent-cr'><strong>{n}</strong></td><td></td><td class='cr-col'>{v:,}</td></tr>" for n, v in st.session_state.cr_acc])
            
            st.markdown(f"""
            <table class="journal-table">
                <thead>
                    <tr><th>Particulars</th><th style="text-align: right;">Debit ($)</th><th style="text-align: right;">Credit ($)</th></tr>
                </thead>
                <tbody>
                    {dr_rows}{cr_rows}
                </tbody>
            </table>
            """, unsafe_allow_html=True)
            
            st.divider()

            st.subheader("💡 Transaction Analysis")
            h1, h2, h3, h4 = st.columns([2, 1, 1, 1])
            h1.markdown("**Account**")
            h2.markdown("**Element**")
            h3.markdown("**Effect**")
            h4.markdown("**Rule**")
            st.divider()

            if st.session_state.analysis:
                for item in st.session_state.analysis:
                    with st.container():
                        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                        c1.markdown(f"**{item['acc']}**")
                        c2.write(item['elem'])
                        c3.write(item['eff'])
                        c4.markdown(f"<span class='rule-debit'>{item['rule']}</span>", unsafe_allow_html=True)
                        st.write("") 
            
            if st.session_state.concept:
                st.info(f"**Key Concept:** {st.session_state.concept}")

            st.balloons()

elif page == "📖 Syllabus Reference":
    st.title("Syllabus Guide")
    st.info("Study Tip: Use the **DEAD LIC** acronym for Double-Entry Rules.")
    # You could add a table here later for the AO1, AO2, AO3 definitions

elif page == "📧 Contact":
    st.title("Contact")
    st.write("Reach out to Syafiq via the NIE portal.")
