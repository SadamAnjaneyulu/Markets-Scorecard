# v13 Performance-Improvement Report

Notebook: `notebook/Markets_Scorecard_v13.ipynb` (38 cells, executed, 0 errors). Outputs: `output/v13/`.
The experiment grid and all decision rules were written to `experiment_registry.json` **before** any result was computed. One amendment was made after a run: an ERC solver bug fix, logged with its reason.

> **Bottom line: with the supplied data and this universe, neither a Sharpe of 1.0 nor one of 1.5 is achievable.**
> - The best Sharpe of **any** of 45 constructions, in **any** window, **before costs**, is **0.81**.
> - The fundamental law says the measured signal strength supports about 0.5. The current strategy already earns about that.
> - Reaching 1.0 would need roughly **double** the signal quality or **four times** the independent bets. Neither can come from re-engineering the existing data.

**On the windows:** "Discovery" means returns earned 2009-06 → 2016-12. "Examined" means 2017-08 → 2026-04. The examined window has been inspected across many iterations, so it is **not** a fresh holdout. **There is no untouched out-of-sample period in the supplied data.**

---

## 1. Current strategy diagnosis (backtest audit)

| Check | Finding | Verdict |
|---|---|---|
| Sharpe calculation | Mean ÷ sd of actual monthly **net** returns × √12; v12's 0.678 reproduces exactly | Correct |
| Annualisation | Lo (2002) autocorrelation-adjusted Sharpe is **0.60** vs 0.68. Overlapping tranches create positive lag-3/4 autocorrelation. | √12 is mildly flattering; both are now reported |
| Return alignment | Weights at month-end t earn the t+1 USD return; an independent loop matches to 1e-16 | Correct, no look-ahead |
| Weights | +50%/−50% × 2 per tranche. **The 6 overlapping tranches net against each other**, so the held book averages 1.48 gross, not 2.0, and ranges from 0.5 to 2.0. | As specified, but exposure is ~74% of intended and varies |
| Tranche accounting | v12 averaged target weights and ignored drift. A drift-accurate engine gives 0.680 vs 0.678. | Approximation was fine; v13 uses the exact engine |
| Costs | One-way bps × Σ\|Δw\|, both legs, first build included. Drift re-trading is now included too. | Correct |
| Risk-free rate | The L/S is self-financing, so rf = 0 is correct. Long-only is judged by information ratio vs equal weight. No T-bill series is supplied; the US 2Y is a disclosed proxy. | Correct |
| Benchmark | Equal-weight 5 markets. No market-cap data, so a cap-weighted benchmark is impossible. | Disclosed |

**Where the baseline return comes from** (full window, `audit_country_contribution.csv`):
- **Eurozone 2.7% of ~4.1% a year gross** (arithmetic contributions), mostly from being short. US +1.2%.
- Japan carries 28% of the variance and contributes −0.3%.
- **Without the Eurozone P&L, the baseline Sharpe drops from 0.66 to 0.13.** The strategy is largely one trade.

---

## 2. Portfolio construction (signal fixed at FCI 6M)

Nine constructions × five rebalancing schedules × four cost levels × three windows (`portfolio_construction_grid.csv`). Sharpe net of 10 bps, 6M overlapping tranches unless noted:

| Construction | Discovery | Examined | Full | Max DD (full) | Turnover |
|---|---|---|---|---|---|
| C2 top2/bottom2 (baseline) | 0.71 | 0.68 | 0.66 | −12.4% | 4.9× |
| C4 long-only top2 (active vs EW) | **0.72** | 0.63 | 0.62 | **−7.1%** | **2.4×** |
| C9 baseline, vol-targeted 10% | 0.70 | 0.71 | 0.66 | −14.1% | 6.4× |
| C7 inverse-vol sizing | 0.65 | 0.67 | 0.63 | −13.4% | 4.9× |
| C8 risk-balanced (ERC) | 0.72 | 0.49 | 0.55 | −9.2% | 5.0× |
| C5 rank-weighted | 0.49 | 0.65 | 0.54 | −14.8% | 5.3× |
| C6 z-weighted | 0.40 | 0.65 | 0.48 | −14.7% | 5.5× |
| C1 top1/bottom1 | 0.15 | 0.54 | 0.32 | −20.0% | 6.3× |
| C3 long-only top1 | 0.33 | 0.23 | 0.24 | −14.4% | 3.0× |
| C2, **monthly rebalance** | 0.18 | 0.16 | 0.14 | −20.4% | 13.0× |

- **Rebalancing frequency matters most.** Monthly rebalancing destroys the signal (0.14), and quarterly or six-monthly discrete rebalancing reaches only 0.40–0.47. The 6M overlapping tranches work because they average six noisy monthly readings.
- **Concentrating hurts.** Top-1 portfolios are much worse than top-2.
- **Risk-based sizing (inverse-vol, ERC, vol-target) does not improve Sharpe.** ERC looked as good in discovery but falls to 0.49 in the examined window.
- **Long-only vs long-short:** long-only top-2 has the same risk-adjusted performance (IR 0.62 vs Sharpe 0.66). It has about half the drawdown (−7% vs −12%) and half the turnover, but delivers less than half the return (1.8% vs 3.5% a year), because it runs at about half the active risk.
- **Pre-registered Rule P failed for every strong configuration.** The rule required that no single market supply more than 60% of discovery return. Every top configuration got 66–85% from the Eurozone. The only eligible configuration is z-weighted with 3M tranches (discovery 0.39).
- **Walk-forward selection** (re-picking the best of the 45 each January using only past data) earned **0.22** from 2013 to 2026. Choosing the "best construction" adds nothing out of sample.

---

## 3. Signal construction (portfolio fixed at the baseline)

Thirteen FCI variants plus one FCI+EPS variant (`signal_construction_grid.csv`). Rule S required **+0.20 discovery Sharpe** and no loss of IC. **None passed, so the base signal stays.**

| Variant | Disc IC 6M | Disc Sharpe | Examined Sharpe | Full Sharpe |
|---|---|---|---|---|
| **S0 base** (6M change ÷ expanding sd) | 0.189 | 0.71 | 0.68 | 0.66 |
| Lookback 3M / 9M / 12M | 0.12 / 0.16 / 0.18 | 0.55 / 0.67 / 0.35 | 0.54 / 0.63 / 0.45 | 0.53 / 0.61 / 0.35 |
| Rolling-36M sd scaling | 0.18 | 0.71 | **0.24** | 0.46 |
| Own z-score (country-level) | 0.17 | 0.62 | 0.64 | 0.61 |
| Absolute change, cross-sectional only | 0.09 | 0.09 | 0.43 | 0.23 |
| FCI **level** instead of change | 0.05 | 0.22 | 0.03 | 0.08 |
| 3M smoothing | 0.18 | 0.56 | 0.68 | 0.58 |
| 3/6/12M blend | 0.16 | 0.54 | 0.34 | 0.39 |
| **Hysteresis** (enter rank ≤2, exit ≥4) | 0.19 | **0.83** | **0.51** | 0.63 |
| Threshold \|z\| ≥ 0.5 | 0.19 | 0.38 | 0.58 | 0.44 |
| Absolute confirmation | 0.19 | 0.46 | 0.47 | 0.49 |

- **The base specification is already at or near the top of every sensible alternative.** Most variants are worse.
- **Hysteresis is the cautionary case.** It is the best discovery result (0.83) but falls to 0.51 in the examined window, exactly the pattern that selection noise produces.
- **Country-level normalisation is essential.** Raw cross-sectional changes are poor (0.23), because the five FCIs are on different scales.

**EPS at the portfolio level** (`eps_portfolio_test.csv`):
- Under Rule E, EPS is added to the Rule-P construction: discovery paired p = 0.050, below the 0.10 threshold.
- In the examined window it adds only +0.4% a year (p 0.43). On the baseline it **reduces** examined Sharpe (0.68 → 0.57).
- v11 showed the EPS effect is mostly a static US/Japan tilt. **The rule is honoured, but the evidence that EPS helps going forward is weak.**

---

## 4. Exploratory candidates (discovery-only; examined window labelled CONTAMINATED)

| Candidate | Disc IC 6M (t) | Disc Sharpe | *Contaminated* examined Sharpe |
|---|---|---|---|
| ERP vs credit, z 36 / 60 / 120M | 0.20 (2.3) / 0.20 (1.9) / 0.28 (1.8) | 0.35 / 0.46 / 0.00 | −0.05 |
| Trend R² 12M, unsigned (v10) | 0.05 (0.6) | 0.13 | 0.58 |
| **Trend R² 12M, signed** (pre-registered fix) | 0.18 (2.2) | 0.27 | 0.39 |
| Signed trend R² 6M / 24M | 0.10 / 0.29 (3.4) | 0.16 / 0.63 | −0.06 / 0.06 |

**ERP vs credit**
- **Rationale:** a relative risk premium. **Direction:** correct (cheap is positive).
- **Data quality is poor:**
  - The US uses a **high-yield** spread; the others are investment grade.
  - **Switzerland's spread is identical to the Eurozone's.**
  - 2Y yields were negative for 92–128 months in the EZ, CH and Japan.
- **Results:** discovery IC is reasonable but the portfolio does not convert it, and the result is sensitive to the window.

**Trend R²**
- The unsigned version was mis-specified, as predicted.
- Signing it fixes the discovery result (IC 0.05 → 0.18), which supports the correction.
- But the 24M signed version is the strongest in discovery and does nothing in the examined window.

**Neither candidate is promoted**, as pre-registered. An independent test needs data after 2026-04.

---

## 5. Data-quality opportunities (`data_improvement_opportunities.csv`)

- **The supplied "price" file contains only P/E ratios.** It matches the BEst P/E fields to within 0.2. Its Eurozone column is labelled **`MXEM Index`, which is the MSCI *Emerging Markets* ticker**; it should be MSCI EMU (`MXEMU`).
- **External data cannot be fetched from this environment.** The network policy blocks finance hosts (Yahoo, Stooq, FRED, iShares).
- **What would improve the data:**
  - Monthly **USD net total-return indices** for all five markets, e.g. the MSCI USA / EMU / UK / Switzerland / Japan Net TR USD family on Bloomberg (verify the tickers on the terminal).
  - Genuine price indices, to check the other four reconstructions.
  - **Point-in-time** consensus snapshots.
  - A Swiss-specific FCI.
- **What dividends would change:** the L/S holds small average net positions (−6% to +5% per market). A 2% dividend-yield gap moves its return by about **0.1pp a year**. Total-return data would improve accuracy but **cannot close the Sharpe gap**.

---

## 6. Net performance across cost scenarios (`candidates_by_cost.csv`, `cost_breakdown.csv`)

| Approach | 0 bps | 5 bps | 10 bps | 20 bps | Breakeven (Sharpe 0) |
|---|---|---|---|---|---|
| Baseline L/S (full) | 0.75 | 0.71 | 0.66 | 0.57 | ~83 bps |
| Long-only top2 active (full) | 0.71 | 0.67 | 0.62 | 0.54 | ~86 bps |
| Vol-targeted L/S (full) | 0.76 | 0.71 | 0.66 | 0.57 | ~81 bps |
| Pre-registered pick (full) | 0.55 | 0.51 | 0.47 | 0.39 | ~44 bps (FCI-only version) |
| Baseline with **monthly** rebalance | 0.31 | 0.23 | 0.14 | −0.02 | **~19 bps** |

- **Costs are not the binding constraint** for the 6M-tranche strategies: they stay profitable well beyond 20 bps.
- **No approach reaches Sharpe 1.0 even at zero cost.** The cost level at which Sharpe would fall below 1.0 is negative in every case.

---

## 7. Robustness and statistical limitations (`robustness_candidates.csv`, `deflated_sharpe.csv`)

| | Baseline L/S | Long-only active | Pre-registered pick |
|---|---|---|---|
| Full Sharpe, 10 bps | 0.66 | 0.62 | 0.47 |
| Without Eurozone P&L | **0.13** | 0.16 | 0.48 |
| Without US P&L | 0.37 | 0.37 | **−0.03** |
| Drop best 12 months | 0.24 | 0.17 | 0.08 |
| Lo-adjusted Sharpe | 0.59 | 0.56 | 0.52 |
| Years positive | 12/18 | 12/18 | 14/18 |

- **Every approach depends on one country.** The strong ones depend on the Eurozone; the diversified-by-rule one depends on the US. A third of the Sharpe comes from about 12 months.
- **Deflated Sharpe** of the best v13 configuration (0.67):
  - Counting only v13's runs, the probability that its true Sharpe is positive is **0.81**.
  - Counting the ~25,500 cumulative research decisions, it is **0.42**. The null's expected maximum Sharpe (0.71) is higher than what we observed.
- **Effective sample:** about 17 independent 6-month periods in the examined window, five markets, and Switzerland shares euro-area FCI and credit data.

---

## 8. Best defensible approach, and whether the objectives are achievable

**What the pre-registered rules select:** z-weighted, 3M tranches, FCI+EPS. Net of 10 bps it earns **0.57 in discovery and 0.44 examined**. It was chosen only because every stronger configuration failed the concentration rule.

**The decision that is yours, not mine:** the concentration constraint is binding.

| Option | Choice | Result (net 10 bps) |
|---|---|---|
| A | Keep the constraint and the pre-registered pick | Sharpe ~0.45, more diversified by rule |
| B | Accept the concentration and use the **long-only top-2** variant | IR 0.62, max DD −7%, 2.4× turnover. Lowest risk; the same Sharpe as L/S. |
| C | Keep the v12 baseline L/S | Sharpe 0.66, max DD −12%. Effectively a Eurozone trade. |

**Is 1.0 achievable? No, not with this data.**
- **IC ceiling:**
  - FCI's 6M IC is about 0.17–0.19, and five markets at a 6M horizon give about 8 independent bets a year. That implies an IR of about 0.5. The realised 0.66–0.75 gross is already above that.
  - **Sharpe 1.0 needs an IC of about 0.35** (at a 3M horizon, 0.25). **Sharpe 1.5 needs about 0.53.** No signal tested in v1–v13 survives validation at even half of that.
- **Breadth ceiling:** at the current IC, Sharpe 1.0 needs about 33 independent bets a year and 1.5 needs about 74. The universe offers about 8.

**What would be needed to move toward 1.0:**
1. **Much more breadth:**
   - Sector-level or country-sector cells (e.g. 5 markets × 10 sectors).
   - More countries (all ~23 developed markets, and emerging markets).
   - Futures across equity indices plus bonds and FX in the same macro framework.
   - Breadth is the only lever large enough.
2. **Additional independent signals.** Each one adds breadth only if it is uncorrelated with FCI and validated on its own.
3. **Better data.** Total returns, point-in-time consensus, and a Swiss-specific FCI improve accuracy and credibility but will not lift Sharpe by 0.3+.
4. **Fresh out-of-sample data after 2026-04.** This is the only way to validate anything new, the exploratory candidates included.

**Not done, deliberately:** relaxing the pre-registered rules after seeing results, selecting on the examined window, or adding features until the target was hit. Any of these could have produced a Sharpe above 1.0 in-sample. It would have been fake.
