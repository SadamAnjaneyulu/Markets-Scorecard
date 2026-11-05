# CRISIL Assignment — Requirement-by-requirement completion checklist

Source of truth: `Assignment_Questions.docx` (CRISIL brief).
Final submission: `notebook/Markets_Scorecard_v14_FINAL.ipynb` · `output/v14/` (CSV and documentation) · `slides/Markets_Scorecard_FINAL.pptx`.
Legend: ✅ complete · ⚠️ complete with a disclosed limitation.

## Objective
| Brief | Status | Where |
|---|---|---|
| Developed-markets scorecard for US, Eurozone, UK, Switzerland, Japan, from the supplied dataset | ✅ | Notebook §1–§4 |
| Identify likely out- and under-performers over the next 3–6 months | ✅ | Every test is run at both 3M and 6M horizons. The backtest uses 6-month holding tranches. |

## Step 1 — Signal construction
| Brief | Status | Where |
|---|---|---|
| Macro signal | ✅ | FCI 6M easing (`signal_definitions.csv`, notebook §2) |
| Micro signal | ✅ | EPS revisions 6M |
| Valuation signal | ✅ | P/E relative to peers |
| Technical signal | ✅ | Low realised volatility 12M |
| Rationale, formula, direction, lookback, standardisation, data source for each | ✅ | `signal_definitions.csv`; slide 1 |
| Technical signal uses defensible price information | ✅ | Notebook §2, three checks: (1) the supplied "Price" workbook holds P/E ratios, not prices; (2) index level = P/E × EPS, and the US matches published S&P 500 returns to 0.04 pp; (3) the signal's R² on EPS revisions is 1.5%. Limitations are listed. |

## Step 2 — Predictive power assessment
| Brief | Status | Where |
|---|---|---|
| Discovery and validation results for every pillar | ✅ | `predictive_power.csv`; slide 2 |
| IC with confidence intervals | ✅ | 95% block-bootstrap CI; `ic_by_pillar.png` |
| Statistical tests and multiple-testing caveats | ✅ | HAC t, block-permutation p, and an explicit selection caveat. No pillar is claimed as significant. |
| Country-level contributions | ✅ | `country_contributions.csv` (exact decomposition: the five country terms sum to the IC) |
| 3M and 6M performance | ✅ | Both horizons, all pillars |
| Retain / provisional / rejected classification | ✅ | `signal_classification.csv`. Rules were fixed before results: Macro PROVISIONAL, Micro PROVISIONAL, Valuation REJECTED, Technical REJECTED. |

## Step 3 — Scorecard construction
| Brief | Status | Where |
|---|---|---|
| Pillar scores for all five countries | ✅ | `pillar_scores_monthly.csv`, `current_scorecard.csv`; slide 3 heatmap |
| Aggregate country scores | ✅ | Equal-weight average (25% each). Pillar contributions are in `scorecard_history.csv`. |
| Market rankings | ✅ | Monthly ranks and calls (overweight / neutral / underweight) |
| Transparent aggregation and weighting | ✅ | Notebook §4; slide 3. The reason for equal weights is stated. |
| Four-pillar scorecard is primary; FCI-only shown separately as a companion | ✅ | The companion is reported alongside, never instead |
| Weak indicators clearly labelled | ✅ | "weak: rejected predictor" labels on charts and slides |

## Step 4 — Backtesting
| Brief | Status | Where |
|---|---|---|
| Historical performance of the actual four-pillar scorecard | ✅ | `backtest_summary.csv`, `backtest_monthly.csv`; slide 4 |
| Long-only and long-short | ✅ | Long-only top-2 vs equal weight; long-short top-2 / bottom-2 |
| Equal-weight benchmark comparison | ✅ | Return, volatility, Sharpe, drawdown, information ratio |
| Cumulative returns, Sharpe, volatility, max drawdown | ✅ | `cumulative_vs_benchmark.png`, `drawdown.png` |
| Transaction costs and turnover | ✅ | 0 / 5 / 10 / 20 bps; drift-accurate turnover |
| Poor performance reported and explained, with no optimisation | ✅ | Long-short validation Sharpe −0.02 is reported as is. Single-pillar attribution shows Valuation and Technical cancelling Macro and Micro. Rules were fixed in advance. |

## Step 5 — Investment view
| Brief | Status | Where |
|---|---|---|
| Ranking of all five markets | ⚠️ | `current_scorecard.csv`; slide 5. **As of 30-Apr-2026**, the latest date common to all five supplied workbooks. |
| Concise recommendation supported by the scorecard | ✅ | Overweight US and UK, neutral Eurozone, underweight Switzerland and Japan. Low conviction, with reasons. The companion's disagreement is disclosed. |
| Up-to-date readings (Nov-2026) | ⚠️ **Not possible with comparable data** | See the note below |

**Why the readings could not be updated.** The brief allows extra data, and this was attempted. Two obstacles remain:
- **Access:** finance data hosts are blocked by the environment's network policy.
- **Comparability:** the inputs (BEst P/E, BEst EPS, GS and Bloomberg FCIs) are Bloomberg-proprietary. No free source is comparable. Mixing substitutes would combine inconsistent series, which is prohibited.

Readings after the as-of date that exist in the supplied files (EZ/JP to Jun-2026, UK/CH to Jul-2026) are shown for information only, in `info_readings_after_asof.csv`. **To refresh:** export the same tickers to date, replace the files in `data/raw/`, re-run the notebook, then run `python3 slides/build_final_ppt.py`. The as-of date is detected automatically.

## Deliverables
| Brief | Status | Where |
|---|---|---|
| 1. Python notebook: signal construction, testing, scorecard methodology, backtest. One reproducible end-to-end run. | ✅ | `Markets_Scorecard_v14_FINAL.ipynb`: 26 cells, executed, 0 errors |
| 2. CSV input and output | ✅ | **Input:** `input_monthly_panel.csv`, `signals_raw_monthly.csv`. **Output:** `pillar_scores_monthly.csv`, `scorecard_history.csv` (historical scores, ranks, calls and realised returns), `current_scorecard.csv`, `predictive_power.csv`, `country_contributions.csv`, `signal_classification.csv`, `aggregate_score_ic.csv`, `backtest_summary.csv`, `backtest_monthly.csv`, `backtest_pillar_attribution.csv` |
| 3. PowerPoint, 4–5 slides, suggested structure | ✅ | `slides/Markets_Scorecard_FINAL.pptx`, **5 slides**: methodology · signal selection and predictive power · scorecard construction · backtest results · current ranking and recommendation. Includes the ranking, pillar contributions, performance vs benchmark, and drawdown. |

## Quality requirements
| Requirement | Status | Evidence |
|---|---|---|
| Every slide figure reconciles with notebook and CSV | ✅ | `slides/check_ppt_reconciliation.py`: 112 slide numbers re-read from CSV, all match. 0 untraceable numeric tokens. |
| Previous notebooks and results preserved | ✅ | v1–v13 unchanged |
| Notebook runs start to finish | ✅ | nbconvert execute, 0 errors |
| Clear investment rationale for every indicator | ✅ | `signal_definitions.csv`; slide 1 |
| Assumptions and limitations explicit | ✅ | `output/v14/METHODOLOGY_AND_LIMITATIONS.md` (generated by the notebook); slides 1, 2 and 5 |
| No fabricated current observations or significance | ✅ | As-of date disclosed on every slide. Significance is explicitly not claimed. |
