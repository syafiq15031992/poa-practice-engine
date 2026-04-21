import streamlit as st
import time
from app import PoAGenerator

# --- 1. INITIALIZATION ---
if 'generator' not in st.session_state:
    st.session_state.generator = PoAGenerator()

if 'score' not in st.session_state:
    st.session_state.score = 0

# --- 2. PAGE SETUP & ADVANCED CSS ---
st.set_page_config(page_title="PoA Mastery Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

    .journal-table {
        width: 100%;
        border-collapse: collapse;
        background: #ffffff;
        border: 2px solid #2d3436;
    }
    .journal-table th { 
        background-color: #2d3436; 
        color: white; 
        padding: 15px; 
        font-size: 16px; 
    }
    .journal-table td { 
        padding: 15px; 
        border-bottom: 1px solid #dfe6e9;
        font-size: 18px; 
        color: #2d3436;
    }
    .dr-col, .cr-col { 
        text-align: right; 
        width: 120px; 
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 22px; 
    }
    .dr-col { color: #27ae60; }
    .cr-col { color: #c0392b; }
    .indent-cr { padding-left: 50px !important; }
    .narration-row {
        font-style: italic; 
        color: #57606f; 
        font-size: 16px; 
        padding-top: 10px;
        padding-bottom: 15px;
    }
    .question-box {
        background-color: #ffffff;
        padding: 30px !important;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 8px solid #2e86de; 
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .scenario-label {
        color: #8395a7; 
        font-size: 13px; 
        font-weight: bold; 
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .big-font {
        font-size: 26px !important;
        font-weight: 600 !important;
        color: #2d3436;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION & TOPIC FILTER ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["🚀 Practice Engine", "📖 Syllabus Reference", "📧 Contact"])
    
    st.divider()
    
    # TOPIC FILTER SELECTOR
    st.subheader("🎯 Focus Area")
    topic_list = [
        "All", "Inventory", "Revenue", "NCA", "Depreciation", 
        "Disposal", "Accruals", "Prepayments", "Impairment", 
        "Capital", "Loans", "Limited Co", "Bank Recon", "Errors", "Suspense", "Concepts"
    ]
    selected_topic = st.selectbox("Select Syllabus Topic:", topic_list)
    
    st.divider()
    st.subheader("Session Progress")
    st.metric(label="Questions Solved", value=st.session_state.score)
    st.progress(min(st.session_state.score * 10, 100))
    
    st.divider()
    st.info("**Syafiq**\n\nNIE Student Teacher (PGDE)\n\n*POA Specialist*")

# --- 4. MAIN CONTENT ---
if page == "🚀 Practice Engine":
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>PoA Practice Engine</h1>
            <p style='color: #576574; font-size: 1.2rem; opacity: 0.8;'>Refining Double-Entry Precision (Syllabus 7088/7086)</p>
            <div style="height: 5px; width: 100px; background-color: #2e86de; margin: 20px auto; border-radius: 10px;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    if st.button("✨ Generate New Challenge", use_container_width=True, key="master_vault_btn"):
        st.session_state.score += 1
        
        # Passing the selected topic to your app.py generator
        q, dr_acc, cr_acc, amt, topic = st.session_state.generator.get_vault(selected_topic)
        
        st.markdown(f"""
            <div class="question-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <p class="scenario-label">Accounting Scenario</p>
                    <span style="background: #dfe6e9; color: #2d3436; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: bold;">
                        {topic.upper()}
                    </span>
                </div>
                <p class="big-font">{q}</p>
            </div>
        """, unsafe_allow_html=True)

        with st.spinner('Validating entries...'):
            time.sleep(0.4)

        with st.expander("🔍 Reveal General Journal Entry"):
            narration_text = q.split(' for')[0] if ' for' in q else q
            
            journal_html = f"""
            <table class="journal-table">
                <thead>
                    <tr>
                        <th>Particulars</th>
                        <th style="text-align: right;">Debit ($)</th>
                        <th style="text-align: right;">Credit ($)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>{dr_acc}</strong></td>
                        <td class="dr-col">{amt}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td class="indent-cr"><strong>{cr_acc}</strong></td>
                        <td></td>
                        <td class="cr-col">{amt}</td>
                    </tr>
                    <tr>
                        <td colspan="3" class="narration-row">
                            &nbsp;&nbsp;(Being {narration_text.lower()})
                        </td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(journal_html, unsafe_allow_html=True)
            st.balloons()

elif page == "📖 Syllabus Reference":
    st.title("Syllabus Guide")
    st.info("Study Tip: Use the DEAD LIC acronym for Double-Entry Rules.")

elif page == "📧 Contact":
    st.title("Contact")
    st.write("Feedback? Reach out to Syafiq via the NIE portal.")