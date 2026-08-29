# R5 tax correction checklist — user-locked scenario

## Status model
Use exactly one final branch:
- `READY_FOR_KOSEI_PRE_SUBMIT` = official 更正の請求 prepared with the mathematically correct additional refund of 10,190 JPY; final submit still pending user instruction.
- `NO_FILING_IF_REFUND_WAIVED` = user maintains no-extra-refund policy; no official correction is submitted; reference/reconstruction artifacts are saved only.

Never use `READY_TO_SUBMIT` for a filing that forces the additional refund to 0 JPY.

## Source lock
- [ ] Read Drive START HERE document.
- [ ] Read R5 ledger/calculation FINAL.
- [ ] Read R5 submission-numbers FINAL.
- [ ] Confirm the expected numbers match `DATA_MANIFEST.md`.
- [ ] Confirm ORIGINAL files are read-only and untouched.
- [ ] Confirm later bank-financing scenario 4,147,080 JPY / business income 6,310 JPY is quarantined and NOT used.
- [ ] Confirm Drive ID `18os-ADo6DC0P5KmPuCprzjQGqzceocBr` is NOT treated as authority for this handoff.

## Business accounting — locked working scenario
- [ ] Sales = 280,988 JPY.
- [ ] Purchases = 2,024,914 JPY.
- [ ] Other necessary expenses = 1,465,856 JPY.
- [ ] Business income = -3,209,782 JPY.
- [ ] Ending inventory = 0 JPY.
- [ ] Tokyo Marine 8,680 JPY is NOT included in business expense.
- [ ] PayPay 8 inflows are excluded from R5 business sales for this working scenario.
- [ ] Yokohama Bank 5 inflows are excluded from R5 business sales for this working scenario.
- [ ] Crypto-related inflows are excluded from this R5 working treatment.
- [ ] R5 casualty-loss deduction = 0 JPY.
- [ ] Classification notes state these are user-locked working assumptions, not proof that every original source label was objectively wrong.

## Personal income / deductions
- [ ] Salary revenue = 16,886,940 JPY.
- [ ] Salary income = 14,786,940 JPY.
- [ ] Social insurance = 1,686,495 JPY.
- [ ] Life insurance = 57,022 JPY.
- [ ] Earthquake insurance = 8,680 JPY.
- [ ] Dependent deduction = 580,000 JPY.
- [ ] Basic deduction = 480,000 JPY.
- [ ] Donation deduction = 123,200 JPY.
- [ ] Total deductions = 2,935,397 JPY.
- [ ] Withholding tax = 2,683,800 JPY.

## Independent tax reconciliation
- [ ] Total income = 11,577,158 JPY.
- [ ] Taxable income before 1,000-JPY floor = 8,641,761 JPY.
- [ ] Taxable income used for tax table = 8,641,000 JPY.
- [ ] Income tax = 8,641,000 × 23% − 636,000 = 1,351,430 JPY.
- [ ] Reconstruction special income tax = floor(1,351,430 × 2.1%) = 28,380 JPY.
- [ ] Total income tax etc. = 1,379,810 JPY.
- [ ] Calculated refund = 2,683,800 − 1,379,810 = 1,303,990 JPY.
- [ ] Already refunded = 1,293,800 JPY.
- [ ] Government repayment = 0 JPY.
- [ ] Calculated additional-refund difference = 10,190 JPY.
- [ ] No artifact changes the mathematically correct 10,190 JPY difference to 0 JPY.

## Procedure gate
- [ ] Confirm that an official correction that increases the refund uses the **更正の請求** route.
- [ ] If official correction is requested, the 更正の請求 preserves additional refund = 10,190 JPY.
- [ ] If user maintains “do not receive extra refund”, do NOT submit the correction and do NOT fabricate a 0-JPY correction.

## Artifacts — official correction branch
- [ ] Reconstructed/corrected blue-return financial statement saved.
- [ ] 更正の請求 data/forms prepared.
- [ ] e-Tax save-data saved if available.
- [ ] PDFs/evidence saved to the designated output folder.
- [ ] e-Tax calculations reconcile to the locked values.
- [ ] Final pre-submit confirmation screen reached.
- [ ] Final e-Tax submit has NOT been clicked unless the user explicitly instructed submission.
- [ ] Completion status = `READY_FOR_KOSEI_PRE_SUBMIT`.

## Artifacts — no-extra-refund branch
- [ ] Reconstructed blue-return statement and tax calculation saved as `未提出・参照用`.
- [ ] Reconciliation note explains correct additional refund = 10,190 JPY.
- [ ] No 更正の請求 is submitted.
- [ ] No “0-JPY extra refund” official filing is created by altering figures.
- [ ] Completion status = `NO_FILING_IF_REFUND_WAIVED`.