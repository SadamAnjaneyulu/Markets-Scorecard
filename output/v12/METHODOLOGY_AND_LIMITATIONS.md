# Developed-Markets Equity Scorecard — Methodology and Limitations

Deliverable notebook: `notebook/Markets_Scorecard_v12.ipynb`. Outputs: `output/v12/`. Audit: `output/v11/AUDIT_REPORT.md`.

## 1. Objective
Rank the US, Eurozone, UK, Switzerland and Japan by expected **relative** USD equity performance over the next 3–6 months.

The work produces two separate outputs:
- **Diagnostic scorecard** — one indicator for each pillar the brief asks for (Macro, Micro, Valuation, Technical), each labelled with its validation status.
- **Predictive score** — only the signal(s) whose out-of-sample evidence survives audit. That is the **Macro FCI 6M signal alone**.

## 2. Data (only the supplied workbooks)
| Item | Construction |
|---|---|
| Panel | Monthly, last observation per month, 2005-12 → **2026-04** (245 months) |
| As-of date | **2026-04-30** — the last month in which all five markets report. The US file binds. EZ/JP (to 2026-06) and UK/CH (to 2026-07) readings beyond that are shown as information only. Nothing is extrapolated. |
| Price | Implied index level = BEst P/E × forward EPS. This is an accounting identity; the US series matches S&P 500 monthly returns to ~0.04pp. **Price return only.** |
| USD conversion | EURUSD, GBPUSD direct; USDCHF, USDJPY inverted |
| FCI | Goldman Sachs FCI (US, UK, Japan; **euro-area GSEAFCI for Switzerland**) and Bloomberg BFCIEU (EZ), oriented so higher = easier |
| EPS | BEst forward EPS; **US uses `Monthly_EPS`** |
| Missing data | None in the core fields within the panel. The undated rows in the UK (15) and CH (113) files are pre-sample history without P/E or EPS, so they have no effect. |

Input CSV: `input_monthly_panel.csv`.

## 3. Indicators (one per pillar)
| Pillar | Indicator | Formula at month-end t |
|---|---|---|
| Macro | FCI 6M easing | (FCI_t − FCI_{t−6}) ÷ expanding sd of that change (≥36 obs burn-in) |
| Micro | EPS revision 6M | EPS_t / EPS_{t−6} − 1 |
| Valuation | P/E vs peers | −expanding z (≥60 obs) of P/E_t ÷ 5-market average P/E_t |
| Technical | Low realised vol | −sd of the last 12 monthly local returns |

Each indicator is z-scored across the five markets every month. The pillar score is that z-score. The diagnostic aggregate is the equal-weight average of the four. Rank 1 is the most attractive.

## 4. Testing predictive power
- **Target:** USD price return from month-end t to t+h, minus the 5-market mean. h = 3 and 6.
- **Statistic:** monthly Spearman rank IC across the five markets, averaged over time.
- **Split:**
  - Discovery runs to 2016-12.
  - A 6-month embargo follows.
  - Validation runs 2017-07 → 2026-01 (3M) / 2025-10 (6M).
  - Each indicator is evaluated on every month in which it is defined. The v11 audit showed that earlier "common samples" had silently dropped 16–27 stress months.
- **Inference:**
  - HAC t (lags = h).
  - Moving-block bootstrap (L = 2h).
  - Block permutation of country labels in h-month blocks (5,000 draws, add-one p).
  - Best-of-family null over the 19 Macro/Micro variants.
  - Size simulation under a no-predictability null.

**Results (validation, 3M / 6M):**

| Pillar | Val IC 3M (t) | Val IC 6M (t) | Status |
|---|---|---|---|
| Macro FCI 6M | +0.127 (1.74) | +0.173 (1.96) | **PROVISIONAL — predictive** |
| Micro EPS 6M | +0.131 (1.70) | +0.074 (0.78) | PROVISIONAL — diagnostic only |
| Valuation P/E vs peers | −0.108 (−1.57) | −0.112 (−1.25) | REJECTED — context only |
| Technical low vol | −0.066 (−1.01) | −0.029 (−0.28) | REJECTED — context only |

**Why FCI and not EPS:**
- Removing each market's average return over the sample leaves FCI's timing IC largely intact: +0.161 (t 1.91) at 6M.
- The same step roughly halves EPS's IC: +0.072 (t 0.99) at 3M and +0.012 at 6M. Most of the EPS result is a persistent tilt toward the US, which outperformed by about 5% a year.
- Neither signal adds to the other out of sample in either direction.

**Why the diagnostic aggregate is not used:** its validation IC is −0.037 (3M) / −0.032 (6M), and its long-short backtest loses money in validation.

## 5. Backtest rules (fixed in advance)
- Signal at month-end t; trade at t; earn the month t+1 USD price return.
- **Long-short:** +50% in each top-2 market, −50% in each bottom-2.
- **Long-only:** 50% in each top-2 market vs a 20% equal-weight benchmark.
- **6-month overlapping tranches:** holdings are the average of the last six target portfolios.
- **Costs:** one-way bps × Σ|Δweight|, on a grid of 0 / 5 / 10 / 20 bps.

**Predictive score (FCI 6M), validation 2017-08 → 2026-04:**

| Book | Cost | Return % p.a. | Sharpe | Max DD % | Turnover p.a. |
|---|---|---|---|---|---|
| Long-short | 0 bps | +3.99 | 0.77 | −8.7 | 4.6× |
| Long-short | 10 bps | +3.51 | 0.68 | −9.4 | 4.6× |
| Long-short | 20 bps | +3.04 | 0.59 | −10.1 | 4.6× |
| Long-only active vs EW | 10 bps | +1.65 | 0.63 | −4.5 | 2.4× |
| *Diagnostic 4-pillar L/S (comparison)* | 10 bps | −0.43 | −0.03 | −19.1 | 3.1× |

Over the common window (2010-12 → 2026-04) the long-short earns +3.21% p.a. net of 10 bps (Sharpe 0.62, max DD −11.9%).

The bootstrap 95% CI for the mean in validation spans zero: [−0.3, +7.9]% p.a. All rows are in `backtest_summary.csv`.

## 6. Current view (as of 2026-04-30)
- **Latest signal (new tranche):**
  - Overweight **US, Switzerland**.
  - Neutral **Eurozone**.
  - Underweight **Japan, UK**.
- **Book held under the tranche rule:** UK +33%, Japan +25%, US −8%, Switzerland −8%, Eurozone −42%.
  - The April reading reversed the Nov–Mar rankings.
  - The book moves toward the new signal only if the signal persists.
- **Context:** the cross-market spread of FCI readings is at the 3rd percentile of its 2009–2026 history. Ranks changed by 6.4 places per month on average over the last six months. The ranking therefore rests on small differences. v10 found no evidence that dispersion predicts IC, so this is not used to scale conviction.
- **Conviction: LOW.**

## 7. Limitations
**Unresolved with the data provided**
1. **Price return, not total return.** Higher-yielding markets (UK) are understated. A carry stress of ±4% p.a. on any single market moves validation ICs by ≤0.03, but backtest returns are still biased.
2. **Point-in-time status of consensus data is unknown.** If EPS or P/E history were restated, EPS-revision results would be biased upward. A 1M reporting lag barely changes the 3M result. Longer lags weaken it.
3. **Stale data.** The ranking is seven months old at the time of writing (2026-11).

**Statistical**
- No signal is significant after accounting for the search that produced it. Best-of-family p is 0.16–0.20; the project made ~25,500 cumulative selection decisions.
- HAC and bootstrap tests over-reject in this sample: 6–9% size at a nominal 5%, up to 17% if market drift is kept.
- The effective sample is small: about 17 independent 6-month periods in validation, and five markets, one of which (CH) shares euro-area FCI and credit data.

**Construction**
- US EPS uses a different field (`Monthly_EPS`). It is smoother and declines less often than the BEst series.
- FCI for Switzerland is a euro-area index, so the Macro pillar carries no Swiss-specific information.
- Credit spreads mix US high-yield with investment-grade elsewhere. They are not used in the final indicators.
- At 3M, FCI depends on the US: ex-US validation IC is +0.060 (t 0.72). At 6M it does not (+0.160, t 1.92). This is why the predictive horizon is 6M.
- Tranches are modelled at constant weight. Intra-tranche drift is ignored, and the benchmark is cost-free.

**Exploratory, not used:** ERP vs credit, and trend-quality R². Both were identified after the validation window had been seen. Trend R² is unsigned and needs a pre-registered signed version tested on post-2026-04 data.

## 8. Next steps
1. Paper-track the FCI signal forward from the next data delivery. No re-fitting.
2. Obtain dividend or total-return data and a point-in-time consensus history.
3. Pre-register the signed trend-quality signal and ERP vs credit before any new data is seen.
