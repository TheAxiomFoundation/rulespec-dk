# rulespec-dk

Denmark RuleSpec source registry.

This repository is a **bounded pilot** of a non-English-source jurisdiction: it targets the Danish child and youth benefit (børne- og ungeydelsen, "børnechecken") under børne- og ungeydelsesloven — the consolidated act LBK nr 603 af 12/05/2025 as amended by LOV nr 1642 af 16/12/2025 and LOV nr 303 af 24/02/2026. The pilot encodes § 1 (the age-banded tax-free benefit amounts at 2011-niveau and their CPI regulation) and § 1 a (the 2 pct. income-based reduction above the 700.000 kr. 2010-niveau bundfradrag). Denmark is a unitary state; all encoded law lives under a single `dk/` national namespace.

The validation year for encoded amounts is **calendar 2026**; effective dates follow each act's own commencement provision. Statutory amounts are stated at base-year niveau (2011-niveau in § 1; 2010-niveau in § 1 a) and regulated annually — the statutory bases and the regulation mechanism are encoded from the act, while current-year regulated krone amounts enter only via captured official publications (`dk/policies/`), not by computing the regulation in this repo.

## Source priority

Policy must come from the furthest upstream available source.

1. retsinformation.dk (Civilstyrelsen / Lovtidende) consolidated acts (LBK) and amendment acts (LOV) at their stable ELI URIs — the PDF manifestations carry ELI legal value `definitive`. Danish is the only authentic language.
2. Bekendtgørelser (ministerial orders) made under the governing act.
3. Skatteministeriet/Skattestyrelsen administrative publications for the annually regulated current-year amounts (satser tables), captured as official documents.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

EUROMOD's Denmark systems (public European Commission JRC release, run on the EUROMOD engine) are the intended parity oracle for this repository; they are not yet wired (see `data/oracles/oracle-index.json`). Statistics Denmark's Lovmodellen is government-internal and not available as an oracle.

## Listing gates

This repo carries `app_visibility = "experimental"` in `.axiom/registry.toml` and stays out of app surfaces until:

1. The encoded surface covers the flagship calculation (per-child annual børne- og ungeydelse including the § 1 a income taper) end to end with companion tests, on current-year regulated amounts from captured official publications.
2. Oracle parity suites exist and pass against EUROMOD DK for the encoded surface.
3. Citation paths are stable (LBK-number form against retsinformation.dk ELI URIs).
