# Developed Markets Equity Scorecard (US · Eurozone · UK · Switzerland · Japan)

| Deliverable | File |
|---|---|
| Python notebook (executed) | `notebook/Markets_Scorecard.ipynb` |
| CSV input | `data/scorecard_input_monthly.csv` (cleaned monthly panel used by the model) |
| CSV outputs | `output/scorecard_monthly_scores.csv`, `current_ranking.csv`, `predictive_power.csv`, `backtest_stats.csv`, `backtest_monthly_returns.csv` |
| PowerPoint (5 slides) | `slides/Markets_Scorecard.pptx` |
| Charts | `output/charts/` |

**Run:** `cd notebook && jupyter nbconvert --to notebook --execute --inplace Markets_Scorecard.ipynb` (needs pandas, numpy, scipy, statsmodels, matplotlib).

## Key choices
- Price proxy = forward P/E × forward EPS (the supplied "price" file actually contains P/E values). Returns in local currency and USD, price-return only.
- Signals (one per pillar, direction fixed ex ante): PMI 3M change (1M publication lag) · EPS 3M revision · forward P/E z-score vs own expanding history (inverted) · 12-1M momentum.
- Cross-sectional z-scores → equal-weight composite → rank. Stance: top 2 Overweight, middle Neutral, bottom 2 Underweight.
- Backtest: monthly signal, 3M/6M overlapping tranches, gross of costs. Window 2010-12 → 2026-04; as-of date Apr-2026 (US file ends there).

## Result (honest read-out)
The pre-specified equal-weight composite shows **no reliable predictive power or backtest edge**. Only the EPS-revision pillar has supporting evidence; the PMI pillar has a negative IC (not flipped, to avoid fitting). The current ranking (UK, Japan OW / Switzerland, Eurozone UW; US Neutral) should be read as a low-conviction tilt.

---
## v2 (exploratory follow-up)
v1 showed no reliable edge, so v2 makes two changes declared up front: **C1** macro pillar PMI → financial-conditions-index easing; **C2** equal weights → walk-forward IC weights.
All four combinations are run and reported (research ledger in the notebook). **v2 designed after viewing v1 on the same data → no untouched out-of-sample; results are exploratory.**

| Deliverable | File |
|---|---|
| v2 notebook (executed) | `notebook/Markets_Scorecard_v2.ipynb` |
| v2 CSV input | `data/scorecard_input_monthly_v2.csv` |
| v2 CSV outputs / charts | `output/v2/` |
| v2 PowerPoint (5 slides) | `slides/Markets_Scorecard_v2.pptx` |

**Result:** headline v2 (FCI + walk-forward weights) improves on v1 (composite IC +0.013 → +0.069; L/S USD Sharpe 0.05 → 0.18) but the Sharpe is not distinguishable from luck (permutation p = 0.24). The macro swap drove the gain; walk-forward weighting did not help. Stable across all specs: Eurozone and Switzerland are bottom-two; Japan top-two in 3 of 4.

---
## v3 — disciplined signal search (latest)
v1/v2 produced no statistically reliable signal, so v3 searches **all supplied data** (40 hypothesis-driven signals: EPS, valuation, 2Y yields, credit, FX, technical, macro; directions fixed ex ante) with selection-bias controls:
discovery 2007-16 → embargo → frozen validation 2017-26, plus a Westfall-Young max-statistic permutation test (noise floor for the best of 40) and a pooled Stage 2.

| Deliverable | File |
|---|---|
| v3 notebook (executed) | `notebook/Markets_Scorecard_v3.ipynb` |
| v3 CSVs / charts | `output/v3/` |
| v3 PowerPoint (5 slides) | `slides/Markets_Scorecard_v3.pptx` |

**Findings:** nothing clears the multiple-testing bar in discovery (best z 2.64 vs 2.95); valuation signals reversed sign after 2016; across the library discovery IC does not predict validation IC (ρ = −0.13).
**EPS revision 6M** is the only signal positive in both windows with pooled adjusted p = 0.09 (validation p = 0.02, Bonferroni 0.11). **FCI easing 6M** is the runner-up (adj. p = 0.27).
Headline v3b = EPS revision 6M + FCI easing 6M (equal weight; valuation and technical pillars get zero weight by rule): IC ≈ +0.16 and L/S Sharpe ≈ 0.5 (USD) in both windows, permutation p ≈ 0.06.
**Not proven:** v3b/v3c choose signals using pooled data, so the validation window is not clean OOS; p-values are not adjusted for choosing among 40 signals; only 5 markets.
Current call (Apr 2026): Overweight US; Neutral Japan, Eurozone; Underweight Switzerland, UK (low conviction on UK).
