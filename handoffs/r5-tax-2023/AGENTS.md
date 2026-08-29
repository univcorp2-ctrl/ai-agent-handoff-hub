# R5 tax 2023 — path-scoped agent rules

These rules apply only under `handoffs/r5-tax-2023/`.

## Status
`READY_FOR_CODEX_PREP / FINAL_SUBMIT_ROUTE_GATED`

## Goal
Prepare and reconcile the Japanese R5 (2023) user-locked tax working scenario from the designated Drive source of truth. Complete all reversible work. Never submit a filing that changes the mathematically correct additional refund of 10,190 JPY to zero.

## Source-of-truth priority for THIS task
1. `CODEX_TASK.md`
2. Drive `START_HERE_R5_CODEX申告指示`
3. `DATA_MANIFEST.md`
4. The two designated FINAL Excel files in Drive
5. Original source documents in ORIGINAL for transcription/evidence
6. Other R5/R6/R7 audit or bank-financing workbooks only as provenance; they are NOT input authorities for this task.

## Critical conflict quarantine
Later bank-financing artifacts contain a different R5 scenario: business sales 4,147,080 JPY and business income 6,310 JPY, created by restoring PayPay 8 inflows (2,806,000 JPY) and four Yokohama Bank inflows (1,060,092 JPY) as sales. They must not override the current user-locked tax scenario.

In particular, do NOT use `02_R5_税務監査正本_修正版_HOLD_20260829` (Drive ID `18os-ADo6DC0P5KmPuCprzjQGqzceocBr`) or any workbook saying the 280,988 JPY scenario is forbidden as the input source for this Codex task.

## Locked working classifications
Do not reopen these unless the user explicitly changes them:
- PayPay 8 inflows / 2,806,000 JPY: excluded from R5 business sales for this working scenario.
- Yokohama Bank 5 inflows / 1,680,378 JPY: excluded from R5 business sales for this working scenario.
- Crypto-related inflows: excluded from this R5 working treatment.
- Tokyo Marine 8,680 JPY: removed from business expense to avoid double counting with earthquake-insurance deduction.
- Ending inventory: 0 JPY.
- R5 casualty-loss deduction: 0 JPY; theft belongs to 2024-side handling.

These classifications are user-locked working assumptions. They are not proof that the underlying source labels were objectively wrong; preserve that distinction in any formal explanation.

## Tax-procedure gate
Under the locked calculations, the corrected refund is 1,303,990 JPY versus 1,293,800 JPY already refunded: an additional 10,190 JPY.

Therefore:
- If the user wants the official R5 filing corrected, use the **更正の請求** route and preserve the correct 10,190 JPY additional refund result.
- If the user maintains the policy of not receiving the additional refund, do **not** submit a correction. Prepare only clearly labeled `未提出・参照用` reconstructed forms and reconciliation artifacts.
- Never fabricate an official correction with an additional refund of 0 JPY.

## Safety / non-goals
- Never edit ORIGINAL source files.
- Do not mix R6/R7 values into R5.
- Do not let later bank-financing scenarios override this task's authority chain.
- Never click irreversible e-Tax final submit without explicit user instruction.
- Do not stop for a question if the answer is already in the designated source-of-truth files.

## Acceptance
- Locked R5 calculations independently reconciled.
- If official-correction branch: 更正の請求 data/forms prepared and e-Tax auto-calculation reconciled to the 10,190 JPY additional refund.
- If no-refund branch: reconstructed reference forms saved as `未提出・参照用`; no filing is submitted.
- Generated artifacts stored in the designated Drive output folder.
- Final submission remains gated by the rules above.