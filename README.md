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

---
## v6 — Predictive research laboratory (ML)
Replaces the manual hypothesis loop with a research engine: one feature matrix (16 features + 5 pre-defined economic interactions), expanding-window walk-forward with a **6-month purge**, a four-model tournament, and systematic feature attribution. Cross-sectional z-scoring makes this a pure *relative* model — globally common variables (VIX, Brent, DXY) become exactly zero and cannot enter as raw features.

| Deliverable | File |
|---|---|
| v6 notebook (executed) | `notebook/Markets_Scorecard_v6.ipynb` |
| v6 CSVs / charts | `output/v6/` (incl. `feature_attribution.csv`, `null_ceiling.csv`, `drop_one_group.csv`) |

### The guard that makes it meaningful
The **entire pipeline** — all four models, all walk-forward folds — is re-run on block-shuffled country labels. A 4-model tournament on pure noise still reaches OOS IC **+0.140** at the 95th percentile. Anything below that is model-selection noise.

| | |
|---|---|
| Best model OOS IC | **+0.168** (GAM, additive splines) |
| One-feature benchmark (EPS revision 6M) | +0.137 |
| p(best-of-4 noise ≥ observed) | **0.017** |
| Non-overlapping 6M IC | **+0.306** (t 3.27, n=17) |
| Sub-period stability | +0.187 / +0.149 |

**First result in the project to clear a full-pipeline null ceiling *and* survive the non-overlapping test.**

### The IC → P&L gap and its cause
Score-weighted L/S Sharpe **−0.03**; equal-weighted top-2 minus bottom-2 Sharpe **+0.51**. Mean next-month return by predicted rank (bps): #1 +86, #2 +71, #3 +68, #4 +74, #5 +45 — the model separates the extremes and jumbles the middle, so score weighting bets hardest on the magnitudes it gets wrong. **The construction was the problem, not the signal.**

### Attribution
Credited by all four views: `ix_cheap_x_epsstab`, `micro_eps_stab`, `micro_eps_rev_6m`, `ix_fci_x_epsrev`, `macro_fci_6m`, `ix_mom_x_epsrev`, `tech_mom_6_1`, `micro_eps_rev_3m`. The **cheap × earnings-stability** interaction that v5 Phase 1 predicted is credited by the engine without being privileged.
Permutation importance alone is unreliable here — `macro_pmi_3m` scores highest on it with a *negative* univariate IC, a textbook correlated-substitute artefact. Drop-one-group is the decisive test: removing interactions hurts every linear model; **removing valuation improves every model**.

### Analytical finding
`ext_oil_local_6m` correlates **+1.00** with `ext_fx_mom_6m` — oil is common to all five markets, so oil-in-local-currency *is* FX after cross-sectional demeaning. The v4 local-currency-oil experiment could never have added information.

**Status: strongest candidate the project has produced, still not established alpha.** Test period is the same window examined in v3–v5, so it is not a clean hold-out. Next step is prospective paper trading of a frozen equal-weighted top-2/bottom-2 implementation.

---
## v7 — Verification pass on the frozen v6 model
No new features, no new hypotheses. Feature matrix loaded as written to disk so the run is bit-identical to v6. Spec frozen in `output/v7/frozen_model_spec.json`.

| Check | Result | Verdict |
|---|---|---|
| All six non-overlapping offsets | +0.306, +0.118, +0.212, +0.118, +0.176, +0.176 → **mean +0.184**, 6/6 positive, 2/6 significant | v6's +0.306 was the best draw; **withdrawn** |
| Null ceiling, 2,000 reps (was 120) | observed +0.168 vs 95% ceiling +0.124, **p = 0.0095** on 19 exceedances | **Holds** |
| GAM vs one-feature benchmark (paired) | difference +0.030, NW t +0.55, bootstrap p 0.265 | **Complexity not justified** |
| Valuation reconciliation | interaction alone +0.009 vs its EPS-stability component alone **+0.130** | **Phase-1 hypothesis rejected** |
| Grouped conditional permutation | micro +0.062, ix +0.053, macro +0.030, **val −0.016** | replaces the v6 `macro_pmi_3m` artefact |
| Five-country P&L (reconciles exactly) | long leg +66.2 bps, **short leg −33.6 bps**; UK short 82% of months, −18.7 bps | short side loses money |
| Leave-one-country-out | **ex-US: IC +0.027, Sharpe +0.10**; ex-Japan and ex-Eurozone *improve* | **substantially a US call** |
| Duplicate feature | r = +0.9993, removal moves GAM −0.0095 | confirmed redundant |

**Key reversal:** v5's "cheapness conditional on earnings stability" is **rejected** — multiplying earnings stability by cheapness destroys information (+0.130 → +0.009). The carrier is earnings stability alone. Scrambling the valuation block *raises* out-of-sample IC.

**Discipline note:** "full model minus valuation main effects" scores +0.193, the best configuration seen, and is **deliberately not adopted** — it was identified on the same data used to evaluate it.

**Corrections to the v6 write-up:** an additive-spline GAM cannot discover interactions; the five were pre-engineered, so the accurate claim is that the engine credited *pre-supplied* terms. Individual permutation importance (`macro_pmi_3m`) was a correlated-substitute artefact.

**Status:** holds against a noise ceiling; a single feature does nearly all the work; the portfolio result depends on the US. Not investable alpha. Everything this dataset can tell us has been extracted — the only remaining test is prospective paper tracking.

---
## v8 — Completing the four pillars
Macro and Micro were settled by v4–v7. v8 attacks the two open pillars with **six economically distinct candidates each**, directions fixed ex ante, under a selection rule declared before any candidate was run.

**Why valuation kept failing (diagnosed, not guessed):** cheap markets re-rate upward (multiple leg +0.149/+0.097) *and* have estimates cut (earnings leg −0.215). The legs cancel. Raw P/E selects for cheap-for-a-reason. v5 also showed the obvious fix fails — multiplying cheapness by earnings stability **destroys** information (+0.130 → +0.009), because a product of z-scores is large when both components are low.

**Selection rule (fixed in advance):** IC positive in *both* windows · ≥4 of 6 non-overlapping offsets positive · valuation must load positively on the **multiple leg**. Winner = highest mean of discovery and validation IC, never the max of either.

| Pillar | Signal | disc IC | val IC | offsets | multiple leg | earnings leg |
|---|---|---|---|---|---|---|
| Macro | FCI 6M easing | +0.079 | +0.127 | 6/6 | −0.069 | +0.213 |
| Micro | EPS revision 6M | +0.117 | +0.131 | 6/6 | −0.089 | +0.333 |
| Valuation | V3 multiple reversal 6M | +0.093 | +0.059 | 4/6 | +0.112 | −0.048 |
| Technical | T3 earnings-confirmed momentum | +0.097 | +0.113 | 6/6 | −0.053 | +0.246 |

### Scorecard
| | disc IC | val IC | disc Sharpe | val Sharpe |
|---|---|---|---|---|
| **4-pillar equal weight** | **+0.234** (t 3.14) | **+0.163** (t 2.11) | **0.80** | **0.63** |
| 3-pillar (no Valuation) | +0.182 | +0.128 | 0.67 | 0.60 |
| 2-pillar core (Macro+Micro) | +0.160 | +0.156 | 0.66 | 0.57 |

Max drawdown −11.3% in validation. **Strongest result in the project**, and the composite IC exceeds every individual signal — genuine diversification. **End-to-end null** (full selection rule re-run on shuffled labels): composite p = **0.000**.

### Where it is weak — on the record
1. **Individual pillar winners do not clear the 12-candidate multiplicity ceiling** (best observed +0.098 vs best-of-12 noise 95th pct +0.120; Valuation p 0.321, Technical p 0.144).
2. **V3's qualifying condition is mechanical.** `P/E_t` sits in both the signal and the target denominator; lag 3 months and the multiple-leg loading falls +0.112 → **+0.001**, validation IC turns **−0.102**. After six distinct constructions, **valuation still has no signal that survives scrutiny at 3–6 months**. V3 is carried as the pillar's best available representative, not as a discovery.
3. Valuation's true worth is 4-pillar vs 3-pillar: val IC +0.163 vs +0.128, Sharpe 0.63 vs 0.60.
4. **Country concentration persists** — without the US, validation Sharpe is −0.08.
5. 2017-26 examined since v3: structured re-use with declared rule and multiplicity corrections, **not a clean hold-out**. Price return only; five markets; 78% first principal component.

**Methodological lesson carried from v5: gate, don't multiply.** T3 gates momentum on positive EPS growth (+0.026 mean IC over plain momentum); the product operator that destroyed cheap×stability is avoided.

**Current ranking (Apr 2026):** US Overweight · Japan Overweight · UK / Eurozone / Switzerland Underweight.

## v11 — Audit of v10 (`notebook/Markets_Scorecard_v11.ipynb`, outputs `output/v11/`)
Report: `output/v11/AUDIT_REPORT.md`. Re-executes committed v9/v10 notebook code: nine tables reproduce exactly (max diff 4e-16).
- **v9 and v10 "common samples" silently dropped 16 / 27 stress months.** Gated signals go constant and every signal lost those months. v10's FCI validation t 2.49 falls to 1.74 on the clean 204-month sample.
- v9 +0.005 vs v10 +0.058 incremental IC: opposite directions on different samples. Neither direction is significant on any sample.
- EPS revision IC is largely a static US/Japan tilt (validation timing-only IC +0.072, t 0.99). FCI survives drift removal better, especially at 6M.
- HAC/bootstrap over-reject (6–9% size under a pure null). Best-of-family p ≈ 0.16–0.20. **No statistical significance can be claimed.**
- Valuation and Technical stay rejected or exploratory, with documentation in `valuation_technical_closure.csv`.
- Latest common data date is 2026-04-30 (US file), 7 months before the session date.
