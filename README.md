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

---
## v4 — hypothesis-driven research (recommended submission)
v4 restarts from economic mechanisms rather than indicator combinations: a data audit, five hypotheses with ex-ante directions, **nested incremental tests** (paired ΔIC + Fama-MacBeth), a frozen validation window, and a **25,301-candidate sweep used purely to calibrate the noise floor**.

| Deliverable | File |
|---|---|
| v4 notebook (executed) | `notebook/Markets_Scorecard_v4.ipynb` |
| v4 CSV input | `data/scorecard_input_monthly_v4.csv` |
| v4 CSV outputs / charts | `output/v4/` (incl. `experiment_log.csv`, `sweep_survivors_validation.csv`) |
| v4 PowerPoint (5 slides) | `slides/Markets_Scorecard_v4.pptx` |

**Headline finding.** The best of 25,301 candidates cleared a Westfall-Young family-wise correction (adjusted **p = 0.002**) — and its validation IC is **−0.091**. All 10 discovery stars tested out of sample are negative (mean −0.060). *Surviving a multiple-testing correction on one sample is not evidence of an edge.*

**What survives.** Only signals with the **same sign in both regimes**: EPS revision 6M (+0.117 → +0.131) and FCI 6M easing (+0.079 → +0.127). Valuation was the strongest family in 2007–16 and reversed after 2016, which also kills the GARP hypothesis in all three forms (additive, conjunction, conditional filter).

**Recommended scorecard** — all four pillars constructed and tested, then weighted by evidence: Macro 50% (FCI 6M easing) + Micro 50% (EPS revision 6M); Valuation and Technical 0%. Validation IC +0.156 (t 2.38), L/S Sharpe 0.51 USD / 0.53 local, max DD −11.9%, active IR 0.47, permutation p 0.064.

**Current view (Apr 2026):** Overweight US · Neutral Japan, Eurozone · Underweight Switzerland, UK.

**Data audit (§1 and §12b of the notebook).** The supplied "price" file contains P/E, not prices — but **price is exactly recoverable**: `Forward P/E × Forward EPS = Price` is an accounting identity, and the recovered US series matches **actual S&P 500 monthly returns to 0.04 pp** (vol 13–17%, 2008-09 drawdown −44% to −58%, cross-market correlations 0.61–0.84). So the return target is the true index, not a proxy, and the "contaminated target" challenge does not stand. It also resolves the US EPS question: since P/E × EPS reproduces SPX exactly, `Monthly_EPS` must be the same forward consensus as `BEst EPS` — a naming difference.

**What an external review upheld (§12b).**
- **Concentration:** the US supplies +157% of the long/short P&L. Excluding it cuts validation IC from +0.156 to +0.050 and Sharpe from 0.51 to 0.14.
- **Redundancy:** adding FCI to EPS revisions is not significant (ΔIC t = 0.46); macro alone gives IC +0.127 / Sharpe 0.49.
- **Inference:** with non-overlapping 6M returns the validation t-stat falls from 1.46 to 0.94.
- **Selection:** the sign-stability rule was chosen after seeing validation, so +0.156 is optimistic.
- **Dividends:** price return only; UK and Switzerland are high-yield and both are Underweight, so the bias runs with the call.
- **Mechanism:** the composite predicts the *earnings* leg (+0.32 validation) and loses on the *multiple* leg (−0.06). Valuation is the mirror image — it predicts re-rating in both windows (+0.149/+0.097) but loses on earnings, which is why its total-return IC appeared to "reverse".

**Status: research candidate for paper trading, not an investable alpha.**

---
## v5 — Phase 1: repricing research
Mechanism-first, not combination-first. Four pre-registered experiments against the **multiple leg** of the return identity (66% of local-return variance, never modelled directly before).

| Deliverable | File |
|---|---|
| v5 notebook (executed) | `notebook/Markets_Scorecard_v5.ipynb` |
| v5 CSVs | `output/v5/` (incl. `experiment_log_v5.csv`, `v5_signals_and_legs_monthly.csv`) |

| ID | Hypothesis | Verdict |
|---|---|---|
| G0 | The re-rating link is a measurement artefact | **Survives** — random-walk placebo IC ≈ 0; real data at 94th/87th percentile |
| R01 | Expanding multiples keep expanding | **Rejected** — IC −0.104 / −0.105 |
| R02 | Cheap markets re-rate upward | **Supported on the component** — multiple-leg IC +0.149 / +0.097; cheap-vs-peers at 6M reaches val IC **+0.166, t 2.26, bootstrap p 0.042** (strongest clean statistic in the project) |
| R03 | Cheapness only re-rates when financing eases | **Rejected** — conditioning collapses IC to +0.028, and the regime relationship *reverses* between windows (easing in discovery, tightening in validation) |
| T1 | The lead is investable | **No** — total-USD IC −0.126; adding to the v4 composite gives ΔIC −0.183 (t −3.28); walk-forward Sharpe −0.30 |

**Conclusion:** valuation forecasts the component it should forecast, and the earnings leg more than offsets it. Cheap markets re-rate upward *and* have their estimates cut. Valuation stays at **zero weight**, now for an understood reason.

**Phase 1 produces a sharper question:** not "does valuation work" but **can the earnings leg be neutralised?** — cheapness conjoined with earnings *stability* (distinct from the GARP conjunction already rejected, which used earnings *momentum*). To be pre-registered before running.
