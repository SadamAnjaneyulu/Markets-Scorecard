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
