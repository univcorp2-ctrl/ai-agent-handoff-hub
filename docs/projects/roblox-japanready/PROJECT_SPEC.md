# PROJECT SPEC — Roblox JapanReady

## 1. Objective

Robloxで「何か作って待つ」のではなく、既存スタジオが日本市場へ展開するときの摩擦を減らすサービスを先に販売し、その反復工程をRoblox Studioプラグインへ製品化する。

## 2. Target customer

### Must-have

- Roblox上に公開中Experienceがある
- 過去90日以内の更新、イベント、コミュニティ活動等が確認できる
- 英語圏または日本国外を主市場としている
- 日本語が未対応、機械翻訳のみ、UI崩れ、説明・課金文言が不自然等の改善余地がある
- 公式サイト、メール、フォーム、Discord、LinkedIn等の実在する連絡経路がある

### Exclude initially

- 個人趣味で更新が止まっている
- 権利侵害・模倣・不適切コンテンツが疑われる
- 日本市場へ既に専任チームを持つ大手
- 連絡経路が推測しかない
- 子どもへの不適切な課金・接触等、安全上の重大懸念がある

## 3. Offer

### Product name

Roblox Japan Launch Sprint

### Promise

In seven days, identify and fix the highest-impact Japanese localization, mobile UI, store-copy, and monetization friction, then deliver a 30-day Japan growth experiment plan.

### Deliverables

1. Executive summary
2. Japanese player journey audit
3. Localization QA matrix
4. Mobile UI overflow/readability findings
5. Experience/store/product copy recommendations
6. Monetization and retention hypotheses
7. Prioritized 30-day experiment backlog
8. KPI baseline/measurement sheet
9. Risk, unknowns, and required data list

### Test pricing

- First three design partners: USD 500–650
- Standard hypothesis after evidence: USD 1,500–3,000
- Monthly optimization hypothesis: USD 300–800/month

All amounts are sales-test hypotheses, not claims of prevailing market prices.

## 4. Service workflow

### Day 0 — Intake

Required:
- Experience URL and universe/place IDs if available
- Current supported languages
- Target player age/region
- Current top products/passes/subscriptions
- Country-level DAU, D1/D7 retention, revenue if customer grants access
- Recent release notes
- Known complaints or support tickets

Do not require API keys for the first public-information audit. If Analytics Query API access is later used, create a least-privilege key limited to `universe.analytics:read`, keep it outside the repository, and rotate/revoke it after the engagement.

### Day 1–2 — Audit

- Experience/store page
- Japanese availability and translation completeness
- UI strings on mobile
- Key onboarding and monetization moments
- Public community feedback
- Unsupported assumptions clearly marked

### Day 3 — Recommendations

Rank by:
- expected player impact
- implementation effort
- evidence strength
- reversibility
- measurement feasibility

### Day 4–5 — Implementation support

Initial engagement provides copy, translation table, QA checklist, and implementation notes. Direct production changes are optional and require explicit scope/access.

### Day 6 — Measurement plan

Define baseline, event, segment, observation window, success threshold, guardrail metric, rollback condition.

### Day 7 — Delivery

Deliver report, prioritized backlog, KPI sheet, and 30-minute review. Record open questions and next-month option.

## 5. Lite plugin MVP

### User story

As a Roblox developer, I want to scan my current Studio DataModel for player-facing text and localization risk so that I can fix missing or fragile Japanese support before release.

### In scope

- Plugin toolbar button
- DockWidget result panel
- Read-only scan of descendants
- Detect text-bearing instances: TextLabel, TextButton, TextBox and configurable additional classes
- Capture:
  - full instance path
  - class name
  - text
  - text length
  - AutoLocalize state where available
  - LocalizationMatchIdentifier where available
  - warning codes
- Warnings:
  - EMPTY_KEY / no localization linkage indicator
  - HARD_CODED_TEXT candidate
  - LONG_TEXT candidate
  - LINE_BREAK / special-character review
  - AUTOLOCALIZE_DISABLED
- CSV-safe output shown in a selectable text area
- Scan summary by warning/type

### Out of scope for Lite v0.1

- automatic translation
- writing to production objects
- remote APIs
- external billing
- user analytics upload
- automatic screenshots
- automatic UI resizing
- Showrunner integration

### Privacy

All scans run locally inside Studio. No data leaves Studio. No telemetry in v0.1.

## 6. Technical design

Recommended toolchain after current verification:

- Luau
- Rojo project structure, if the agent confirms current compatibility
- StyLua for formatting
- Selene for static analysis
- TestEZ or a pure-Luau test strategy for scanner/CSV modules
- GitHub Actions for lint/tests where runnable outside Studio

The agent must verify current versions and official/primary documentation before pinning dependencies.

### Modules

- `scanner.lua`: read-only traversal and normalized finding records
- `rules.lua`: warning rules with deterministic inputs/outputs
- `csv.lua`: RFC-4180-style escaping and row generation
- `ui.lua`: toolbar/DockWidget rendering
- `Main.server.lua`: orchestration only

Keep domain logic outside UI so it can be tested.

## 7. Prospect pipeline

Required fields:
- prospect_id
- studio_name
- studio_url
- experience_name
- experience_url
- creator_url
- contact_channel
- contact_url
- evidence_checked_at
- recent_activity_evidence
- japanese_support_state
- observed_issue
- fit_score
- priority
- outreach_status
- next_action
- notes

No guessed contact addresses. Record `unverified` instead.

## 8. Sales message requirements

Every first contact must include:
- one true, publicly observable finding specific to the experience
- one concrete outcome
- narrow seven-day scope
- test price or invitation to discuss pilot, depending on channel
- low-friction CTA
- no unsupported promise of revenue uplift

## 9. IP and terms boundaries

- No unlicensed third-party brand, character, music, voice, or likeness.
- Customer confirms ownership/authorization for supplied content.
- Showrunner is manual-only. Do not automate access or generation.
- Public Showrunner content may be remixable and subject to broad platform license; core IP assets should remain outside until approved.
- Legal/contract language is draft until reviewed for the actual transaction and jurisdiction.

## 10. Evidence and analytics

Report factual observation separately from hypothesis.

Example:
- Fact: Japanese strings are unavailable on the public page.
- Fact: a mobile screenshot shows truncation.
- Hypothesis: resolving truncation will improve onboarding completion.
- Test: A/B or phased release with completion-rate guardrail.

## 11. Milestones

### M0 — Ready to sell

Offer, sample audit, intake, delivery template, prospect schema, and 10 verified prospects.

### M1 — Market signal

30 personalized outreach attempts, at least five replies and three conversations, or documented reason why target/list/offer failed.

### M2 — Paid evidence

One paid pilot or three design partners with explicit willingness to use/test.

### M3 — Product evidence

Lite v0.1 passes tests and is used by three target studios.

### M4 — Decision

Continue, narrow, reprice, partner, or stop based on evidence. Only then consider avatar accessories, Fab, or Fortnite investment.
