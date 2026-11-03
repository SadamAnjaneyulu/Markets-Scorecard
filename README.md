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
