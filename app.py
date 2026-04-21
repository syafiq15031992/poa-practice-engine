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
            {"topic": "Inventory", "q": f"Purchased goods for ${amt} on credit from {t_ent}", "dr": [("Inventory", amt)], "cr": [(f"Trade Payables - {t_ent}", amt)]},
            {"topic": "Inventory", "q": f"Returned goods worth ${small_amt} to {t_ent} due to defects", "dr": [(f"Trade Payables - {t_ent}", small_amt)], "cr": [("Purchase Returns", small_amt)]},
            {"topic": "Revenue", "q": f"Sold goods on credit to {t_ent} for ${amt}", "dr": [(f"Trade Receivables - {t_ent}", amt)], "cr": [("Sales Revenue", amt)]},
            {"topic": "Revenue", "q": f"{t_ent} returned goods worth ${small_amt} from a previous sale", "dr": [("Sales Returns", small_amt)], "cr": [(f"Trade Receivables - {t_ent}", small_amt)]},
            {"topic": "Drawings", "q": f"Owner took goods worth ${small_amt} for personal use", "dr": [("Drawings", small_amt)], "cr": [("Inventory", small_amt)]},
            {"topic": "Inventory", "q": f"Purchased goods for ${amt}. Paid ${small_amt} by cheque and the balance on credit from {t_ent}", "dr": [("Inventory", amt)], "cr": [("Cash at Bank", small_amt), (f"Trade Payables - {t_ent}", amt - small_amt)]},

            # --- PILLAR 2: NON-CURRENT ASSETS ---
            {"topic": "NCA", "q": f"Paid ${amt} for a new {ast.lower()} and ${small_amt} for delivery charges", "dr": [(ast, amt + small_amt)], "cr": [("Cash at Bank", amt + small_amt)]},
            {"topic": "Depreciation", "q": f"Annual depreciation for {ast.lower()} is charged at 10% on cost of ${amt*10}", "dr": [(f"Depreciation - {ast}", amt)], "cr": [(f"Accumulated Depreciation - {ast}", amt)]},
            {"topic": "Disposal", "q": f"An old {ast.lower()} (Cost: ${amt*2}, Acc. Dep: ${amt}) was sold for ${amt} cash", "dr": [("Cash at Bank", amt), (f"Accumulated Depreciation - {ast}", amt)], "cr": [(f"Disposal of {ast}", amt * 2)]},
            {"topic": "CapEx/RevEx", "q": f"Paid ${small_amt} for the annual maintenance of {ast.lower()}", "dr": [("Repair & Maintenance", small_amt)], "cr": [("Cash at Bank", small_amt)]},

            # --- PILLAR 3: ADJUSTMENTS ---
            {"topic": "Accruals", "q": f"At 31 Dec, {exp.lower()} of ${small_amt} was still unpaid", "dr": [(exp, small_amt)], "cr": [(f"Accrued {exp}", small_amt)]},
            {"topic": "Prepayments", "q": f"Paid ${amt} for {exp.lower()}, which includes ${small_amt} for the next year", "dr": [(f"Prepaid {exp}", small_amt), (exp, amt - small_amt)], "cr": [("Cash at Bank", amt)]},
            {"topic": "Impairment", "q": f"A debt of ${small_amt} from {t_ent} is written off as irrecoverable", "dr": [("Impairment Loss on Trade Receivables", small_amt)], "cr": [(f"Trade Receivables - {t_ent}", small_amt)]},
            {"topic": "Impairment", "q": f"Allowance for Impairment of Trade Receivables is to be adjusted to ${small_amt} (previously ${small_amt + 100})", "dr": [("Allowance for Impairment", 100)], "cr": [("Reduction in Allowance for Impairment", 100)]},

            # --- PILLAR 4: LIABILITIES & EQUITY ---
            {"topic": "Capital", "q": f"Owner {o_ent} contributed a personal vehicle worth ${amt} into the business", "dr": [("Motor Vehicles", amt)], "cr": [("Capital", amt)]},
            {"topic": "Loans", "q": f"Paid the monthly loan installment: ${amt} for principal and ${small_amt} for interest", "dr": [("Bank Loan", amt), ("Interest Expense", small_amt)], "cr": [("Cash at Bank", amt + small_amt)]},
            {"topic": "Limited Co", "q": f"The company issued 50,000 ordinary shares for ${amt} cash", "dr": [("Cash at Bank", amt)], "cr": [("Share Capital", amt)]},

            # --- PILLAR 5: BANK RECON & ERRORS ---
            {"topic": "Bank Recon", "q": f"Bank statement shows a credit transfer of ${amt} from {t_ent} not in books", "dr": [("Cash at Bank", amt)], "cr": [(f"Trade Receivables - {t_ent}", amt)]},
            {"topic": "Bank Recon", "q": f"A cheque of ${small_amt} received from {t_ent} was returned by bank as dishonoured", "dr": [(f"Trade Receivables - {t_ent}", small_amt)], "cr": [("Cash at Bank", small_amt)]},
            {"topic": "Errors", "q": f"A sale of ${amt} to {t_ent} was recorded in {o_ent}'s account by mistake", "dr": [(f"Trade Receivables - {t_ent}", amt)], "cr": [(f"Trade Receivables - {o_ent}", amt)]},
            {"topic": "Errors", "q": f"The purchase of {ast.lower()} for ${amt} was omitted from the books", "dr": [(ast, amt)], "cr": [("Other Payables", amt)]},

            # --- PILLAR 6: CONCEPTS ---
            {"topic": "Concepts", "q": f"Owner {o_ent} took ${small_amt} from the cash drawer to pay for personal groceries (Entity Concept)", "dr": [("Drawings", small_amt)], "cr": [("Cash", small_amt)]},
            {"topic": "Concepts", "q": f"Purchased a calculator for $15. Recorded as an expense due to small value (Materiality)", "dr": [("Office Stationery", 15)], "cr": [("Cash at Bank", 15)]},
            {"topic": "Concepts", "q": f"At year-end, a provision for legal claims of ${amt} is created (Prudence)", "dr": [("Legal Expenses", amt)], "cr": [("Provision for Legal Claims", amt)]},
            {"topic": "Concepts", "q": f"Inventory bought for ${amt} stays at ${amt} despite market value rising (Historical Cost)", "dr": [("No Entry Required", 0)], "cr": [("No Entry Required", 0)]},

            # --- PILLAR 7: OTHER INCOME ---
            {"topic": "Other Income", "q": f"Received a cheque for ${small_amt} as commission earned", "dr": [("Cash at Bank", small_amt)], "cr": [("Commission Income", small_amt)]},
            {"topic": "Other Income", "q": f"Received ${amt} by cheque for renting out premises", "dr": [("Cash at Bank", amt)], "cr": [("Rent Income", amt)]},
            {"topic": "Other Income", "q": f"Received a discount of ${small_amt} from supplier {t_ent} for early payment", "dr": [(f"Trade Payables - {t_ent}", small_amt)], "cr": [("Discount Received", small_amt)]},

            # --- PILLAR 8: LIABILITIES ---
            {"topic": "Liabilities", "q": f"Obtained a 5-year bank loan of ${amt*5} to buy new equipment", "dr": [("Cash at Bank", amt * 5)], "cr": [("Bank Loan", amt * 5)]},
            {"topic": "Liabilities", "q": f"At year-end, interest of ${small_amt} on the bank loan has been incurred but not yet paid", "dr": [("Interest Expense", small_amt)], "cr": [("Accrued Interest Expense", small_amt)]},

            # --- PILLAR 9: ADVANCED DISPOSALS ---
            {"topic": "Disposal", "q": f"Scrapped an old {ast.lower()} (Cost: ${amt}) that was fully depreciated. No cash received.", "dr": [(f"Accumulated Depreciation - {ast}", amt)], "cr": [(ast, amt)]},
            {"topic": "Disposal", "q": f"Traded in an old {ast.lower()} (Cost: ${amt}, Acc. Dep: ${small_amt}) for a new one costing ${amt*3}", "dr": [(f"{ast} (New)", amt * 3), (f"Accumulated Depreciation - {ast}", small_amt)], "cr": [(f"{ast} (Old)", amt), ("Cash at Bank", amt * 3 - (amt - small_amt))]},

            # --- PILLAR 10: ADVANCED INVENTORY ---
            {"topic": "Inventory", "q": f"Purchased goods worth ${amt} on credit, subject to a 10% trade discount", "dr": [("Inventory", int(amt * 0.9))], "cr": [(f"Trade Payables - {t_ent}", int(amt * 0.9))]},
            {"topic": "Inventory", "q": f"Inventory found damaged. Cost ${amt}, but NRV is only ${amt-small_amt}.", "dr": [("Inventory Loss / Cost of Sales", small_amt)], "cr": [("Inventory", small_amt)]},

            # --- PILLAR 11: CONTROL ACCOUNTS ---
            {"topic": "Control Accounts", "q": f"Total credit sales from the Sales Journal was ${amt}.", "dr": [("Trade Receivables Control", amt)], "cr": [("Sales Revenue", amt)]},
            {"topic": "Control Accounts", "q": f"A contra entry of ${small_amt} was made between Sales and Purchase Ledgers.", "dr": [("Trade Payables Control", small_amt)], "cr": [("Trade Receivables Control", small_amt)]},

            # --- PILLAR 12: LIMITED COMPANIES ---
            {"topic": "Limited Co", "q": "The directors declared a final ordinary dividend of $0.10 per share on 500,000 shares.", "dr": [("Retained Earnings", 50000)], "cr": [("Dividends Payable", 50000)]},
            {"topic": "Limited Co", "q": f"Transfer of ${amt} from year's profit to General Reserve.", "dr": [("Retained Earnings", amt)], "cr": [("General Reserve", amt)]},

            # --- PILLAR 13: SUSPENSE ACCOUNT ---
            {"topic": "Suspense", "q": f"Repairs of ${small_amt} entered in Cash Book but omitted from Repairs account.", "dr": [("Repairs Expense", small_amt)], "cr": [("Suspense Account", small_amt)]},
            {"topic": "Suspense", "q": f"Total of Sales Journal was overcast (overstated) by ${amt}.", "dr": [("Sales Revenue", amt)], "cr": [("Suspense Account", amt)]},

            # --- PILLAR 14: BUSINESS PURCHASE ---
            {"topic": "Business Purchase", "q": f"Purchased business: Assets ${amt*10}, Liabs ${amt*2}. Paid ${amt*9} by cheque.", "dr": [("Assets", amt * 10), ("Goodwill", amt)], "cr": [("Liabilities", amt * 2), ("Cash at Bank", amt * 9)]},

            # --- PILLAR 15: INCOMPLETE RECORDS ---
            {"topic": "Incomplete Records", "q": f"Closing Capital is ${amt+2000}. Drawings ${small_amt}. Opening Capital ${amt}. Calculate Profit.", "dr": [("Capital", 2000 + small_amt)], "cr": [("Profit & Loss", 2000 + small_amt)]},
            {"topic": "Inventory", "q": f"Goods sold at 25% markup. Sales Revenue ${amt}. Record Cost of Sales.", "dr": [("Cost of Sales", int(amt / 1.25))], "cr": [("Inventory", int(amt / 1.25))]}
        ]
        
        if category != "All":
            filtered_vault = [q for q in vault if q['topic'] == category]
            if filtered_vault:
                vault = filtered_vault

        # THE FIX: 
        # 1. Select the item
        # 2. Return ONLY the 4 required values (q, dr, cr, topic)
        # 3. No extra code below this return
        choice = random.choice(vault)
        return choice['q'], choice['dr'], choice['cr'], choice['topic']
    st.title("Syllabus Guide")
    st.write("Review the rules of Double Entry (DEAD LIC) here.")
