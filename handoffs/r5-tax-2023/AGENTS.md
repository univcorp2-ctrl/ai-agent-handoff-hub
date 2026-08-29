# R5 tax 2023 — path-scoped agent rules

These rules apply only under `handoffs/r5-tax-2023/`.

## Goal
Prepare the Japanese R5 (2023) individual income-tax correction/filing package from the locked Drive source of truth, complete all reversible work, and stop only before irreversible e-Tax submission unless the user explicitly instructs `申告して` / `送信して`.

## Source of truth priority
1. `CODEX_TASK.md`
2. Drive `START_HERE_R5_CODEX申告指示`
3. `DATA_MANIFEST.md`
4. Current FINAL Excel files in Drive
5. Original source documents in the ORIGINAL folder
6. Audit/history only for provenance — never use old intermediate values as current inputs

## Locked working classifications
Do not reopen or relitigate these unless the user explicitly changes them:
- PayPay 8 inflows / 2,806,000 JPY: exclude from R5 business sales.
- Yokohama Bank 5 inflows / 1,680,378 JPY: exclude from R5 business sales.
- Crypto-related inflows: exclude from this R5 working treatment.
- Tokyo Marine 8,680 JPY: remove from business expense to avoid double counting with earthquake insurance deduction.
- Ending inventory: 0 JPY.
- R5 casualty-loss deduction: 0 JPY; theft belongs to 2024-side handling.
- Additional refund: do not claim; preserve the calculated 10,190 JPY difference as an internal calculation note.

## Safety / non-goals
- Never edit ORIGINAL source files.
- Do not mix R6/R7 values into R5.
- Do not change locked classifications just because older logs differ.
- Never click irreversible e-Tax final submit without explicit user instruction.
- Do not stop for a question if the answer is already in the source-of-truth files.

## Acceptance
- Formal R5 return / blue-return statement prepared.
- e-Tax automatic calculations reconciled to the locked source values or every difference fully explained and resolved.
- Generated PDF/save-data stored in the designated Drive output folder.
- Browser/e-Tax flow advanced to the final pre-submit confirmation screen.
- Final submit remains pending explicit user command.