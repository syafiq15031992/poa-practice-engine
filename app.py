import streamlit as st
import random
import time

# --- 1. THE ENGINE (Logic) ---
class PoAGenerator:
    def __init__(self):
        # Precise K342/K233 terminology
        self.trade_entities = ["Alpha Trading", "Tan & Sons", "LKH Ltd", "J. Wong & Co"]
        self.other_entities = ["Best Motors", "Total Office Solutions", "Tech-Mart"]
        
        self.non_current_assets = ["Office Equipment", "Motor Vehicles", "Computers", "Machinery"]
        self.expenses = ["Utilities", "Insurance", "Advertising", "Rates and Taxes", "Wages and Salaries"]

    def get_vault(self, category="All"):
        t_ent = random.choice(self.trade_entities)
        o_ent = random.choice(self.other_entities)
        ast = random.choice(self.non_current_assets)
        exp = random.choice(self.expenses)
        amt = random.randrange(1000, 5000, 100)
        small_amt = random.randrange(50, 400, 10)

        # THE COMPREHENSIVE VAULT
        vault = [
            # --- PILLAR 1: THE TRADING ACCOUNT (Inventory & Sales) ---
            {"topic": "Inventory", "q": f"Purchased goods for ${amt} on credit from {t_ent}", "dr": "Inventory", "cr": f"Trade Payables - {t_ent}", "val": amt},
            {"topic": "Inventory", "q": f"Returned goods worth ${small_amt} to {t_ent} due to defects", "dr": f"Trade Payables - {t_ent}", "cr": "Purchase Returns", "val": small_amt},
            {"topic": "Revenue", "q": f"Sold goods on credit to {t_ent} for ${amt}", "dr": f"Trade Receivables - {t_ent}", "cr": "Sales Revenue", "val": amt},
            {"topic": "Revenue", "q": f"{t_ent} returned goods worth ${small_amt} from a previous sale", "dr": "Sales Returns", "cr": f"Trade Receivables - {t_ent}", "val": small_amt},
            {"topic": "Drawings", "q": f"Owner took goods worth ${small_amt} for personal use", "dr": "Drawings", "cr": "Inventory", "val": small_amt},

            # --- PILLAR 2: NON-CURRENT ASSETS (The 'Expensive' Stuff) ---
            {"topic": "NCA", "q": f"Paid ${amt} for a new {ast.lower()} and ${small_amt} for delivery charges", "dr": ast, "cr": "Cash at Bank", "val": amt + small_amt},
            {"topic": "Depreciation", "q": f"Annual depreciation for {ast.lower()} is charged at 10% on cost of ${amt*10}", "dr": f"Depreciation - {ast}", "cr": f"Accumulated Depreciation - {ast}", "val": amt},
            {"topic": "Disposal", "q": f"An old {ast.lower()} (Cost: ${amt*2}, Acc. Dep: ${amt}) was sold for ${amt} cash", "dr": "Cash at Bank", "cr": f"Disposal of {ast}", "val": amt},
            {"topic": "CapEx/RevEx", "q": f"Paid ${small_amt} for the annual maintenance of {ast.lower()}", "dr": f"Repair & Maintenance", "cr": "Cash at Bank", "val": small_amt},

            # --- PILLAR 3: ADJUSTMENTS (Year-End Magic) ---
            {"topic": "Accruals", "q": f"At 31 Dec, {exp.lower()} of ${small_amt} was still unpaid", "dr": exp, "cr": f"Accrued {exp}", "val": small_amt},
            {"topic": "Prepayments", "q": f"Paid ${amt} for {exp.lower()}, which includes ${small_amt} for the next year", "dr": f"Prepaid {exp}", "cr": "Cash at Bank", "val": small_amt},
            {"topic": "Impairment", "q": f"A debt of ${small_amt} from {t_ent} is written off as irrecoverable", "dr": "Impairment Loss on Trade Receivables", "cr": f"Trade Receivables - {t_ent}", "val": small_amt},
            {"topic": "Impairment", "q": f"Allowance for Impairment of Trade Receivables is to be adjusted to ${small_amt} (previously ${small_amt + 100})", "dr": "Allowance for Impairment", "cr": "Reduction in Allowance for Impairment", "val": 100},

            # --- PILLAR 4: LIABILITIES & EQUITY ---
            {"topic": "Capital", "q": f"Owner {o_ent} contributed a personal vehicle worth ${amt} into the business", "dr": "Motor Vehicles", "cr": "Capital", "val": amt},
            {"topic": "Loans", "q": f"Took a bank loan of ${amt*5}. Interest for the month is ${small_amt}", "dr": "Interest Expense", "cr": "Cash at Bank / Accrued Interest", "val": small_amt},
            {"topic": "Limited Co", "q": f"The company issued 50,000 ordinary shares for ${amt} cash", "dr": "Cash at Bank", "cr": "Share Capital", "val": amt},

            # --- PILLAR 5: BANK RECON & ERRORS ---
            {"topic": "Bank Recon", "q": f"Bank statement shows a credit transfer of ${amt} from {t_ent} not in books", "dr": "Cash at Bank", "cr": f"Trade Receivables - {t_ent}", "val": amt},
            {"topic": "Bank Recon", "q": f"A cheque of ${small_amt} received from {t_ent} was returned by bank as dishonoured", "dr": f"Trade Receivables - {t_ent}", "cr": "Cash at Bank", "val": small_amt},
            {"topic": "Errors", "q": f"A sale of ${amt} to {t_ent} was recorded in {o_ent}'s account by mistake", "dr": f"Trade Receivables - {t_ent}", "cr": f"Trade Receivables - {o_ent}", "val": amt},
            {"topic": "Errors", "q": f"The purchase of {ast.lower()} for ${amt} was omitted from the books", "dr": ast, "cr": "Other Payables", "val": amt},
        
        # --- PILLAR 6: ACCOUNTING CONCEPTS (Theory Application) ---
            {"topic": "Concepts", "q": f"Owner {o_ent} took ${small_amt} from the cash drawer to pay for personal groceries (Entity Concept)", "dr": "Drawings", "cr": "Cash / Cash at Bank", "val": small_amt},
            {"topic": "Concepts", "q": f"Purchased a calculator for $15. It was recorded as an expense even though it lasts 5 years (Materiality Concept)", "dr": "Office Stationery / General Expenses", "cr": "Cash at Bank", "val": 15},
            {"topic": "Concepts", "q": f"At year-end, a customer is suing the business for ${amt}. A provision for legal claims is created (Prudence Concept)", "dr": "Legal Expenses", "cr": "Provision for Legal Claims", "val": amt},
            {"topic": "Concepts", "q": f"Inventory was bought for ${amt}, but its market value is now ${amt+500}. It is kept at ${amt} in the books (Historical Cost)", "dr": "No Entry Required", "cr": "No Entry Required", "val": 0},

        # --- PILLAR 7: OTHER INCOME (Non-Sales Revenue) ---
            {"topic": "Other Income", "q": f"Received a cheque for ${small_amt} as commission for referring a customer", "dr": "Cash at Bank", "cr": "Commission Income", "val": small_amt},
            {"topic": "Other Income", "q": f"Received ${amt} by cheque for renting out an unused corner of the warehouse", "dr": "Cash at Bank", "cr": "Rent Income", "val": amt},
            {"topic": "Other Income", "q": f"Received a discount of ${small_amt} from supplier {t_ent} for settling the account early", "dr": f"Trade Payables - {t_ent}", "cr": "Discount Received", "val": small_amt},
            {"topic": "Other Income", "q": f"Interest of ${small_amt} was earned on the business's fixed deposit account", "dr": "Cash at Bank", "cr": "Interest Income", "val": small_amt},

        # --- PILLAR 8: NON-CURRENT LIABILITIES (Loans & Interest) ---
            {"topic": "Liabilities", "q": f"Obtained a 5-year bank loan of ${amt*5} to buy new equipment", "dr": "Cash at Bank", "cr": "Bank Loan", "val": amt*5},
            {"topic": "Liabilities", "q": f"Paid the monthly loan installment: ${amt} for principal and ${small_amt} for interest", "dr": "Bank Loan / Interest Expense", "cr": "Cash at Bank", "val": amt + small_amt},
            {"topic": "Liabilities", "q": f"At year-end, interest of ${small_amt} on the bank loan has been incurred but not yet paid", "dr": "Interest Expense", "cr": "Accrued Interest Expense", "val": small_amt},

        # --- PILLAR 9: ADVANCED NCA DISPOSALS (Gains & Losses) ---
            {"topic": "Disposal", "q": f"Sold an old {ast.lower()} (Cost: ${amt*2}, Acc. Dep: ${amt}) for ${amt+200} cash", "dr": "Cash at Bank / Acc. Dep", "cr": f"{ast} / Gain on Disposal", "val": amt+200},
            {"topic": "Disposal", "q": f"Scrapped an old {ast.lower()} (Cost: ${amt}) that was fully depreciated. No cash was received.", "dr": f"Accumulated Depreciation - {ast}", "cr": ast, "val": amt},
            {"topic": "Disposal", "q": f"Traded in an old {ast.lower()} for a trade-in value of ${amt} against a new one costing ${amt*3}", "dr": "New Asset / Acc. Dep", "cr": "Old Asset / Cash", "val": amt*3},

        # --- PILLAR 10: INVENTORY ADJUSTMENTS (Advanced) ---
            {"topic": "Inventory", "q": f"Purchased goods worth ${amt} on credit, subject to a 10% trade discount", "dr": "Inventory", "cr": f"Trade Payables - {t_ent}", "val": int(amt * 0.9)},
            {"topic": "Inventory", "q": f"Inventory was found to be damaged. Cost was ${amt}, but it can only be sold for ${amt-small_amt} (NRV)", "dr": "Cost of Sales / Inventory Loss", "cr": "Inventory", "val": small_amt},
            {"topic": "Inventory", "q": f"The owner took goods costing ${small_amt} for a charity donation (not personal use)", "dr": "Charity / Advertising Expenses", "cr": "Inventory", "val": small_amt},

        # --- PILLAR 11: CONTROL ACCOUNTS (The 'Total' Summaries) ---
            {"topic": "Control Accounts", "q": f"Total credit sales from the Sales Journal was ${amt}. Record the end-of-month summary entry.", "dr": "Trade Receivables Control", "cr": "Sales Revenue", "val": amt},
            {"topic": "Control Accounts", "q": f"A contra entry of ${small_amt} was made between the Sales and Purchase Ledgers.", "dr": "Trade Payables Control", "cr": "Trade Receivables Control", "val": small_amt},
            {"topic": "Control Accounts", "q": f"Interest of ${small_amt} was charged to a credit customer, {t_ent}, for an overdue balance.", "dr": "Trade Receivables Control", "cr": "Interest Income", "val": small_amt},
            {"topic": "Control Accounts", "q": f"Total of Sales Returns Journal for the month was ${small_amt}.", "dr": "Sales Returns", "cr": "Trade Receivables Control", "val": small_amt},

        # --- PILLAR 12: LIMITED COMPANIES (Equity Specifics) ---
            {"topic": "Limited Co", "q": "The directors declared a final ordinary dividend of $0.10 per share on 500,000 issued ordinary shares.", "dr": "Dividends / Retained Earnings", "cr": "Dividends Payable", "val": 50000},
            {"topic": "Limited Co", "q": f"Transfer of ${amt} from the year's profit to the General Reserve account.", "dr": "Retained Earnings", "cr": "General Reserve", "val": amt},
            {"topic": "Limited Co", "q": f"Issued 200,000 new ordinary shares at $1.20 each, with all proceeds received by cheque.", "dr": "Cash at Bank", "cr": "Share Capital", "val": 240000},

        # --- PILLAR 13: THE SUSPENSE ACCOUNT (Correction of Errors Part 2) ---
            {"topic": "Suspense", "q": f"A payment of ${small_amt} for repairs was correctly entered in the Cash Book but omitted from the Repairs account.", "dr": "Repairs Expense", "cr": "Suspense Account", "val": small_amt},
            {"topic": "Suspense", "q": f"The total of the Sales Journal was overcast (overstated) by ${amt}.", "dr": "Sales Revenue", "cr": "Suspense Account", "val": amt},
            {"topic": "Suspense", "q": f"Purchased equipment for ${amt}. It was correctly debited to the Equipment account but entered as ${amt-100} in the Cash Book.", "dr": "Suspense Account", "cr": "Cash at Bank", "val": 100},

        # --- PILLAR 14: SALE OF BUSINESS & GOODWILL ---
            {"topic": "Business Purchase", "q": f"Purchased a small business. Total assets were ${amt*10}, liabilities were ${amt*2}. Paid ${amt*9} by cheque.", "dr": "Assets / Goodwill", "cr": "Liabilities / Cash at Bank", "val": amt*1},
            {"topic": "Equity", "q": f"The owner {o_ent} converted a personal loan of ${amt} into business capital.", "dr": "Personal Loan (to business)", "cr": "Capital", "val": amt},

        # --- PILLAR 15: INCOMPLETE RECORDS (Profit Logic) ---
            {"topic": "Incomplete Records", "q": f"Opening Capital was ${amt}. Closing Capital is ${amt+2000}. Owner drew ${small_amt} during the year. Calculate Profit.", "dr": "Profit & Loss", "cr": "Capital", "val": 2000 + small_amt},
            {"topic": "Inventory", "q": f"Goods were sold at a markup of 25%. If Sales Revenue was ${amt}, calculate the Cost of Sales entry.", "dr": "Cost of Sales", "cr": "Inventory", "val": int(amt / 1.25)},
        ]
        
        if category != "All":
            filtered_vault = [q for q in vault if q['topic'] == category]
            # Fallback if a category is empty or misspelled
            if filtered_vault:
                vault = filtered_vault

        choice = random.choice(vault)
        return choice['q'], choice['dr'], choice['cr'], choice['val'], choice['topic']

        choice = random.choice(templates)

        # We return choice['val'] so the answer ALWAYS matches the question text
        return choice['q'], choice['dr'], choice['cr'], choice['val']

# --- 2. INITIALIZATION ---
if 'generator' not in st.session_state:
    st.session_state.generator = PoAGenerator()

if 'score' not in st.session_state:
    st.session_state.score = 0

# --- 3. UI SETUP & CSS ---
st.set_page_config(page_title="PoA Practice Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .question-box {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 15px;
        border-left: 10px solid #2e86de;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        margin: 20px 0;
    }
    .big-font { font-size:24px !important; font-weight: 600; color: #2c3e50; }
    .journal-table { width: 100%; border-collapse: collapse; background: white; }
    .journal-table td { padding: 10px; border: 1px solid #eee; font-family: 'Courier New'; }
    .indent { padding-left: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    page = st.radio("Go to", ["🚀 Practice Engine", "📖 Syllabus Guide"])
    st.divider()
    st.metric("Total Solved", st.session_state.score)
    st.info("**Syafiq**\n\nNIE Student Teacher\n\nPOA Specialist")

# --- 5. MAIN CONTENT ---
if page == "🚀 Practice Engine":
    st.markdown("<h1 style='text-align: center;'>PoA Practice Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Syllabus K342/K233 Precision Training</p>", unsafe_allow_html=True)
    
    if st.button("✨ Generate New Challenge", use_container_width=True):
        # We unpack the 4 values directly from the generator
        q, dr, cr, amt = st.session_state.generator.get_question()
        st.session_state.score += 1
        
        st.markdown(f"""
            <div class="question-box">
                <p class="big-font">{q}</p>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 Reveal General Journal Entry"):
            # This HTML version uses the CSS classes we defined earlier
            journal_html = f"""
            <table class="journal-table">
                <thead>
                    <tr>
                        <th>Particulars</th>
                        <th>Debit ($)</th>
                        <th>Credit ($)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{dr_acc}</td>
                        <td class="dr-col">{amt}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td class="indent-cr">{cr_acc}</td>
                        <td></td>
                        <td class="cr-col">{amt}</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic; color: #888; font-size: 13px; padding-top: 15px;">
                            (Being {q.split(' for')[0].lower()})
                        </td>
                        <td></td>
                        <td></td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(journal_html, unsafe_allow_html=True)
            st.balloons()

else:
    st.title("Syllabus Guide")
    st.write("Review the rules of Double Entry (DEAD LIC) here.")