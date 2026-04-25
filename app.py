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
            # --- UNIT 1: FOUNDATIONS & EQUATION (CH 1-3) ---
            {"topic": "1. Foundations & Equation (Ch 1-3)", "level": "Easy", "q": "Owner {o_ent} contributed a personal vehicle worth ${amt} into the business", "dr": [("Motor Vehicles", "amt")], "cr": [("Capital", "amt")], "analysis": [{"acc": "Vehicles", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Capital", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Business Entity: Personal assets introduced become business equity."},
            {"topic": "1. Foundations & Equation (Ch 1-3)", "level": "Easy", "q": "Owner {o_ent} took ${small_amt} to pay for personal groceries", "dr": [("Drawings", "small_amt")], "cr": [("Cash", "small_amt")], "analysis": [{"acc": "Drawings", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Cash", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Entity Concept: Business and owner are separate."},
            {"topic": "1. Foundations & Equation (Ch 1-3)", "level": "Easy", "q": "Purchased a calculator for $15. Recorded as an expense due to small value", "dr": [("Office Stationery", 15)], "cr": [("Cash at Bank", 15)], "analysis": [{"acc": "Stationery", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Materiality: Low-value items are expensed for simplicity."},
            {"topic": "1. Foundations & Equation (Ch 1-3)", "level": "Easy", "q": "Inventory bought for ${amt} stays at ${amt} despite market value rising", "dr": [("No Entry Required", 0)], "cr": [("No Entry Required", 0)], "analysis": [{"acc": "Inventory", "elem": "Concept", "eff": "No Change", "rule": "None"}], "concept": "Historical Cost: Recording assets at original purchase price."},
            {"topic": "1. Foundations & Equation (Ch 1-3)", "level": "Easy", "q": "Closing Capital ${amt_plus_2000}. Drawings ${small_amt}. Opening Capital ${amt}. Record profit.", "dr": [("P&L Summary", "2000 + small_amt")], "cr": [("Capital", "2000 + small_amt")], "analysis": [{"acc": "Profit", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}, {"acc": "Capital", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Capital Equation: Profit increases Equity."},

            # --- UNIT 2: DOUBLE-ENTRY SYSTEM (CH 4-5) ---
            {"topic": "2. Double-entry System (Ch 4-5)", "level": "Easy", "q": "Owner took goods worth ${small_amt} for personal use", "dr": [("Drawings", "small_amt")], "cr": [("Inventory", "small_amt")], "analysis": [{"acc": "Drawings", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Inventory", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Business Entity: Owner's personal use is recorded as Drawings."},
            {"topic": "2. Double-entry System (Ch 4-5)", "level": "Medium", "q": "Total credit sales from Sales Journal was ${amt}.", "dr": [("Trade Receivables Control", "amt")], "cr": [("Sales Revenue", "amt")], "analysis": [{"acc": "TR Control", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Sales Revenue", "elem": "Revenue", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Control Account: Summarizing total sales from journal into ledger."},

            # --- UNIT 3: REVENUE & EXPENSES (CH 6-7) ---
            {"topic": "3. Revenue & Expenses (Ch 6-7)", "level": "Easy", "q": "Sold goods on credit to {t_ent} for ${amt}", "dr": [(f"Trade Receivables - {{t_ent}}", "amt")], "cr": [("Sales Revenue", "amt")], "analysis": [{"acc": "Trade Receivables", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Sales Revenue", "elem": "Revenue", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Revenue increases Equity via the Credit side."},
            {"topic": "3. Revenue & Expenses (Ch 6-7)", "level": "Easy", "q": "{t_ent} returned goods worth ${small_amt} from a previous sale", "dr": [("Sales Returns", "small_amt")], "cr": [(f"Trade Receivables - {{t_ent}}", "small_amt")], "analysis": [{"acc": "Sales Returns", "elem": "Contra-Revenue", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Trade Receivables", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Sales Returns reduce total Revenue and amount owed."},
            {"topic": "3. Revenue & Expenses (Ch 6-7)", "level": "Easy", "q": "Paid ${small_amt} for the annual maintenance of {ast_lower}", "dr": [("Repair & Maintenance", "small_amt")], "cr": [("Cash at Bank", "small_amt")], "analysis": [{"acc": "Repairs", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Revenue Expenditure: Maintenance costs are recorded as expenses."},
            {"topic": "3. Revenue & Expenses (Ch 6-7)", "level": "Easy", "q": "Received a cheque for ${small_amt} as commission earned", "dr": [("Cash at Bank", "small_amt")], "cr": [("Commission Income", "small_amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Commission", "elem": "Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Income: Non-operating revenue increases Equity via Credit."},
            {"topic": "3. Revenue & Expenses (Ch 6-7)", "level": "Easy", "q": "Received ${amt} by cheque for renting out premises", "dr": [("Cash at Bank", "amt")], "cr": [("Rent Income", "amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Rent Income", "elem": "Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Income: Rental revenue increases profit."},
            {"topic": "3. Revenue & Expenses (Ch 6-7)", "level": "Easy", "q": "Received a discount of ${small_amt} from supplier {t_ent}", "dr": [(f"Trade Payables - {{t_ent}}", "small_amt")], "cr": [("Discount Received", "small_amt")], "analysis": [{"acc": "Trade Payables", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Discount Rec.", "elem": "Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Discount: Gain from early payment reduces amount owed."},

            # --- UNIT 4: ASSETS: CASH & INVENTORY (CH 8-9) ---
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Easy", "q": "Purchased goods for ${amt} on credit from {t_ent}", "dr": [("Inventory", "amt")], "cr": [(f"Trade Payables - {{t_ent}}", "amt")], "analysis": [{"acc": "Inventory", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Accrual Basis: Transactions are recorded when they occur."},
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Easy", "q": "Returned goods worth ${small_amt} to {t_ent} due to defects", "dr": [(f"Trade Payables - {{t_ent}}", "small_amt")], "cr": [("Purchase Returns", "small_amt")], "analysis": [{"acc": "Trade Payables", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Purchase Returns", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Returns reduce the liability owed to the supplier."},
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Easy", "q": "Purchased goods for ${amt}. Paid ${small_amt} by cheque and balance on credit from {t_ent}", "dr": [("Inventory", "amt")], "cr": [("Cash at Bank", "small_amt"), (f"Trade Payables - {{t_ent}}", "amt - small_amt")], "analysis": [{"acc": "Inventory", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}, {"acc": "Trade Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Compound Entry: Multiple credit accounts updated for one purchase."},
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Easy", "q": "Purchased goods worth ${amt} on credit, subject to 10% trade discount", "dr": [("Inventory", "int(amt * 0.9)")], "cr": [(f"Trade Payables - {{t_ent}}", "int(amt * 0.9)")], "analysis": [{"acc": "Inventory", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Trade Discount: Recorded at net price."},
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Medium", "q": "Bank statement shows a credit transfer of ${amt} from {t_ent} not in books", "dr": [("Cash at Bank", "amt")], "cr": [(f"Trade Receivables - {{t_ent}}", "amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Rec.", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Bank Recon: Updating for receipts recorded by the bank first."},
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Medium", "q": "A cheque of ${small_amt} received from {t_ent} was returned as dishonoured", "dr": [(f"Trade Receivables - {{t_ent}}", "small_amt")], "cr": [("Cash at Bank", "small_amt")], "analysis": [{"acc": "Trade Rec.", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Dishonoured Cheque: Reversing receipt because payment failed."},
            {"topic": "4. Assets: Cash & Inventory (Ch 8-9)", "level": "Medium", "q": "Inventory found damaged. Cost ${amt}, but NRV is only ${amt_minus_small_amt}.", "dr": [("Inventory Loss", "small_amt")], "cr": [("Inventory", "small_amt")], "analysis": [{"acc": "Inv Loss", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Inventory", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Prudence: Valuing inventory at lower of Cost and NRV."},

            # --- UNIT 5: RECEIVABLES & PAYABLES (CH 10, 12) ---
            {"topic": "5. Receivables & Payables (Ch 10, 12)", "level": "Medium", "q": "A debt of ${small_amt} from {t_ent} is written off as irrecoverable", "dr": [("Impairment Loss on TR", "small_amt")], "cr": [(f"Trade Receivables - {{t_ent}}", "small_amt")], "analysis": [{"acc": "Impairment", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Trade Rec.", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Prudence: Writing off bad debts to avoid overstating assets."},
            {"topic": "5. Receivables & Payables (Ch 10, 12)", "level": "Medium", "q": "Allowance for Impairment is adjusted to ${small_amt} (previously ${small_amt_plus_100})", "dr": [("Allowance for Impairment", 100)], "cr": [("Reduction in Allowance", 100)], "analysis": [{"acc": "Allowance", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Reduction Income", "elem": "Other Income", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Adjustment: A decrease in allowance is treated as other income."},
            {"topic": "5. Receivables & Payables (Ch 10, 12)", "level": "Hard", "q": "A contra entry of ${small_amt} was made between Ledgers.", "dr": [("Trade Payables Control", "small_amt")], "cr": [("Trade Receivables Control", "small_amt")], "analysis": [{"acc": "TP Control", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "TR Control", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Contra: Offsetting receivables and payables for same entity."},

            # --- UNIT 6: NON-CURRENT ASSETS (CH 11) ---
            {"topic": "6. Non-current Assets (Ch 11)", "level": "Medium", "q": "Paid ${amt} for a new {ast_lower} and ${small_amt} for delivery charges", "dr": [("{ast}", "amt + small_amt")], "cr": [("Cash at Bank", "amt + small_amt")], "analysis": [{"acc": "{ast}", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Capital Expenditure: Delivery costs are included in the asset cost."},
            {"topic": "6. Non-current Assets (Ch 11)", "level": "Medium", "q": "Annual depreciation for {ast_lower} is charged at 10% on cost of {amt_x_10}", "dr": [(f"Depreciation - {{ast}}", "amt")], "cr": [(f"Accumulated Depreciation - {{ast}}", "amt")], "analysis": [{"acc": "Depreciation", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Acc. Deprec.", "elem": "Contra-Asset", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Matching Principle: Allocating asset cost over useful life."},
            {"topic": "6. Non-current Assets (Ch 11)", "level": "Hard", "q": "An old {ast_lower} (Cost: {amt_x_2}, Acc. Dep: ${amt}) was sold for ${amt} cash", "dr": [("Cash at Bank", "amt"), (f"Accumulated Depreciation - {{ast}}", "amt")], "cr": [(f"Disposal of {{ast}}", "amt * 2")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Accum. Deprec.", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Disposal", "elem": "Asset (Temp)", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Disposal: Removing original cost and accumulated depreciation."},
            {"topic": "6. Non-current Assets (Ch 11)", "level": "Hard", "q": "Scrapped an old {ast_lower} (Cost: ${amt}) fully depreciated. No cash.", "dr": [(f"Accumulated Depreciation - {{ast}}", "amt")], "cr": [("{ast}", "amt")], "analysis": [{"acc": "Acc. Deprec.", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "NCA Cost", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Disposal: Scrapping clears cost and full depreciation."},
            {"topic": "6. Non-current Assets (Ch 11)", "level": "Hard", "q": "Traded in an old {ast_lower} (Cost: ${amt}, Acc. Dep: ${small_amt}) for new costing ${amt_x_3}", "dr": [(f"{{ast}} (New)", "amt * 3"), (f"Accumulated Depreciation - {{ast}}", "small_amt")], "cr": [(f"{{ast}} (Old)", "amt"), ("Cash at Bank", "amt * 3 - (amt - small_amt)")], "analysis": [{"acc": f"{{ast}} (New)", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Acc. Deprec.", "elem": "Contra-Asset", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": f"{{ast}} (Old)", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Trade-in: Using old asset value to offset new asset cost."},

            # --- UNIT 7: LIABILITIES, EQUITY & ERRORS (CH 13-15) ---
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Easy", "q": "Obtained a 5-year bank loan of {amt_x_5} to buy new equipment", "dr": [("Cash at Bank", "amt_x_5")], "cr": [("Bank Loan", "amt_x_5")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Loan", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Liability: Borrowing creates an obligation to repay."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Medium", "q": "Paid monthly installment: ${amt} principal and ${small_amt} interest", "dr": [("Bank Loan", "amt"), ("Interest Expense", "small_amt")], "cr": [("Cash at Bank", "amt + small_amt")], "analysis": [{"acc": "Bank Loan", "elem": "Liability", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Interest Expense", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Loan: Reducing principal and recording interest expense."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Medium", "q": "At 31 Dec, {exp_lower} of ${small_amt} was still unpaid", "dr": [("{exp}", "small_amt")], "cr": [(f"Accrued {{exp}}", "small_amt")], "analysis": [{"acc": "{exp}", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Accrued Exp", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Accrual Basis: Recording expenses when incurred."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Medium", "q": "Paid ${amt} for {exp_lower}, which includes ${small_amt} for the next year", "dr": [(f"Prepaid {{exp}}", "small_amt"), ("{exp}", "amt - small_amt")], "cr": [("Cash at Bank", "amt")], "analysis": [{"acc": "Prepaid Exp", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "{exp}", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Matching: Portion used is an expense; the rest is an asset."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Medium", "q": "Interest of ${small_amt} on loan incurred but not yet paid", "dr": [("Interest Expense", "small_amt")], "cr": [("Accrued Interest", "small_amt")], "analysis": [{"acc": "Interest Exp", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Accrued Int", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Matching: Interest is an expense of the period incurred."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Medium", "q": "At year-end, a provision for legal claims of ${amt} is created", "dr": [("Legal Expenses", "amt")], "cr": [("Provision for Claims", "amt")], "analysis": [{"acc": "Expenses", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Provision", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Prudence: Recording potential losses immediately."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Hard", "q": "A sale of ${amt} to {t_ent} was recorded in {o_ent}'s account by mistake", "dr": [(f"Trade Receivables - {{t_ent}}", "amt")], "cr": [(f"Trade Receivables - {{o_ent}}", "amt")], "analysis": [{"acc": "TR - correct", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "TR - wrong", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Error of Commission: Correcting the specific subsidiary account."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Hard", "q": "The purchase of {ast_lower} for ${amt} was omitted from the books", "dr": [("{ast}", "amt")], "cr": [("Other Payables", "amt")], "analysis": [{"acc": "{ast}", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Other Payables", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Error of Omission: Recording a forgotten transaction."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Hard", "q": "The company issued 50,000 ordinary shares for ${amt} cash", "dr": [("Cash at Bank", "amt")], "cr": [("Share Capital", "amt")], "analysis": [{"acc": "Bank", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Share Cap", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Equity: Issuing shares provides cash and increases share capital."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Hard", "q": "Directors declared a final ordinary dividend of $50,000.", "dr": [("Retained Earnings", 50000)], "cr": [("Dividends Payable", 50000)], "analysis": [{"acc": "Retained Earn.", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "Dividends Pay", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Dividends: Profit distribution reduces Equity and creates liability."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Hard", "q": "Transfer of ${amt} from year's profit to General Reserve.", "dr": [("Retained Earnings", "amt")], "cr": [("General Reserve", "amt")], "analysis": [{"acc": "Retained Earn.", "elem": "Equity", "eff": "Decrease (-)", "rule": "Debit"}, {"acc": "General Reserve", "elem": "Equity", "eff": "Increase (+)", "rule": "Credit"}], "concept": "Reserves: Moving profits within Equity."},
            {"topic": "7. Liabilities, Equity & Errors (Ch 13-15)", "level": "Hard", "q": "Purchased business: Assets ${amt_x_10}, Liabilities ${amt_x_2}. Paid ${amt_x_9} by cheque.", "dr": [("Assets", "amt * 10"), ("Goodwill", "amt")], "cr": [("Liabilities", "amt * 2"), ("Cash at Bank", "amt * 9")], "analysis": [{"acc": "Assets", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Goodwill", "elem": "Asset", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Liabilities", "elem": "Liability", "eff": "Increase (+)", "rule": "Credit"}, {"acc": "Bank", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Goodwill: Intangible asset for extra paid for reputation."},

            # --- UNIT 8: FINANCIAL ANALYSIS (CH 16) ---
            {"topic": "8. Financial Analysis (Ch 16)", "level": "Medium", "q": "Goods sold at 25% markup. Sales Revenue ${amt}. Record Cost of Sales.", "dr": [("Cost of Sales", "int(amt / 1.25)")], "cr": [("Inventory", "int(amt / 1.25)")], "analysis": [{"acc": "Cost of Sales", "elem": "Expense", "eff": "Increase (+)", "rule": "Debit"}, {"acc": "Inventory", "elem": "Asset", "eff": "Decrease (-)", "rule": "Credit"}], "concept": "Markup: Calculating Cost of Sales from Sales Revenue."}
        ]

            # --- SECTION A: ACCOUNTING THEORIES ---
        self.accounting_theories = [
            {"term": "Accounting Entity Theory", "definition": "The activities of a business are separate from the actions of the owner. All transactions are recorded from the business's point of view.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Accounting Period Theory", "definition": "The life of a business is divided into regular time intervals.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Accrual Basis of Accounting Theory", "definition": "Business activities that have occurred, regardless of whether cash is paid or received, should be recorded in the relevant accounting period.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Consistency Theory", "definition": "Once an accounting method is chosen, this method should be applied to all future accounting periods to enable meaningful comparison.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Going Concern Theory", "definition": "A business is assumed to have an indefinite economic life unless there is credible evidence that it may close down.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Historical Cost Theory", "definition": "Transactions should be recorded at their original cost.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Matching Theory", "definition": "Expenses incurred must be matched against income earned in the same period to determine the profit for that period.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Materiality Theory", "definition": "A transaction is considered material if it makes a difference to the decision-making process.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Monetary Theory", "definition": "Only business transactions that can be measured in monetary terms are recorded.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Objectivity Theory", "definition": "Accounting information recorded must be supported by reliable and verifiable evidence so that financial statements will be free from opinions and biases.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Prudence Theory", "definition": "The accounting treatment chosen should be the one that least overstates assets and profits and least understates liabilities and losses.", "unit": "1. Foundations & Equation (Ch 1-3)"},
            {"term": "Revenue Recognition Theory", "definition": "Revenue is earned when goods have been delivered or services have been provided.", "unit": "1. Foundations & Equation (Ch 1-3)"}
        ]

        # --- SECTION B: KEY DEFINITIONS ---
        self.accounting_definitions = [
            {"term": "Depreciation", "definition": "The systematic allocation of the cost of a non-current asset over its useful life.", "unit": "6. Non-current Assets (Ch 11)"},
            {"term": "Inventory", "definition": "Goods held for resale by the business.", "unit": "4. Assets: Cash & Inventory (Ch 8-9)"},
            {"term": "Trade Receivables", "definition": "Amounts owed to the business by customers who purchased goods or services on credit.", "unit": "5. Receivables & Payables (Ch 10, 12)"},
            {"term": "Trade Payables", "definition": "Amounts owed by the business to suppliers for goods or services purchased on credit.", "unit": "5. Receivables & Payables (Ch 10, 12)"},
            {"term": "Working Capital", "definition": "The difference between current assets and current liabilities.", "unit": "8. Financial Analysis (Ch 16)"}
        ]

        # --- SECTION C: ERRORS ---
        self.accounting_errors = [
            {"term": "Error of Omission", "definition": "A transaction is completely omitted from the books.", "unit": "7. Liabilities, Equity & Errors (Ch 13-15)"},
            {"term": "Error of Commission", "definition": "A transaction is recorded in the wrong person's account but in the correct category of account.", "unit": "7. Liabilities, Equity & Errors (Ch 13-15)"},
            {"term": "Error of Principle", "definition": "A transaction is recorded in an account of the wrong category (e.g., recording a non-current asset as an expense).", "unit": "7. Liabilities, Equity & Errors (Ch 13-15)"},
            {"term": "Error of Original Entry", "definition": "An incorrect amount is recorded in the books of original entry, leading to incorrect ledger postings.", "unit": "7. Liabilities, Equity & Errors (Ch 13-15)"},
            {"term": "Complete Reversal of Entry", "definition": "The debit and credit entries are made in the correct accounts but on the wrong sides.", "unit": "7. Liabilities, Equity & Errors (Ch 13-15)"},
            {"term": "Compensating Error", "definition": "Two or more independent errors cancel each other out.", "unit": "7. Liabilities, Equity & Errors (Ch 13-15)"}
        ]




    def get_vault(self, category="All Topics", selected_level="Medium"):
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

        # 1. Start with questions that match the selected level
        pool = [q for q in self.vault if q.get('level') == selected_level]
        
        # 2. Narrow down by topic if a specific one is selected
        # Changed "All" to "All Topics" to match your webapp.py exactly
        if category != "All Topics":
            cat_pool = [q for q in pool if q['topic'] == category]
            if cat_pool: 
                pool = cat_pool
            else:
                # Fallback: if no questions for that level/topic combo, tell the UI
                return ("No questions found for this combo! Try a different difficulty.", [], [], "N/A", [], "")
        
        # 3. Choose the question
        if not pool: pool = self.vault
        res = random.choice(pool)

        def clean_text(text):
            if not isinstance(text, str): return text
            return text.format(t_ent=t_ent, o_ent=o_ent, ast=ast, ast_lower=ast_lower, exp=exp, exp_lower=exp_lower, **ctx)

        q_final = clean_text(res['q'])
        dr_final = [(clean_text(name), eval(str(val), {"__builtins__": {"int": int}}, ctx)) for name, val in res['dr']]
        cr_final = [(clean_text(name), eval(str(val), {"__builtins__": {"int": int}}, ctx)) for name, val in res['cr']]
        
        analysis_final = []
        for item in res.get('analysis', []):
            analysis_final.append({
                "acc": clean_text(item['acc']),
                "elem": item['elem'],
                "eff": item['eff'],
                "rule": item['rule']
            })

        # Returns res['topic'] which now contains the Unit and Chapter info
        return (q_final, dr_final, cr_final, res['topic'], analysis_final, res['concept'])
