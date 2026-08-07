# ACCEPTANCE CRITERIA

This checklist is the release gate for the next AI agent. A checked box requires evidence, not a narrative claim.

## A. Commercial readiness

- [ ] The target customer is specific enough to identify ten real studios.
- [ ] `sales/OFFER_EN.md` states audience, problem, seven-day scope, deliverables, exclusions, price hypothesis, CTA, and data needed.
- [ ] A Japanese equivalent exists for internal review.
- [ ] Delivery template and intake form exist.
- [ ] No claim promises guaranteed revenue, retention, ranking, or Japan-market success.
- [ ] Test price is labelled as a hypothesis, not a market fact.
- [ ] Payment/refund/contract language is marked draft pending actual transaction review.

## B. Prospect evidence

- [ ] 30 prospects have real Experience and creator/studio URLs.
- [ ] Every prospect has a checked-at timestamp.
- [ ] Every prospect has a real contact channel or `unverified`.
- [ ] No guessed email address is represented as verified.
- [ ] Japanese support state is based on direct observation.
- [ ] Each TOP10 prospect has one specific observable issue.
- [ ] TOP3 have a one-page sample audit.
- [ ] Duplicate studios/Experiences are removed.

## C. Outreach quality

- [ ] Messages are sent in three waves of at most ten.
- [ ] Every message includes the exact Experience name and one specific observation.
- [ ] Maker and Checker roles are different contexts/agents.
- [ ] Checker verifies recipient, factual observation, promise, price, attachments, CTA, and personal data.
- [ ] Send log records date/time, channel, recipient, message version, result, and follow-up date.
- [ ] Bulk spam, scraped personal contacts, and unsupported pressure tactics are absent.

## D. Plugin v0.1

- [ ] Plugin uses no remote code loading or obfuscation.
- [ ] Plugin makes no external network request.
- [ ] Plugin is read-only against the scanned DataModel.
- [ ] Toolbar button opens/closes a DockWidget.
- [ ] Scanner detects non-empty TextLabel, TextButton, and TextBox text.
- [ ] Scanner returns deterministic normalized records.
- [ ] Instance paths are stable and human-readable.
- [ ] CSV escapes commas, quotes, CR/LF, and Unicode.
- [ ] Long-text and AutoLocalize warnings have documented thresholds/logic.
- [ ] Empty strings are excluded or explicitly categorized.
- [ ] Scanner, rules, and CSV logic are separated from UI.
- [ ] README includes install, use, privacy, known limits, uninstall, and test instructions.

## E. Tests

Required deterministic tests:

1. plain text record
2. empty string
3. embedded comma
4. embedded double quote
5. newline and Japanese Unicode
6. long text boundary below/equal/above threshold
7. AutoLocalize enabled/disabled
8. unsupported object ignored
9. duplicate text in different paths retained separately
10. scan failure handled without corrupting output

- [ ] Lint passes.
- [ ] Unit tests pass.
- [ ] Manual Studio smoke test is documented with screenshot or exact result log.
- [ ] CI result URL is recorded.
- [ ] No secret-like values appear in repository history or logs.

## F. Creator Store readiness

Before public submission, re-check official current documentation.

- [ ] Seller onboarding status is recorded as Pending/Success/blocked, without sensitive information.
- [ ] Seller-owned individual asset requirement is satisfied.
- [ ] Asset Privacy recommendation is applied where appropriate.
- [ ] Plugin name, description, creator, icon/thumbnail meet current requirements.
- [ ] Current price range and 30-day escrow are confirmed.
- [ ] Distribution limits and verification status are confirmed.
- [ ] Remote asset loading, third-party restricted assets, misleading claims, and harmful code are absent.
- [ ] Submission is not claimed complete until the Creator Dashboard shows it.

## G. Security and privacy

- [ ] API keys are kept outside Git and Drive documents.
- [ ] Analytics access, if used, is least privilege and Universe-scoped.
- [ ] Customer data use is documented and minimized.
- [ ] No tax, bank, Stripe, identity document, session cookie, or password appears in artifacts.
- [ ] Logs redact tokens and personal identifiers.

## H. Showrunner / IP

- [ ] No automated browser, scraper, script, or agent operates Showrunner.
- [ ] Hiro manually controls generation/publication.
- [ ] Core IP and public/remixable material are separated.
- [ ] Voice, music, likeness, and character rights are documented.
- [ ] Fable/Showrunner license implications are acknowledged before publication.
- [ ] Platform revenue share is not treated as guaranteed revenue unless current binding terms explicitly confirm it.

## I. Evidence and systems

- [ ] GitHub repository/branch/PR URL exists.
- [ ] Google Drive folder and index exist.
- [ ] Notion task is updated with status, results, blockers, and links.
- [ ] Files are re-read after save.
- [ ] Calendar/task entries are not duplicated.
- [ ] `logs/execution-log.md` and `outputs/status.json` agree.

## J. Independent final audit

### Rule compliance
- [ ] PASS / FAIL recorded with cited requirements.

### Fact and challenge
- [ ] PASS / FAIL recorded after independent re-opening of official sources and recalculation of important numbers.

### Execution and artifact
- [ ] PASS / FAIL recorded after independent inspection of actual files, CI, Drive, Notion, and public/private state.

A single FAIL blocks release. The Maker revises; the independent Checker reruns the complete audit.
