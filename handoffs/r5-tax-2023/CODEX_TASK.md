# Codex task — R5 tax correction preparation

**Status:** READY_FOR_CODEX_PREP / FINAL_SUBMIT_ROUTE_GATED  
**Scope:** Japanese individual income tax, R5 / 2023 only.

## Start here
Read this Drive document first and treat it as the execution contract:
https://docs.google.com/document/d/1bHKK2EdvF8i1WZXKFLsnfD-onS42kV33q6e-44gcAes/edit

Then read:
- `AGENTS.md`
- `DATA_MANIFEST.md`
- `SUBMISSION_CHECKLIST.md`

## Critical authority rule
For this task, the user-locked tax working scenario is:
- Business sales: 280,988 JPY
- Purchases: 2,024,914 JPY
- Other expenses: 1,465,856 JPY
- Business income: -3,209,782 JPY

A later bank-financing scenario uses sales 4,147,080 JPY and business income 6,310 JPY by restoring PayPay and four Yokohama Bank inflows. That is a different scenario. Do not use it for this task. Do not use Drive ID `18os-ADo6DC0P5KmPuCprzjQGqzceocBr` as the authority for this task.

Do not ask the user to repeat classifications already locked here. Do not re-open PayPay, Yokohama Bank, or crypto treatment unless the user explicitly changes the instruction.

## Required sequence
1. Read both designated FINAL Excel files from Drive.
2. Validate their summary values against `DATA_MANIFEST.md`.
3. Read the reissued withholding statement and original R5 return / blue-return statement from ORIGINAL for source fields.
4. Independently recompute the material R5 tax figures.
5. Use the R5 **更正の請求** workflow for an official correction, because the locked scenario produces a larger refund than the filed return.
6. Build/reconstruct the blue-return financial statement using the locked business values.
7. Enter salary, business income, deductions, withholding, and other required R5 fields and compare e-Tax automatic calculations with the expected values.
8. If a discrepancy appears, diagnose the exact field from the designated source files. Do not resolve it by restoring the bank-financing scenario or by reclassifying PayPay/Yokohama/crypto.
9. Save PDFs/save-data/reconciliation artifacts into the output folder.
10. Apply the submission branch below.

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

## Submission branch — mandatory
### A. Official correction requested
Prepare the **更正の請求** with the correct additional refund of 10,190 JPY. Advance to final pre-submit confirmation. Do not click final submit without an explicit user instruction.

### B. User maintains “do not receive the extra refund”
Do not submit a correction and do not change 10,190 JPY to 0. Save reconstructed forms and reconciliation outputs clearly labeled `未提出・参照用`, then stop with `NO_FILING_IF_REFUND_WAIVED`.

## Output destination
https://drive.google.com/drive/folders/1l9lcOVBBibwwcgzz_TyMDcz0HxUGD2aB

## Completion report
Report only:
1. artifacts created,
2. Drive locations,
3. independent/e-Tax reconciliation result,
4. which submission branch applies,
5. `FINAL_SUBMIT_PENDING_USER_INSTRUCTION` or `NO_FILING_IF_REFUND_WAIVED`.

Do not call an official filing ready if the procedure/result has been altered merely to force the additional refund to zero.