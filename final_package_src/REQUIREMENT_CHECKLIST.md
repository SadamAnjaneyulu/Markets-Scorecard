# Requirement checklist

Each requirement is mapped to the deliverable that meets it. "Verified" means a check was actually executed, and the method is stated. Items that could not be verified, or that carry a caveat, are marked.

## Task

| Requirement | Deliverable | Status |
|---|---|---|
| Scorecard for US, Eurozone, UK, Switzerland, Japan | `output/final/scorecard_history.csv` (5 markets × 201 months) | Verified: 5 markets, no duplicate (month, market) rows |
| Identify likely out- and under-performers over 3–6 months | Rank IC tested at both horizons; 3M and 6M columns in `predictive_power.csv` | Done |
| Use only the supplied dataset | Notebook reads only the six workbooks in `data/raw/` | Verified: no network or download calls in the notebook code |

## Step 1 — Signal construction

| Requirement | Deliverable | Status |
|---|---|---|
| At least one Macro, Micro, Valuation and Technical signal | `signal_definitions.csv`, `*_signal_history.csv`, notebook §4 | Done: one indicator per pillar |
| Economic rationale for each | `signal_definitions.csv`, methodology §3–§4 | Done |
| Mathematical construction, direction, lookback, standardisation, data source, limitations | `signal_definitions.csv` | Done |
| Price information in the Technical pillar is disclosed | Notebook §3, methodology §2.3 and §4.5 | Done. The supplied price workbook holds valuation ratios, so prices are reconstructed; the Technical pillar is stated to be non-independent |

## Step 2 — Predictive power

| Requirement | Deliverable | Status |
|---|---|---|
| Discovery and examined results for every pillar | `predictive_power.csv` | Done |
| Confidence intervals, statistical tests, multiple-testing caveat | Same file; methodology §6 | Done: bootstrap intervals, HAC t, caveats stated |
| Country-level contributions | `country_ic_contributions.csv` | Verified: the five country terms sum to each IC |
| 3M and 6M horizons | `predictive_power.csv` | Done |
| Confidence labels | `signal_classification.csv` | Done: Macro and Micro predictive (provisional); Valuation and Technical diagnostic |

## Step 3 — Scorecard

| Requirement | Deliverable | Status |
|---|---|---|
| Pillar scores for all five markets | `pillar_scores.csv` | Done |
| Aggregate scores, two views | `aggregate_country_scores.csv` | Done: four-pillar diagnostic and predictive |
| Rankings | `country_rankings.csv`, `current_ranking.csv` | Done |
| Failed pillars kept visible, with no predictive weight | `scorecard_history.csv` (contributions) | Done: weight 0.25 in the diagnostic score, 0 in the predictive score |
| Contribution of each pillar | `scorecard_history.csv`, deck slides 3 and 5 | Done |

## Step 4 — Backtest

| Requirement | Deliverable | Status |
|---|---|---|
| Long-only and long-short | `backtest_performance_summary.csv`, `monthly_portfolio_returns.csv` | Done |
| Equal-weight benchmark | `benchmark_returns.csv` | Done |
| Sharpe, volatility, drawdown, turnover, costs | `backtest_performance_summary.csv`, `transaction_cost_sensitivity.csv` | Done: costs at 0/5/10/20 bps, plus 30 and 50 bps in the sensitivity file |
| Country attribution | `country_attribution.csv` | Done |
| Original versus revised model, identical dates and rules | `model_comparison.csv` | Done: five models on one engine |

## Step 5 — Investment view

| Requirement | Deliverable | Status |
|---|---|---|
| Current ranking of all five markets | `current_ranking.csv`, slide 5 | Done, **as of 30 April 2026** |
| As-of date disclosed | Every slide footer, the slide 5 stamp, README, methodology §9 | Done. The ranking is the latest the supplied data supports and is not presented as current market data |
| Concise recommendation | Slide 5, methodology §9 | Done, with a conviction and risk statement |

## Deliverables

| Requirement | Deliverable | Status |
|---|---|---|
| Notebook with the required 13-part structure | `notebook/Developed_Markets_Scorecard_FINAL.ipynb` | Verified: executed top to bottom with `nbconvert`, 41 cells, 0 errors, 0 unexecuted code cells |
| CSV inputs and outputs | `output/final/` | Verified: all 19 required files exist; no duplicate rows; every missing value is structural (see below) |
| Five-slide deck | `slides/Developed_Markets_Equity_Scorecard_FINAL.pptx` | Verified: exactly 5 slides |
| Methodology and research document | `METHODOLOGY_AND_RESEARCH_PROCESS.md` | Done: first-person, ten sections, numbered references |
| README and this checklist | `README.md`, this file | Done |

## Quality checks that were executed

| Check | Method | Result |
|---|---|---|
| Notebook runs end to end | `jupyter nbconvert --execute`, run several times from a cleared output folder, and once more from an unpacked copy of this package | 0 errors; about 12 seconds |
| Deck numbers trace to outputs | `slides/check_final_deck.py`: re-reads each registered slide number from its CSV | 126 of 126 match; 0 numeric tokens on slides without a source |
| Deck is readable and unclipped | All five slides rendered to images and inspected; overlaps found in earlier drafts were fixed and re-inspected | Done. Rendered with an open-source renderer, **not** opened in PowerPoint itself |
| CSV coverage and duplicates | Programmatic check of required files, duplicate rows and (month, market) keys | Clean |
| Missing values | Counted per file | All structural: indicator burn-in periods, forward returns not yet realised for the last months, and metrics that do not apply to a book |
| Main figures reproduce | An independent set of 14 matched-sample information coefficients was reproduced to four decimal places by applying the one-month signal lag | Matched. That comparison file is not part of this package |
| Identifier scan | Every notebook cell and output, script, CSV, JSON and markdown file, plus the internals and properties of the deck, for personal and organisation names, email addresses, usernames, file paths and links | Clean. Two benign matches: a random substring inside an embedded chart image, and the vendor-neutral namespace URIs that every `.pptx` contains |

## Caveats

- **Hard-coded reference values.** The notebook contains eight published monthly US index returns, typed in by hand, used only to validate the price reconstruction (§3.2). They feed no signal, score or backtest, and they are the only values in the notebook that do not come from the supplied workbooks.
- **Some figures in the methodology text are carried from earlier research and not recomputed by this notebook:** the selection-adjusted p-values of roughly 0.16–0.20, the count of about seventeen independent six-month periods, and the account of how earlier specifications behaved. The document labels these as earlier-stage results.
- **Walk-forward result against my choice.** Re-selecting each year among the three Micro specifications would choose the weighted persistence measure in most years. Retaining the simple measure is a parsimony judgement; the methodology document says so.
- **Input workbooks are not in the package.** Their file properties contain personal and organisation names, and the originals should not be altered. The README lists the six files to place in `data/raw/`.
- **File names are neutral.** They carry no organisation or personal names.
- **No pillar is statistically significant** once the length of the research process is considered, and the examined window is not untouched holdout data.
