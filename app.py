import streamlit as st
import random

# --- 1. THE ENGINE (Logic) ---
class PoAGenerator:
    def __init__(self):
        # --- RANDOMIZED SEED LISTS ---
        self.trade_entities = [
            "Ames Ltd", "Ben & Co", "Chandra Pte Ltd", "Dinesh Trading", 
            "Elijah's Logistics", "Farah Furnishings", "Guan Hoe & Sons", 
            "Hock Seng Apparel", "Ibrahim & Partners", "J-Tech Solutions",
            "Kailash Emporium", "Lina's Boutique", "Maju Jaya Enterprise",
            "Ngee Ann Trading", "Oceanic Seafood", "Pioneer Hardware"
        ] 
        self.other_entities = [
            "Randy", "Mr Tan", "Ms Lee", "Mrs Gopal", "Alice Wong", 
            "David Lim", "Fatimah", "Ryan", "Hafiz", "Zhi Hao"
        ]
        self.non_current_assets = [
            "Motor Vehicles", "Office Equipment", "Computers", "Machinery", 
            "Delivery Vans", "Display Cabinets", "Air-Conditioning Units", 
            "Store Fixtures", "Photocopying Machines", "Cash Registers"
        ]
        self.expenses = [
            "Rent Expense", "Insurance", "Electricity", "Water & Utilities", 
            "Advertising", "Wages & Salaries", "Telephone Charges", 
            "Printing & Stationery", "General Expenses", "Postage Fees"
        ]

        # 2. THE COMPREHENSIVE VAULT (Stored as self.vault)
        self.vault = [
            # --- EASY: FOUNDATION (AO1) ---
            {"topic": "Inventory", "level": "Easy", "q": "Purchased goods for ${amt} on credit from {t_ent}", "dr": [("Inventory", "amt")], "cr": [(f"Trade Payables - {{t_ent}}", "amt")], "analysis": [{"acc": "Inventory", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Accrual Basis: Transactions are recorded when they occur."},
            {"topic": "Inventory", "level": "Easy", "q": "Returned goods worth ${small_amt} to {t_ent} due to defects", "dr": [(f"Trade Payables - {{t_ent}}", "small_amt")], "cr": [("Purchase Returns", "small_amt")], "analysis": [{"acc": "Trade Payables", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Purchase Returns", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Returns reduce the liability owed to the supplier."},
            {"topic": "Revenue", "level": "Easy", "q": "Sold goods on credit to {t_ent} for ${amt}", "dr": [(f"Trade Receivables - {{t_ent}}", "amt")], "cr": [("Sales Revenue", "amt")], "analysis": [{"acc": "Trade Receivables", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Sales Revenue", "elem": "Revenue", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Revenue increases Equity via the Credit side."},
            {"topic": "Revenue", "level": "Easy", "q": "{t_ent} returned goods worth ${small_amt} from a previous sale", "dr": [("Sales Returns", "small_amt")], "cr": [(f"Trade Receivables - {{t_ent}}", "small_amt")], "analysis": [{"acc": "Sales Returns", "elem": "Contra-Revenue", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Trade Receivables", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Sales Returns reduce total Revenue and amount owed."},
            {"topic": "Drawings", "level": "Easy", "q": "Owner took goods worth ${small_amt} for personal use", "dr": [("Drawings", "small_amt")], "cr": [("Inventory", "small_amt")], "analysis": [{"acc": "Drawings", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Inventory", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Business Entity: Owner's personal use is recorded as Drawings."},
            {"topic": "Inventory", "level": "Easy", "q": "Purchased goods for ${amt}. Paid ${small_amt} by cheque and balance on credit from {t_ent}", "dr": [("Inventory", "amt")], "cr": [("Cash at Bank", "small_amt"), (f"Trade Payables - {{t_ent}}", "amt - small_amt")], "analysis": [{"acc": "Inventory", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}, {"acc": "Trade Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Compound Entry: Multiple credit accounts updated for one purchase."},
            {"topic": "CapEx/RevEx", "level": "Easy", "q": "Paid ${small_amt} for the annual maintenance of {ast_lower}", "dr": [("Repair & Maintenance", "small_amt")], "cr": [("Cash at Bank", "small_amt")], "analysis": [{"acc": "Repairs", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Revenue Expenditure: Maintenance costs are recorded as expenses."},
            {"topic": "Capital", "level": "Easy", "q": "Owner {o_ent} contributed a personal vehicle worth ${amt} into the business", "dr": [("Motor Vehicles", "amt")], "cr": [("Capital", "amt")], "analysis": [{"acc": "Vehicles", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Capital", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Business Entity: Personal assets introduced become business equity."},
            {"topic": "Concepts", "level": "Easy", "q": "Owner {o_ent} took ${small_amt} to pay for personal groceries", "dr": [("Drawings", "small_amt")], "cr": [("Cash", "small_amt")], "analysis": [{"acc": "Drawings", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Cash", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Entity Concept: Business and owner are separate."},
            {"topic": "Concepts", "level": "Easy", "q": "Purchased a calculator for $15. Recorded as an expense due to small value", "dr": [("Office Stationery", 15)], "cr": [("Cash at Bank", 15)], "analysis": [{"acc": "Stationery", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Materiality: Low-value items are expensed for simplicity."},
            {"topic": "Concepts", "level": "Easy", "q": "Inventory bought for ${amt} stays at ${amt} despite market value rising", "dr": [("No Entry Required", 0)], "cr": [("No Entry Required", 0)], "analysis": [{"acc": "Inventory", "elem": "Concept", "eff": "No Change", "rule": "None"}], "concept": "Historical Cost: Recording assets at original purchase price."},
            {"topic": "Other Income", "level": "Easy", "q": "Received a cheque for ${small_amt} as commission earned", "dr": [("Cash at Bank", "small_amt")], "cr": [("Commission Income", "small_amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Commission", "elem": "Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Income: Non-operating revenue increases Equity via Credit."},
            {"topic": "Other Income", "level": "Easy", "q": "Received ${amt} by cheque for renting out premises", "dr": [("Cash at Bank", "amt")], "cr": [("Rent Income", "amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Rent Income", "elem": "Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Income: Rental revenue increases profit."},
            {"topic": "Other Income", "level": "Easy", "q": "Received a discount of ${small_amt} from supplier {t_ent}", "dr": [(f"Trade Payables - {{t_ent}}", "small_amt")], "cr": [("Discount Received", "small_amt")], "analysis": [{"acc": "Trade Payables", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Discount Rec.", "elem": "Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Discount: Gain from early payment reduces amount owed."},
            {"topic": "Liabilities", "level": "Easy", "q": "Obtained a 5-year bank loan of {amt_x_5} to buy new equipment", "dr": [("Cash at Bank", "amt_x_5")], "cr": [("Bank Loan", "amt_x_5")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Loan", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Liability: Borrowing creates an obligation to repay."},
            {"topic": "Inventory", "level": "Easy", "q": "Purchased goods worth ${amt} on credit, subject to 10% trade discount", "dr": [("Inventory", "int(amt * 0.9)")], "cr": [(f"Trade Payables - {{t_ent}}", "int(amt * 0.9)")], "analysis": [{"acc": "Inventory", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Trade Discount: Recorded at net price."},
            {"topic": "Incomplete Records", "level": "Easy", "q": "Closing Capital ${amt_plus_2000}. Drawings ${small_amt}. Opening Capital ${amt}. Record profit.", "dr": [("P&L Summary", "2000 + small_amt")], "cr": [("Capital", "2000 + small_amt")], "analysis": [{"acc": "Profit", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}, {"acc": "Capital", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Capital Equation: Profit increases Equity."},

            # --- MEDIUM: APPLICATION (AO2) ---
            {"topic": "NCA", "level": "Medium", "q": "Paid ${amt} for a new {ast_lower} and ${small_amt} for delivery charges", "dr": [("{ast}", "amt + small_amt")], "cr": [("Cash at Bank", "amt + small_amt")], "analysis": [{"acc": "{ast}", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Capital Expenditure: Delivery costs are included in the asset cost."},
            {"topic": "Depreciation", "level": "Medium", "q": "Annual depreciation for {ast_lower} is charged at 10% on cost of {amt_x_10}", "dr": [(f"Depreciation - {{ast}}", "amt")], "cr": [(f"Accumulated Depreciation - {{ast}}", "amt")], "analysis": [{"acc": "Depreciation", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Acc. Deprec.", "elem": "Contra-Asset", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Matching Principle: Allocating asset cost over useful life."},
            {"topic": "Accruals", "level": "Medium", "q": "At 31 Dec, {exp_lower} of ${small_amt} was still unpaid", "dr": [("{exp}", "small_amt")], "cr": [(f"Accrued {{exp}}", "small_amt")], "analysis": [{"acc": "{exp}", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Accrued Exp", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Accrual Basis: Recording expenses when incurred."},
            {"topic": "Prepayments", "level": "Medium", "q": "Paid ${amt} for {exp_lower}, which includes ${small_amt} for the next year", "dr": [(f"Prepaid {{exp}}", "small_amt"), ("{exp}", "amt - small_amt")], "cr": [("Cash at Bank", "amt")], "analysis": [{"acc": "Prepaid Exp", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "{exp}", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Matching: Portion used is an expense; the rest is an asset."},
            {"topic": "Impairment", "level": "Medium", "q": "A debt of ${small_amt} from {t_ent} is written off as irrecoverable", "dr": [("Impairment Loss", "small_amt")], "cr": [(f"Trade Receivables - {{t_ent}}", "small_amt")], "analysis": [{"acc": "Impairment", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Rec.", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Prudence: Writing off bad debts to avoid overstating assets."},
            {"topic": "Impairment", "level": "Medium", "q": "Allowance for Impairment is adjusted to ${small_amt} (previously ${small_amt_plus_100})", "dr": [("Allowance for Impairment", 100)], "cr": [("Reduction in Allowance", 100)], "analysis": [{"acc": "Allowance", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Reduction Income", "elem": "Other Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Adjustment: A decrease in allowance is treated as other income."},
            {"topic": "Loans", "level": "Medium", "q": "Paid monthly installment: ${amt} principal and ${small_amt} interest", "dr": [("Bank Loan", "amt"), ("Interest Expense", "small_amt")], "cr": [("Cash at Bank", "amt + small_amt")], "analysis": [{"acc": "Bank Loan", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Interest Expense", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Loan: Reducing principal and recording interest expense."},
            {"topic": "Bank Recon", "level": "Medium", "q": "Bank statement shows a credit transfer of ${amt} from {t_ent} not in books", "dr": [("Cash at Bank", "amt")], "cr": [(f"Trade Receivables - {{t_ent}}", "amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Rec.", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Bank Recon: Updating for receipts recorded by the bank first."},
            {"topic": "Bank Recon", "level": "Medium", "q": "A cheque of ${small_amt} received from {t_ent} was returned as dishonoured", "dr": [(f"Trade Receivables - {{t_ent}}", "small_amt")], "cr": [("Cash at Bank", "small_amt")], "analysis": [{"acc": "Trade Rec.", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Dishonoured Cheque: Reversing receipt because payment failed."},
            {"topic": "Concepts", "level": "Medium", "q": "At year-end, a provision for legal claims of ${amt} is created", "dr": [("Legal Expenses", "amt")], "cr": [("Provision for Claims", "amt")], "analysis": [{"acc": "Expenses", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Provision", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Prudence: Recording potential losses immediately."},
            {"topic": "Liabilities", "level": "Medium", "q": "Interest of ${small_amt} on loan incurred but not yet paid", "dr": [("Interest Expense", "small_amt")], "cr": [("Accrued Interest", "small_amt")], "analysis": [{"acc": "Interest Exp", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Accrued Int", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Matching: Interest is an expense of the period incurred."},
            {"topic": "Inventory", "level": "Medium", "q": "Inventory found damaged. Cost ${amt}, but NRV is only ${amt_minus_small_amt}.", "dr": [("Inventory Loss", "small_amt")], "cr": [("Inventory", "small_amt")], "analysis": [{"acc": "Inv Loss", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Inventory", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Prudence: Valuing inventory at lower of Cost and NRV."},
            {"topic": "Control Accounts", "level": "Medium", "q": "Total credit sales from Sales Journal was ${amt}.", "dr": [("Trade Receivables Control", "amt")], "cr": [("Sales Revenue", "amt")], "analysis": [{"acc": "TR Control", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Sales Revenue", "elem": "Revenue", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Control Account: Summarizing total sales from journal into ledger."},
            {"topic": "Inventory", "level": "Medium", "q": "Goods sold at 25% markup. Sales Revenue ${amt}. Record Cost of Sales.", "dr": [("Cost of Sales", "int(amt / 1.25)")], "cr": [("Inventory", "int(amt / 1.25)")], "analysis": [{"acc": "Cost of Sales", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Inventory", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Markup: Calculating Cost of Sales from Sales Revenue."},

            # --- HARD: MASTERY (AO3) ---
            {"topic": "Disposal", "level": "Hard", "q": "An old {ast_lower} (Cost: {amt_x_2}, Acc. Dep: ${amt}) was sold for ${amt} cash", "dr": [("Cash at Bank", "amt"), (f"Accumulated Depreciation - {{ast}}", "amt")], "cr": [(f"Disposal of {{ast}}", "amt * 2")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Accum. Deprec.", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Disposal", "elem": "Asset (Temp)", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Disposal: Removing original cost and accumulated depreciation."},
            {"topic": "Limited Co", "level": "Hard", "q": "The company issued 50,000 ordinary shares for ${amt} cash", "dr": [("Cash at Bank", "amt")], "cr": [("Share Capital", "amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Share Cap", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Equity: Issuing shares provides cash and increases share capital."},
            {"topic": "Errors", "level": "Hard", "q": "A sale of ${amt} to {t_ent} was recorded in {o_ent}'s account by mistake", "dr": [(f"Trade Receivables - {{t_ent}}", "amt")], "cr": [(f"Trade Receivables - {{o_ent}}", "amt")], "analysis": [{"acc": "TR - correct", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "TR - wrong", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Error of Commission: Correcting the specific subsidiary account."},
            {"topic": "Errors", "level": "Hard", "q": "The purchase of {ast_lower} for ${amt} was omitted from the books", "dr": [("{ast}", "amt")], "cr": [("Other Payables", "amt")], "analysis": [{"acc": "{ast}", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Other Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Error of Omission: Recording a forgotten transaction."},
            {"topic": "Disposal", "level": "Hard", "q": "Scrapped an old {ast_lower} (Cost: ${amt}) fully depreciated. No cash.", "dr": [(f"Accumulated Depreciation - {{ast}}", "amt")], "cr": [("{ast}", "amt")], "analysis": [{"acc": "Acc. Deprec.", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "NCA Cost", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Disposal: Scrapping clears cost and full depreciation."},
            {"topic": "Disposal", "level": "Hard", "q": "Traded in an old {ast_lower} (Cost: ${amt}, Acc. Dep: ${small_amt}) for new costing {amt_x_3}", "dr": [(f"{{ast}} (New)", "amt * 3"), (f"Accumulated Depreciation - {{ast}}", "small_amt")], "cr": [(f"{{ast}} (Old)", "amt"), ("Cash at Bank", "amt * 3 - (amt - small_amt)")], "analysis": [{"acc": f"{{ast}} (New)", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Acc. Deprec.", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": f"{{ast}} (Old)", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Trade-in: Using old asset value to offset new asset cost."},
            {"topic": "Control Accounts", "level": "Hard", "q": "A contra entry of ${small_amt} was made between Ledgers.", "dr": [("Trade Payables Control", "small_amt")], "cr": [("Trade Receivables Control", "small_amt")], "analysis": [{"acc": "TP Control", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "TR Control", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Contra: Offsetting receivables and payables for same entity."},
            {"topic": "Limited Co", "level": "Hard", "q": "Directors declared a final ordinary dividend of $50,000.", "dr": [("Retained Earnings", 50000)], "cr": [("Dividends Payable", 50000)], "analysis": [{"acc": "Retained Earn.", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Dividends Pay", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Dividends: Profit distribution reduces Equity and creates liability."},
            {"topic": "Limited Co", "level": "Hard", "q": "Transfer of ${amt} from year's profit to General Reserve.", "dr": [("Retained Earnings", "amt")], "cr": [("General Reserve", "amt")], "analysis": [{"acc": "Retained Earn.", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "General Reserve", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Reserves: Moving profits within Equity."},
            {"topic": "Suspense", "level": "Hard", "q": "Repairs of ${small_amt} entered in Cash Book but omitted from Repairs account.", "dr": [("Repairs Expense", "small_amt")], "cr": [("Suspense Account", "small_amt")], "analysis": [{"acc": "Repairs", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Suspense", "elem": "Temporary", "eff": "N/A", "rule": "Credit"}], "concept": "Suspense: Temporary account for one-sided errors."},
            {"topic": "Suspense", "level": "Hard", "q": "Total of Sales Journal was overcast by ${amt}.", "dr": [("Sales Revenue", "amt")], "cr": [("Suspense Account", "amt")], "analysis": [{"acc": "Sales Revenue", "elem": "Revenue", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Suspense", "elem": "Temporary", "eff": "N/A", "rule": "Credit"}], "concept": "Error Correction: Reducing overstated revenue using suspense."},
            {"topic": "Business Purchase", "level": "Hard", "q": "Purchased business: Assets {amt_x_10}, Liabs {amt_x_2}. Paid {amt_x_9} cheque.", "dr": [("Assets", "amt * 10"), ("Goodwill", "amt")], "cr": [("Liabilities", "amt * 2"), ("Cash at Bank", "amt * 9")], "analysis": [{"acc": "Assets", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Goodwill", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Liabilities", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Goodwill: Intangible asset for extra paid for reputation."}
        ]

    def get_vault(self, category="All", selected_level="Medium"):
        t_ent = random.choice(self.trade_entities)
        o_ent = random.choice(self.other_entities)
        ast = random.choice(self.non_current_assets)
        ast_lower = ast.lower()
        exp = random.choice(self.expenses)
        exp_lower = exp.lower()
        amt = random.randrange(1000, 5000, 100)
        small_amt = random.randrange(50, 400, 10)

        ctx = {
            "amt": amt, "small_amt": small_amt, "amt_x_2": amt * 2, "amt_x_3": amt * 3, 
            "amt_x_5": amt * 5, "amt_x_9": amt * 9, "amt_x_10": amt * 10, 
            "amt_plus_2000": amt + 2000, "amt_minus_small_amt": amt - small_amt, 
            "small_amt_plus_100": small_amt + 100, "int": int
        }

        pool = [q for q in self.vault if q.get('level') == selected_level]
        if category != "All":
            cat_pool = [q for q in pool if q['topic'] == category]
            if cat_pool: pool = cat_pool
        
        if not pool: pool = self.vault
        res = random.choice(pool)

        def clean_text(text):
            if not isinstance(text, str): return text
            return text.format(t_ent=t_ent, o_ent=o_ent, ast=ast, ast_lower=ast_lower, exp=exp, exp_lower=exp_lower, **ctx)

        q_final = clean_text(res['q'])
        dr_final = [(clean_text(name), eval(str(val), {"__builtins__": {}}, ctx)) for name, val in res['dr']]
        cr_final = [(clean_text(name), eval(str(val), {"__builtins__": {}}, ctx)) for name, val in res['cr']]
        
        analysis_final = []
        for item in res.get('analysis', []):
            analysis_final.append({
                "acc": clean_text(item['acc']),
                "elem": item['elem'],
                "eff": item['eff'],
                "rule": item['rule']
            })

        return (q_final, dr_final, cr_final, res['topic'], analysis_final, res['concept'])
