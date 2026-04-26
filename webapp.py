import streamlit as st
from app import PoAGenerator
import random

# --- 1. INITIALIZATION ---
if 'generator' not in st.session_state:
    st.session_state.generator = PoAGenerator()
    st.session_state.current_q = "Ready to start? Click the ✨ Generate New Challenge button."
    st.session_state.dr_acc = []
    st.session_state.cr_acc = []
    st.session_state.topic = "General"
    st.session_state.score = 0
    st.session_state.analysis = []
    st.session_state.concept = ""
    st.session_state.selected_level = "Medium"
    st.session_state.selected_topic = "All Topics"

if not hasattr(st.session_state.generator, 'accounting_theories'):
    st.session_state.generator = PoAGenerator()

# --- 2. CALLBACKS ---
def handle_change():
    topic = st.session_state.get('selected_topic', 'All Topics')
    level = st.session_state.get('selected_level', 'Medium')
    res = st.session_state.generator.get_vault(topic, level)
    st.session_state.show_ans = False
    st.session_state.current_q = res[0]
    st.session_state.dr_acc = res[1]
    st.session_state.cr_acc = res[2]
    st.session_state.topic = res[3]
    st.session_state.analysis = res[4]
    st.session_state.concept = res[5]

# --- 3. PAGE SETUP & CSS ---
st.set_page_config(page_title="PoA Mastery Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background: var(--background-color); background-image: radial-gradient(circle at 2px 2px, rgba(128,128,128,0.15) 1px, transparent 0); background-size: 40px 40px; }
    .journal-table { width: 100%; border-collapse: collapse; background: var(--secondary-background-color); border: 2px solid var(--text-color); border-radius: 10px; overflow: hidden; }
    .journal-table th { background-color: #2d3436; color: #ffffff; padding: 15px; }
    .journal-table td { padding: 15px; border-bottom: 1px solid rgba(128,128,128,0.2); font-size: 18px; color: var(--text-color); }
    .dr-col { color: #2ecc71; text-align: right; width: 120px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 22px; }
    .cr-col { color: #e74c3c; text-align: right; width: 120px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 22px; }
    .indent-cr { padding-left: 50px !important; }
    .question-box { background-color: var(--secondary-background-color); padding: 30px !important; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border-left: 8px solid #2e86de; margin-top: 20px; margin-bottom: 20px; color: var(--text-color); }
    .big-font { font-size: 26px !important; font-weight: 600 !important; line-height: 1.4; }
    .rule-debit { color: #54a0ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    
    category = st.selectbox("Navigation Section:", ["🚀 Let's Practice", "📖 Syllabus Room"])
    
    if category == "🚀 Let's Practice":
        nav_choice = st.radio(
            "Choose Mode:", 
            ["Double Entry Practice", "Source Documents", "Correction of Errors", "Theories & Definitions", "Account Classification"], 
            label_visibility="collapsed"
        )
    else:
        nav_choice = st.radio(
            "Choose Resource:", 
            ["Syllabus Reference", "Contact"], 
            label_visibility="collapsed"
        )

    st.divider()
    st.info(f"**Ahmad Syafiq B Amiruddin**\n\nNIE Student Teacher (PGDE)")

    # --- ADDITIONS BELOW ---
    
    st.divider()
    st.markdown("### 🚀 Version Control")
    col1, col2 = st.columns(2)
    col1.metric("Version", "1.2.0")
    col2.metric("Build", "APR-26")

    st.divider()
    st.markdown("### 📖 Reference")
    st.markdown("**Principles of Accounts**")
    st.caption("G2/G3 Upper Secondary")
    st.caption("Marshall Cavendish Education")
    
    with st.expander("Syllabus Mapping (7088)"):
        st.write("""
        - **Units 1-3:** Ch. 1 to 5
        - **Units 4-5:** Ch. 8 to 10
        - **Unit 6:** Ch. 11 (NCA)
        - **Unit 7:** Ch. 13 to 15
        """)

# --- 5. MAIN CONTENT ---

if nav_choice == "Double Entry Practice":
    st.markdown("<div style='text-align: center;'><h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>PoA Double Entry Practice</h1></div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 1.5, 0.5])
        with col1:
            st.select_slider("Difficulty (AO Level):", options=["Easy", "Medium", "Hard"], key="selected_level", on_change=handle_change)
        with col2:
            topic_list = ["All Topics", "1. Foundations & Equation (Ch 1-3)", "2. Double-entry System (Ch 4-5)", "3. Revenue & Expenses (Ch 6-7)", "4. Assets: Cash & Inventory (Ch 8-9)", "5. Receivables & Payables (Ch 10, 12)", "6. Non-current Assets (Ch 11)", "7. Liabilities, Equity & Errors (Ch 13-15)", "8. Financial Analysis (Ch 16)"]
            st.selectbox("Select Syllabus Topic:", topic_list, key="selected_topic", on_change=handle_change)
        with col3:
            st.metric("Questions Solved", st.session_state.get('score', 0))

    if st.button("✨ Generate New Challenge", use_container_width=True):
        handle_change()
        st.session_state.score += 1
        st.rerun()

    st.markdown(f"<div class='question-box'><p style='color:#8395a7; font-size:12px;'>TOPIC: {st.session_state.topic}</p><p class='big-font'>{st.session_state.current_q}</p></div>", unsafe_allow_html=True)

    if st.session_state.dr_acc and "Ready" not in st.session_state.current_q:
        with st.expander("🔍 Reveal General Journal Entry & Analysis", expanded=st.session_state.show_ans):
            st.subheader("📓 General Journal")
            dr_rows = "".join([f"<tr><td><strong>{n}</strong></td><td class='dr-col'>{v}</td><td></td></tr>" for n, v in st.session_state.dr_acc])
            cr_rows = "".join([f"<tr><td class='indent-cr'><strong>{n}</strong></td><td></td><td class='cr-col'>{v}</td></tr>" for n, v in st.session_state.cr_acc])
            st.markdown(f"<table class='journal-table'><thead><tr><th>Particulars</th><th style='text-align: right;'>Debit ($)</th><th style='text-align: right;'>Credit ($)</th></tr></thead><tbody>{dr_rows}{cr_rows}</tbody></table>", unsafe_allow_html=True)
            
            st.divider()
            st.subheader("💡 Transaction Analysis")
            h1, h2, h3, h4 = st.columns([2, 1, 1, 1])
            h1.markdown("**Account**"); h2.markdown("**Element**"); h3.markdown("**Effect**"); h4.markdown("**Rule**")
            st.divider()

            for item in st.session_state.analysis:
                with st.container():
                    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                    c1.markdown(f"**{item['acc']}**")
                    c2.write(item['elem']); c3.write(item['eff'])
                    c4.markdown(f"<span class='rule-debit'>{item['rule']}</span>", unsafe_allow_html=True)

            if st.session_state.concept:
                st.info(f"**Key Concept:** {st.session_state.concept}")

elif nav_choice == "Theories & Definitions":
    st.markdown("<h1 style='color: #2c3e50;'>Accounting Theories & Definitions</h1>", unsafe_allow_html=True)
    study_type = st.segmented_control("What are we revising?", ["Theories", "Definitions", "Errors"], default="Theories")
    current_list = getattr(st.session_state.generator, f"accounting_{study_type.lower()}")
    
    if 'theory_idx' not in st.session_state: st.session_state.theory_idx = 0
    st.session_state.theory_idx %= len(current_list)
    card = current_list[st.session_state.theory_idx]
    
    st.caption(f"Chapter Reference: {card['unit']}")
    with st.container(border=True):
        st.markdown(f"<h1 style='text-align: center; color: #2e86de; padding: 20px;'>{card['term']}</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("🔍 Reveal Definition", use_container_width=True):
                st.markdown(f"""
                    <div style="
                        background-color: #d4edda; 
                        color: #155724; 
                        padding: 25px; 
                        border-radius: 10px; 
                        font-size: 26px; 
                        line-height: 1.5; 
                        border: 2px solid #c3e6cb;
                    ">
                        <strong>Definition:</strong><br>{card['definition']}
                    </div>
                """, unsafe_allow_html=True)
        if c2.button("Next Item ➡️", use_container_width=True):
            st.session_state.theory_idx = (st.session_state.theory_idx + 1) % len(current_list)
            st.rerun()

elif nav_choice == "Source Documents":
    scenarios = [
        {"type": "Sales Invoice", "vendor": "Ames Ltd", "buyer": "J-Tech Solutions", "items": [("Laptop Pro 14-inch", 2400.00), ("Wireless Mouse", 45.00)], "note": "Terms: 30 days net credit."},
        {"type": "Sales Invoice", "vendor": "North Star Stationery", "buyer": "ABC Tuition Centre", "items": [("A4 Paper Reams (Box of 10)", 120.00), ("Whiteboard Markers", 35.00)], "note": "Goods sold on credit."},
        {"type": "Credit Note", "vendor": "Ames Ltd", "buyer": "J-Tech Solutions", "items": [("Damaged Laptop (Returned)", 800.00)], "note": "Reduction in amount due to faulty goods."},
        {"type": "Debit Note", "vendor": "Elite Tech Ltd", "buyer": "Tan's Gadgets", "items": [("Price adjustment for Inv #902", 50.00)], "note": "Notification of undercharge on previous invoice."},
        {"type": "Receipt", "vendor": "MediServe Singapore", "buyer": "HealthFirst Clinic", "items": [("Settlement of Account", 1500.00)], "note": "Payment received via Cheque #5501."},
        {"type": "Payment Voucher", "vendor": "Elite Tech Ltd", "buyer": "Sparkle Clean Services", "items": [("Office Cleaning Fees", 200.00)], "note": "Paid in cash for April services."},
        {"type": "Bank Statement", "vendor": "DBS Bank", "buyer": "Elite Tech Ltd", "items": [("Bank Charges", 15.00), ("Interest Income", 2.50)], "note": "Statement for the month of April."},
        {"type": "Remittance Advice", "vendor": "Tan's Gadgets", "buyer": "North Star Stationery", "items": [("Payment for Invoice #102", 250.00)], "note": "We have processed your payment via FAST transfer."}
    ]

    doc_meta = {
        "Sales Invoice": {"role": "Evidence of credit sales or purchases", "entry": "Dr Inventory / Cr Trade Payables"},
        "Credit Note": {"role": "Evidence of returns of goods / reduction in amount", "entry": "Dr Trade Payables / Cr Returns Outwards"},
        "Debit Note": {"role": "Evidence of undercharge / increase in amount", "entry": "Dr Inventory / Cr Trade Payables"},
        "Receipt": {"role": "Evidence of cash or cheque received", "entry": "Dr Cash at Bank / Cr Trade Receivables"},
        "Payment Voucher": {"role": "Internal evidence of cash payment", "entry": "Dr Expenses / Cr Cash at Bank"},
        "Bank Statement": {"role": "External evidence of transactions recorded by bank", "entry": "Dr Bank Charges / Cr Cash at Bank"},
        "Remittance Advice": {"role": "Notification of payment details (No journal entry)", "entry": "No Journal Entry Required"}
    }

    col_title, col_toggle = st.columns([2, 1])
    with col_title:
        st.markdown("<h1 style='margin:0; color: #2c3e50;'>Source Document Analysis</h1>", unsafe_allow_html=True)
    with col_toggle:
        difficulty = st.radio("Difficulty:", ["Easy", "Hard"], horizontal=True, label_visibility="collapsed")
        st.caption(f"Current Mode: **{difficulty}**")

    if 'current_doc' not in st.session_state:
        scene = random.choice(scenarios)
        d_type = scene["type"]
        st.session_state.current_doc = {
            "type": d_type,
            "vendor": scene["vendor"],
            "buyer": scene["buyer"],
            "items": scene["items"],
            "note": scene["note"],
            "role": doc_meta[d_type]["role"],
            "entry_logic": doc_meta[d_type]["entry"],
            "date": "25 April 2026",
            "revealed": False,
            "doc_no": f"{random.randint(1000, 9999)}"
        }

    doc = st.session_state.current_doc
    total_val = sum(p for i, p in doc['items'])

    display_title = doc['type'].upper() if difficulty == "Easy" else "BUSINESS DOCUMENT"
    theme_color = "#2e86de" if difficulty == "Easy" else "#2d3436"
    
    st.markdown(f"""
    <div style="border: 2px solid #333; padding: 25px; background-color: #fff; color: #000; border-radius: 5px; box-shadow: 8px 8px 0px {theme_color};">
        <div style="display: flex; justify-content: space-between;">
            <div><h3 style="margin:0; color:{theme_color};">{display_title}</h3><p style="margin:5px 0 0 0;"><strong>FROM:</strong> {doc['vendor']}</p></div>
            <div style="text-align: right;"><p style="margin:0;"><strong>No:</strong> {doc['doc_no']}</p><p style="margin:0;"><strong>Date:</strong> {doc['date']}</p></div>
        </div>
        <hr style="border: 1px solid #000;">
        <p style="margin:0; font-size: 12px; color: #636e72;">TO:</p><p style="margin:0;"><strong>{doc['buyer']}</strong></p>
        <div style="margin-top: 20px; min-height: 80px;">
            <table style="width: 100%; font-size: 14px;">
                <tr style="border-bottom: 2px solid #333;"><th style="text-align: left;">Description</th><th style="text-align: right;">Amount ($)</th></tr>
                {"".join([f"<tr><td>{i}</td><td style='text-align:right;'>{p:,.2f}</td></tr>" for i, p in doc['items']])}
            </table>
        </div>
        <div style="text-align: right; margin-top: 15px; font-size: 18px; border-top: 1px solid #eee;"><strong>TOTAL: ${total_val:,.2f}</strong></div>
        <div style="margin-top: 15px; font-size: 11px; color: #555; font-style: italic;">Note: {doc['note']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🕵️ Discovery Phase")
    c1, c2 = st.columns(2)
    with c1:
        ans1 = st.selectbox("1. Document Type:", ["---"] + list(doc_meta.keys()))
        ans2 = st.selectbox(f"2. Role of document ({doc['buyer']}'s view):", ["---"] + [m["role"] for m in doc_meta.values()])
    with c2:
        ans3 = st.selectbox(f"3. If you are {doc['buyer']}, you are the:", ["---", "Buyer/Recipient", "Seller/Issuer"])
        ans4 = st.selectbox("4. Journal Impact:", ["---", "Credit Purchase", "Return Outwards", "Cash Payment", "Bank Charges", "No Entry Required"])

    if st.button("Check Analysis", use_container_width=True):
        if ans1 == doc['type'] and ans2 == doc['role']:
            st.success(f"🎯 Correct! This is a {doc['type']}.")
            st.session_state.current_doc['revealed'] = True
        else:
            st.error("❌ Incorrect. Re-read the 'Note' and check the 'FROM' entity.")

    if doc['revealed']:
        with st.expander("📓 Syllabus Answer Key", expanded=True):
            st.write(f"**Journal Entry for {doc['buyer']}:**")
            if doc['type'] == "Sales Invoice":
                st.code(f"Dr Inventory ${total_val:,.2f}\nCr Trade Payables ({doc['vendor']}) ${total_val:,.2f}")
            elif doc['type'] == "Credit Note":
                st.code(f"Dr Trade Payables ({doc['vendor']}) ${total_val:,.2f}\nCr Returns Outwards ${total_val:,.2f}")
            elif doc['type'] == "Debit Note":
                st.code(f"Dr Inventory ${total_val:,.2f}\nCr Trade Payables ({doc['vendor']}) ${total_val:,.2f}")
            elif doc['type'] == "Receipt":
                st.code(f"Dr Cash at Bank ${total_val:,.2f}\nCr Trade Receivables ({doc['vendor']}) ${total_val:,.2f}")
            elif doc['type'] == "Payment Voucher":
                st.code(f"Dr Expenses ${total_val:,.2f}\nCr Cash at Bank ${total_val:,.2f}")
            elif doc['type'] == "Bank Statement":
                st.code(f"Dr Bank Charges ${total_val:,.2f}\nCr Cash at Bank ${total_val:,.2f}")
            else:
                st.code("No Journal Entry Required")
            
            if st.button("Next Scenario ➡️"):
                del st.session_state['current_doc']
                st.rerun()

elif nav_choice == "Correction of Errors":
    st.markdown("<div style='text-align: center;'><h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>Correction of Errors</h1></div>", unsafe_allow_html=True)
    
    error_types = {
        "Error of Omission": "The transaction was completely left out of the books.",
        "Error of Commission": "Recorded in the wrong person's account (but right category).",
        "Error of Principle": "Recorded in the wrong type of account (e.g., Asset vs Expense).",
        "Error of Original Entry": "The correct accounts were used, but the wrong amount was recorded in both.",
        "Error of Reversal": "The transaction was recorded on the wrong sides (Dr/Cr swapped).",
    }

    if 'error_scenario' in st.session_state and 'cat' not in st.session_state.error_scenario:
        del st.session_state['error_scenario']

    if 'error_scenario' not in st.session_state:
        v_names = ["Ames Ltd", "J-Tech Solutions", "Elite Tech Ltd", "Tan's Gadgets", "North Star Stationery"]
        c_names = ["The Daily Crust", "HealthFirst Clinic", "ABC Tuition", "Sparkle Cleaners"]
        amt = random.randint(100, 5000)
        
        cat = random.choice(["PURCHASE", "SALE", "RETURN_OUT", "RETURN_IN", "EXPENSE", "ASSET_BUY", "DISHONOUR"])
        e_type = random.choice(list(error_types.keys()))

        if cat == "PURCHASE":
            v = random.choice(v_names)
            base = f"Purchased goods worth <span style='color:#2e86de;'>${amt:,}</span> from <span style='color:#2e86de;'>{v}</span> on credit."
            if e_type == "Error of Principle":
                mkt = "Recorded as a purchase of Office Equipment."
                fix = f"Dr Inventory ${amt:,.2f}\nCr Office Equipment ${amt:,.2f}"
            elif e_type == "Error of Commission":
                mkt = "Recorded in the account of Z-Tech Supplies by mistake."
                fix = f"Dr Trade Payables (Z-Tech Supplies) ${amt:,.2f}\nCr Trade Payables ({v}) ${amt:,.2f}"
            elif e_type == "Error of Reversal":
                mkt = f"Debited {v} and Credited Inventory."
                fix = f"Dr Inventory ${amt*2:,.2f}\nCr Trade Payables ({v}) ${amt*2:,.2f}"
            else:
                e_type = "Error of Omission"; mkt = "No record was made in any journal."; fix = f"Dr Inventory ${amt:,.2f}\nCr Trade Payables ({v}) ${amt:,.2f}"

        elif cat == "SALE":
            c = random.choice(c_names)
            base = f"Sold goods on credit to <span style='color:#2e86de;'>{c}</span> for <span style='color:#2e86de;'>${amt:,}</span>."
            if e_type == "Error of Omission":
                mkt = "The sales invoice was lost and no entry was made."; fix = f"Dr Trade Receivables ({c}) ${amt:,.2f}\nCr Sales Revenue ${amt:,.2f}"
            elif e_type == "Error of Original Entry":
                mkt = f"Recorded as ${amt-50:,} in both the Sales and {c} accounts."; fix = f"Dr Trade Receivables ({c}) $50.00\nCr Sales Revenue $50.00"
            else:
                e_type = "Error of Commission"; mkt = "Recorded in the account of The Weekly Bread instead."; fix = f"Dr Trade Receivables ({c}) ${amt:,.2f}\nCr Trade Receivables (The Weekly Bread) ${amt:,.2f}"

        elif cat == "RETURN_OUT":
            v = random.choice(v_names)
            base = f"Returned faulty goods worth <span style='color:#2e86de;'>${amt//5:,}</span> to <span style='color:#2e86de;'>{v}</span>."
            e_type = "Error of Reversal"
            mkt = "Debited Returns Outwards and Credited Trade Payables."
            fix = f"Dr Trade Payables ({v}) ${(amt//5)*2:,.2f}\nCr Returns Outwards ${(amt//5)*2:,.2f}"

        elif cat == "EXPENSE":
            base = f"Paid <span style='color:#2e86de;'>${amt//10:,}</span> for Repairs to the office premises by cheque."
            if e_type == "Error of Principle":
                mkt = "Recorded as a debit to the Office Premises (Asset) account."; fix = f"Dr Repairs Expense ${(amt//10):,.2f}\nCr Office Premises ${(amt//10):,.2f}"
            else:
                e_type = "Error of Omission"; mkt = "The cheque butt was not recorded."; fix = f"Dr Repairs Expense ${(amt//10):,.2f}\nCr Cash at Bank ${(amt//10):,.2f}"

        elif cat == "ASSET_BUY":
            base = f"Bought a new Display Cabinet (Asset) for <span style='color:#2e86de;'>${amt:,}</span> in cash."
            e_type = "Error of Principle"
            mkt = "Recorded as General Purchases in the Inventory account."
            fix = f"Dr Office Equipment/Fittings ${amt:,.2f}\nCr Inventory ${amt:,.2f}"

        elif cat == "DISHONOUR":
            c = random.choice(c_names)
            base = f"A cheque for <span style='color:#2e86de;'>${amt:,}</span> previously received from <span style='color:#2e86de;'>{c}</span> was dishonoured."
            e_type = "Error of Omission"
            mkt = "No entry was made to record the dishonoured cheque."
            fix = f"Dr Trade Receivables ({c}) ${amt:,.2f}\nCr Cash at Bank ${amt:,.2f}"
        
        else:
            base = f"Paid insurance premium of ${amt:,} by cheque."; e_type = "Error of Omission"; mkt = "Forgot to record."; fix = f"Dr Insurance ${amt:,.2f}\nCr Cash at Bank ${amt:,.2f}"

        st.session_state.error_scenario = {
            "cat": cat, "base": base, "e_type": e_type, "mkt": mkt, "fix": fix, "revealed": False
        }

    err = st.session_state.error_scenario

    st.markdown(f"""
        <div class='question-box'>
            <p style='color:#8395a7; font-size:14px; font-weight:bold; text-transform: uppercase;'>Syllabus Challenge: {err['cat'].replace('_', ' ')}</p>
            <p class='big-font'>
                {err['base']}
                <br><br>
                <span style='color: #e67e22; font-weight: bold;'>The Error:</span> {err['mkt']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🕵️ Analysis & Correction")
    col_sel, col_hint = st.columns([1, 1])
    with col_sel:
        student_choice = st.selectbox("Identify the type of error:", ["---"] + list(error_types.keys()))
    with col_hint:
        st.write("") 
        st.caption(f"Syllabus Focus: {error_types.get(student_choice, 'Select an error to see the definition.')}")
    
    st.write("Provide the Correcting Journal Entry:")
    c_dr, c_cr = st.columns(2)
    with c_dr: st.text_input("Debit Account", placeholder="Account to increase/fix")
    with c_cr: st.text_input("Credit Account", placeholder="Account to decrease/fix")

    if st.button("Verify Correction", use_container_width=True):
        if student_choice == err['e_type']:
            st.success(f"🎯 Spot on! This is an {err['e_type']}.")
            st.session_state.error_scenario['revealed'] = True
        else:
            st.error("❌ Incorrect. Check if the error involves the wrong category of account or just the wrong name.")

    if err['revealed']:
        with st.expander("📓 Syllabus Answer Key", expanded=True):
            st.write("Correcting Journal Entry:")
            st.code(err['fix'])
            if st.button("Next Challenge ➡️"):
                del st.session_state['error_scenario']
                st.rerun()

elif nav_choice == "Account Classification":
    # --- HEADER & METRIC SECTION ---
    st.markdown("<br>", unsafe_allow_html=True)
    header_col, metric_col = st.columns([3, 1])
    
    with header_col:
        st.markdown("<h1 style='color: #ececec; font-size: 3rem; margin: 0; padding: 0;'>Account Classification</h1>", unsafe_allow_html=True)
    
    with metric_col:
        st.markdown("<div style='margin-top: 15px;'>", unsafe_allow_html=True)
        st.metric(label="Questions Solved", value=st.session_state.get('class_score', 0))
        st.markdown("</div>", unsafe_allow_html=True)

    if 'class_score' not in st.session_state:
        st.session_state.class_score = 0

    # --- THE SYLLABUS POOL ---
    accounts_pool = [
        # ASSETS
        {"name": "Cash at Bank", "element": "Asset", "balance": "Debit", "tip": "Money held in the business bank account."},
        {"name": "Cash in Hand", "element": "Asset", "balance": "Debit", "tip": "Physical cash kept on the business premises."},
        {"name": "Inventory", "element": "Asset", "balance": "Debit", "tip": "Goods held for resale to customers."},
        {"name": "Trade Receivables", "element": "Asset", "balance": "Debit", "tip": "Amounts owed to the business by customers for credit sales."},
        {"name": "Office Equipment", "element": "Asset", "balance": "Debit", "tip": "Long-term assets like computers or printers used in the office."},
        {"name": "Motor Vehicles", "element": "Asset", "balance": "Debit", "tip": "Vehicles used for business operations (e.g., delivery vans)."},
        {"name": "Fixtures and Fittings", "element": "Asset", "balance": "Debit", "tip": "Shelving, lighting, or other fixed items in the shop/office."},
        {"name": "Buildings / Premises", "element": "Asset", "balance": "Debit", "tip": "The physical property owned by the business."},
        {"name": "Prepaid Expenses", "element": "Asset", "balance": "Debit", "tip": "Expenses paid in advance that provide a future benefit."},
        {"name": "Accrued Revenue", "element": "Asset", "balance": "Debit", "tip": "Revenue earned but the cash has not been received yet."},
        
        # CONTRA-ASSETS
        {"name": "Allowance for Impairment of Trade Receivables", "element": "Asset (Contra)", "balance": "Credit", "tip": "An estimate of trade receivables that may not be collectible."},
        {"name": "Accumulated Depreciation (Office Equipment)", "element": "Asset (Contra)", "balance": "Credit", "tip": "The total depreciation charged on office equipment to date."},
        {"name": "Accumulated Depreciation (Motor Vehicles)", "element": "Asset (Contra)", "balance": "Credit", "tip": "The total depreciation charged on motor vehicles to date."},
        
        # LIABILITIES
        {"name": "Trade Payables", "element": "Liability", "balance": "Credit", "tip": "Amounts owed by the business to suppliers for credit purchases."},
        {"name": "Bank Loan", "element": "Liability", "balance": "Credit", "tip": "Formal borrowing from a financial institution."},
        {"name": "Bank Overdraft", "element": "Liability", "balance": "Credit", "tip": "A negative bank balance where the business owes the bank."},
        {"name": "Accrued Expenses", "element": "Liability", "balance": "Credit", "tip": "Expenses incurred but not yet paid for."},
        {"name": "Income Received in Advance / Unearned Revenue", "element": "Liability", "balance": "Credit", "tip": "Cash received from customers before the service/goods are provided."},
        {"name": "Other Payables", "element": "Liability", "balance": "Credit", "tip": "Amounts owed for non-trade items (e.g., electricity bills)."},
        
        # EQUITY & CONTRA-EQUITY
        {"name": "Capital", "element": "Equity", "balance": "Credit", "tip": "The owner's total investment and claim on business assets."},
        {"name": "Drawings", "element": "Equity (Contra)", "balance": "Debit", "tip": "Withdrawals of cash or goods by the owner for personal use."},
        {"name": "Retained Earnings / Profit", "element": "Equity", "balance": "Credit", "tip": "Profits kept in the business rather than being distributed."},
        
        # REVENUE & CONTRA-REVENUE
        {"name": "Sales Revenue", "element": "Revenue", "balance": "Credit", "tip": "Income earned from selling goods in the ordinary course of business."},
        {"name": "Service Revenue / Fees", "element": "Revenue", "balance": "Credit", "tip": "Income earned from providing services to customers."},
        {"name": "Commission Income", "element": "Revenue", "balance": "Credit", "tip": "Income earned for acting as an agent or providing a referral."},
        {"name": "Rent Income", "element": "Revenue", "balance": "Credit", "tip": "Income earned from subletting part of the premises."},
        {"name": "Interest Income", "element": "Revenue", "balance": "Credit", "tip": "Income earned from bank deposits or loans to others."},
        {"name": "Returns Inwards", "element": "Revenue (Contra)", "balance": "Debit", "tip": "Goods returned to us by customers; reduces sales revenue."},
        
        # EXPENSES / ADJUSTMENTS
        {"name": "Cost of Sales", "element": "Expense", "balance": "Debit", "tip": "The direct cost of goods sold to customers."},
        {"name": "Wages and Salaries", "element": "Expense", "balance": "Debit", "tip": "Payments made to employees for their work."},
        {"name": "Rent Expense", "element": "Expense", "balance": "Debit", "tip": "The cost of using business premises."},
        {"name": "Insurance Expense", "element": "Expense", "balance": "Debit", "tip": "Payments for protection against business risks."},
        {"name": "Advertising Expense", "element": "Expense", "balance": "Debit", "tip": "The cost of promoting the business to customers."},
        {"name": "Electricity / Utilities", "element": "Expense", "balance": "Debit", "tip": "The cost of power and water used by the business."},
        {"name": "Repairs and Maintenance", "element": "Expense", "balance": "Debit", "tip": "Costs to keep assets in good working condition."},
        {"name": "Impairment Loss on Trade Receivables", "element": "Expense", "balance": "Debit", "tip": "The expense recognized when a debt is confirmed as uncollectible."},
        {"name": "Depreciation Expense", "element": "Expense", "balance": "Debit", "tip": "The allocation of a non-current asset's cost over its useful life."},
        {"name": "Loss on Disposal of Non-Current Asset", "element": "Expense", "balance": "Debit", "tip": "The loss made when an asset is sold for less than its book value."},
        {"name": "Returns Outwards", "element": "Inventory (Adjustment)", "balance": "Credit", "tip": "Goods returned by us to suppliers; reduces inventory cost."}
    ]

    if 'class_q' in st.session_state and 'tip' not in st.session_state.class_q:
        del st.session_state['class_q']

    if 'class_q' not in st.session_state:
        st.session_state.class_q = random.choice(accounts_pool)
        st.session_state.class_revealed = False

    q = st.session_state.class_q

    # --- DARK THEMED QUESTION BOX ---
    st.markdown(f"""
        <div style='background-color: #1e272e; padding: 40px; border-radius: 12px; border: 1px solid #485460; margin-top: 20px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.5);'>
            <p style='color:#808e9b; font-size:14px; font-weight:bold; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px;'>Syllabus Challenge</p>
            <h2 style='color: #d2dae2; margin: 0; font-size: 2rem;'>
                Account Name: <span style='color: #4bcffa;'>{q['name']}</span>
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # --- ANALYSIS PORTION WITH BUTTON-STYLE SELECTORS ---
    st.markdown("### 🕵️ Analysis")
    
    with st.container():
        sel_col, bal_col = st.columns([2, 1])
        
        with sel_col:
            st.markdown("<p style='font-weight: bold; color: #74b9ff; margin-bottom: 5px;'>1. CLASSIFICATION</p>", unsafe_allow_html=True)
            elements = ["Asset", "Asset (Contra)", "Liability", "Equity", "Equity (Contra)", "Revenue", "Revenue (Contra)", "Expense", "Inventory (Adjustment)"]
            user_element = st.selectbox("Element Type", ["---"] + elements, label_visibility="collapsed")
        
        with bal_col:
            st.markdown("<p style='font-weight: bold; color: #74b9ff; margin-bottom: 10px;'>2. NORMAL BALANCE</p>", unsafe_allow_html=True)
            # Using st.pills for button-style selection side-by-side
            user_bal = st.pills("Balance Selection", ["Debit", "Credit"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Check Classification", use_container_width=True, type="primary"):
        if user_element == "---" or user_bal is None:
            st.warning("Please select both the Classification and the Normal Balance.")
        elif user_element == q['element'] and user_bal == q['balance']:
            st.success(f"🎯 Correct! {q['name']} is a {q['element']} with a {q['balance']} balance.")
            st.session_state.class_score += 1
            st.session_state.class_revealed = True
        else:
            st.error("❌ Incorrect classification.")
            st.info(f"💡 **Syllabus Tip:** {q['tip']}")

    if st.session_state.class_revealed:
        if st.button("Next Account ➡️", use_container_width=True):
            del st.session_state['class_q']
            st.session_state.class_revealed = False
            st.rerun()

elif nav_choice == "Syllabus Reference":
    st.markdown("<h1>Syllabus Reference</h1>", unsafe_allow_html=True)
    st.write("Reference materials for the POA Syllabus.")

elif nav_choice == "Contact":
    st.title("Contact")
    st.write("Ahmad Syafiq B Amiruddin - Student Teacher (NIE)")
