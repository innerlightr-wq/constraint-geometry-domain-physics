# Contributing

This repository documents a methodological framework rather than a software project, so contributions are editorial and scientific rather than functional.

## Contributions that are welcome

- **Typographical corrections** in the manuscript or documentation.
- **Citation verification** — confirming, correcting, or completing bibliographic records, especially the entries listed as unresolved in `bibliography_status.md`.
- **Clarification of terminology** — cases where a term is used inconsistently, or where a definition in `docs/terminology.md` admits a reading the manuscript does not intend.
- **Independent tests of embeddings** — any attempt to justify, or to undermine, a domain map $a/b=F(X)$ used in the note.
- **Counterexamples** — a domain in which the framework's stated conclusions fail, or a case in which a safeguard is shown to be too weak or too strong.
- **Domain applications** that satisfy the five-step protocol in `docs/protocol.md`.

Negative results are welcome on the same footing as positive ones. A domain shown *not* to be organized by its partition structure is a result, not a failure.

## What a new application must identify

A proposed application will not be accepted as a diagnostic unless it states, explicitly:

1. **The genuine conserved or complete partition.** Which two sectors, and for what domain-internal reason they exhaust a fixed total. Two positive quantities divided by their sum do not qualify.
2. **The independent domain map.** The functional form of $a/b=F(X)$, its derivation, and — separately — which parts of it are conventional. Any undetermined overall normalization must be reported, because it propagates directly into the location of every landmark.
3. **The admissible physical range.** The bounds the domain itself imposes, and where the landmark sits relative to them. A landmark outside the admissible range is not a diagnostic.
4. **The test that could fail.** A held-out prediction, a family collapse with a reported residual, an independent determination of a structure that then predicts a trajectory, a cross-domain recurrence under a pre-declared normalization, or a demonstrated compression. A construction that cannot fail explains nothing.

## Style

- Keep the epistemic tiering explicit. Label exact mathematics, domain diagnostics, and speculative interpretation separately, as in `docs/epistemic_tiers.md`.
- Prefer understatement. If a claim needs a qualifier, put the qualifier in the claim rather than in a footnote.
- Do not introduce DOIs, numerical results, or citations that have not been verified.

## How to propose a change

Open an issue describing the correction or the application, with the four items above where applicable. For textual corrections a pull request against the relevant file is fine; for changes to the manuscript, note that the LaTeX source in `paper/` is authoritative and the PDF is regenerated from it.
