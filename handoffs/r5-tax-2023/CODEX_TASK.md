# Codex task — R5 e-Tax filing preparation

**Status:** READY_FOR_CODEX  
**Scope:** Japanese individual income tax, R5 / 2023 only.  
**Human action left:** irreversible final e-Tax submission only.

## Start here
Read this Drive document first and follow it as the execution contract:
https://docs.google.com/document/d/1bHKK2EdvF8i1WZXKFLsnfD-onS42kV33q6e-44gcAes/edit

Then read:
- `AGENTS.md`
- `DATA_MANIFEST.md`
- `SUBMISSION_CHECKLIST.md`

## Goal
Use the current R5 FINAL source files to prepare the formal R5 tax return / blue-return financial statement, enter them into e-Tax, reconcile automatic calculations, save all formal artifacts to Drive, and navigate to the final pre-submit confirmation screen.

Do not ask the user to repeat classifications already locked in the source. Do not re-open PayPay, Yokohama Bank, or crypto treatment. Do not use old Notion intermediate values as current inputs.

## Required sequence
1. Read both current FINAL Excel files from Drive.
2. Validate their summary values against `DATA_MANIFEST.md`.
3. Read the official reissued withholding statement and the original R5 return / blue-return statement from ORIGINAL for identity and source fields.
4. Open the appropriate R5 e-Tax correction/filing workflow.
5. Build the corrected blue-return financial statement using the locked business values.
6. Enter salary, business income, deductions, withholding, and other required R5 fields.
7. Compare every material e-Tax auto-calculated field with the locked expected values.
8. If a discrepancy appears, diagnose the exact field and resolve it from the current source-of-truth files. Do **not** resolve it by reclassifying PayPay/Yokohama/crypto or resurrecting Tokyo Marine 8,680 JPY as a business expense.
9. Save generated PDFs, save-data, and any confirmation artifact into the formal-forms Drive folder.
10. Advance to the final pre-submit confirmation screen.
11. Stop there unless the user explicitly instructs final submission.

## Expected values for reconciliation
- Business sales: 280,988 JPY
- Purchases: 2,024,914 JPY
- Other expenses: 1,465,856 JPY
- Business income: -3,209,782 JPY
- Total income: 11,577,158 JPY
- Total deductions: 2,935,397 JPY
- Taxable income: 8,641,000 JPY
- Income tax: 1,351,430 JPY
- Reconstruction special income tax: 28,380 JPY
- Income tax etc. total: 1,379,810 JPY
- Withholding: 2,683,800 JPY
- Calculated refund: 1,303,990 JPY
- Already refunded: 1,293,800 JPY
- Government repayment: 0 JPY
- Calculated additional-refund difference: 10,190 JPY
- Additional refund claim: 0 JPY per locked user working policy

## Output destination
https://drive.google.com/drive/folders/1l9lcOVBBibwwcgzz_TyMDcz0HxUGD2aB

## Completion report
Report only:
1. formal forms created,
2. Drive locations,
3. e-Tax auto-calculation reconciliation result,
4. whether final pre-submit screen was reached,
5. `FINAL_SUBMIT_PENDING_USER_INSTRUCTION` if not yet submitted.

Do not call the task complete if the formal forms are not saved or if e-Tax reconciliation has not been performed.