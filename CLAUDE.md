# rulespec-dk Agent Notes

This repo stores Denmark RuleSpec source registry materials, oracle references, and encoded policy rules. Denmark is a unitary state (kommuner administer and Udbetaling Danmark pays, but the modelled law is national), so all encoded law lives under a single `dk/` national namespace.

## Scope

- `dk/statutes/`: Acts of the Folketing as consolidated on retsinformation.dk — lovbekendtgørelser (LBK, consolidated acts) such as børne- og ungeydelsesloven (LBK nr 603 af 12/05/2025), plus the ændringslove (LOV, amendment acts) captured for amendment diligence.
- `dk/regulations/`: bekendtgørelser (ministerial orders, BEK) made under the governing acts.
- `dk/policies/`: administrative publications that carry annually regulated current-year amounts (Skatteministeriet/Skattestyrelsen tables, satser publications), captured as official documents.
- `programs/`: declarative compose specs (one per jurisdiction/program/period).
- `data/coverage/`, `data/oracles/`: coverage backlog and comparison references. These are never legal authority.

## Sources: retsinformation.dk mechanics

- Danish law is published in Lovtidende and served by retsinformation.dk (Civilstyrelsen) under **stable ELI URIs**: `retsinformation.dk/eli/lta/{year}/{number}`. Content negotiation: `.json` returns the ELI JSON-LD metadata graph; `/dan/pdf`, `/dan/html`, `/dan/xml` are the manifestation URLs. Per the ELI metadata, the **PDF manifestation carries legal value `definitive`**; HTML and LexDania XML are `official`. The HTML manifestation URL serves the SPA shell to non-browser clients — use the PDF (or, for a future section-level adapter, the XML).
- Use the ELI JSON-LD graph for currency checks before encoding: `in_force`, `consolidated_by` (a newer LBK supersedes), and `changed_by` (amendment acts to diligence section-by-section).
- A lovbekendtgørelse consolidates prior amendments listed in its preamble; amendments made **after** the consolidation must be checked against every encoded section and recorded in the corpus manifest metadata.
- Danish is the only authentic language. Corpus provisions carry `language: da`; there is no official English text. Do not encode from unofficial translations.

## Do

- Start from the furthest upstream source: the current in-force LBK consolidation on retsinformation.dk first, then its post-consolidation ændringslove, then bekendtgørelser, and administrative satser tables only for the annually regulated current-year values.
- Add RuleSpec under `dk/statutes/`, `dk/regulations/`, or `dk/policies/` with companion `.test.yaml` files.
- Cite corpus paths from modules via `module.source_verification.corpus_citation_path` (or `corpus_citation_paths`).
- Use calendar year 2026 as the validation year. Danish statutes typically state amounts at a base-year level (e.g. 2010-niveau, 2011-niveau) with an annual regulation mechanism (the act's own CPI rule or personskattelovens § 20). **Encode the statutory base amounts and the mechanism from the statute; current-year regulated amounts may only come from a captured official publication, never from computing the regulation yourself and never from third-party summaries.**
- Quote Danish number style verbatim in proof excerpts ("16.992 kr. årligt (2011-niveau)" — dot as thousands separator); formulas use plain integers (16992).
- Amounts are in DKK (seeded currency unit, minor_units 2).
- Keep exact oracle versions in `data/oracles/oracle-index.json`. EUROMOD's public DK systems (JRC release) are the natural parity oracle once wired.
- Sync `axiom-encode` and `.axiom/toolchain.toml` before substantial encoding runs (fetch origin and read the current version before every encode run and before choosing any version-bump number).

## Do Not

- Use borger.dk guidance, bank/payroll summaries, or third-party tax calculators as the first legal source when an act governs the rule.
- Invent, round, interpolate, or **self-compute the annual regulation of** any Danish monetary amount, rate, or threshold. Every number must come verbatim from a captured official provision.
- Migrate EUROMOD policy code or agency calculator logic mechanically as RuleSpec.
- Add generated source payload dumps, formula artifacts, `parameters.yaml`, or standalone YAML fixtures outside allowed RuleSpec roots.
- Hand-copy statute text into RuleSpec without a corpus `citation_path`.
