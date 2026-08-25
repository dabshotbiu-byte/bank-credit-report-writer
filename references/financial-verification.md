# Financial and bank-flow verification

## Scope control

Label every number with entity scope, period, currency and unit. Do not compare consolidated revenue with parent-company tax or bank data without a bridge. Tie opening balances to the prior closing balance and document audit adjustments.

## Material-account selection

Analyze an account when any of the following applies:

- It is among the five largest asset, liability, revenue, cost, expense or cash-flow items.
- It is at least 10% of total assets, liabilities, revenue or cost.
- Its absolute movement is at least 30% and financially meaningful.
- It involves a related party, aging, impairment, restriction, financing, unusual contra entry or off-balance-sheet exposure.
- It is important to the operating model even if not large, such as contract assets, prepayments, inventory, R&D capitalization, deferred revenue or platform receivables.

For each selected account provide multi-period balance/movement, share, change, business reason, top-five detail with amount/share/age/terms, subsequent settlement or realization, counterparty quality, accounting treatment, risk and conclusion. Obtain detail from the trial balance or subledger. “经营团队已核实无误” alone is not an analysis.

## Bank receipt classification

Build a complete account list first. Normalize dates, amounts, signs, counterparty names, account numbers, purpose and remarks. De-duplicate overlapping exports and identify payment-platform gross/net settlement.

Classify receipts into:

- Verified sales receipts
- Candidate sales receipts requiring contract/invoice/customer support
- Internal account transfer
- Loan, bill discounting or other financing
- Equity contribution or shareholder/related-party funding
- Wealth-management redemption/principal
- Interest
- Tax refund, subsidy or government grant
- Refund/reversal
- Deposit, guarantee money or other non-revenue receipt
- Unclassified

Do not treat cash deposits, controller transfers, related-party receipts, round-number credits, or “往来款” as sales without transaction evidence. Do not double-count a platform-to-bank settlement and its underlying customer transactions. Negative/reversal entries should offset their linked receipt.

The report table should show:

| Item | Amount | Transactions | Treatment |
|---|---:|---:|---|
| Total credits imported | | | Starting population |
| Less: non-sales categories | | | List each category |
| Candidate sales pending support | | | Excluded from verified sales until supported |
| Verified sales receipts | | | Numerator |
| Financial-statement revenue | | | Same scope/period |
| Verification ratio | | | Verified receipts / revenue |
| Difference | | | Explain timing, VAT, AR, advance or scope |

Review `scripts/review_bank_flows.py` output before using it. Keyword classification is a workpaper accelerator, not evidence.

## Revenue triangulation

Reconcile financial-statement revenue to VAT returns, CIT returns, invoice ledger and verified receipts. Explain differences through VAT, opening/closing receivables, advances/contract liabilities, unbilled revenue, foreign exchange, returns, platform deductions and entity scope. Use contracts, invoices, delivery/acceptance and subsequent receipts for a sample concentrated on top customers, large amounts, related parties, year-end entries and unusual descriptions.

## Downside case and repayment

Build a transparent downside case from operational drivers rather than applying an unexplained haircut. State assumptions for price, volume, gross margin, collection days, inventory days, supplier terms, fixed expenses, capex, debt service and confirmed financing. Do not count an unsigned financing round, unapproved grant, unsupported asset sale or undrawn facility as certain cash. Show opening cash, operating cash generation/use, financing, debt service and closing liquidity.
