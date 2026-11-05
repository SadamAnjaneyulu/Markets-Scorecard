# Unresolved issues that materially affect the investment conclusion
Recorded at v9 (revalidation phase). Ordered by impact on the conclusion.

| # | Issue | Why it matters | Can it be resolved with the supplied data? |
|---|---|---|---|
| 1 | **No signal is statistically validated.** Every validation bootstrap CI includes zero; no pillar adds incrementally with a CI excluding zero. | The scorecard's composite result rests on signals that are individually inconclusive. | No — needs more markets or out-of-sample time. |
| 2 | **Cumulative selection history cannot be priced.** v4 screened ~25,301 combinations, v8 screened 12 pillar candidates; v9's null prices only the 5 signals tested here. | All p-values are **conditional**. The true multiplicity burden is strictly larger than reported. | No — would require re-running every historical search inside one null. |
| 3 | **Validation window re-used since v3.** It has informed feature choice across v3–v9. | It is a structured re-use, not a clean hold-out; reported effect sizes are biased upward. | No — the dataset ends 2026-04. Only forward paper trading fixes this. |
| 4 | **Price return only — no dividends.** UK and Switzerland are the high-yield markets and both sit on the short side. | The bias runs *with* the recommendation, inflating apparent short-side performance. | No — no dividend or total-return series supplied. |
| 5 | **US concentration.** Four-pillar validation Sharpe collapses when the US is removed. | The portfolio result may be one country call rather than a cross-market model. | Partly — reported, not fixable. |
| 6 | **US EPS field is `Monthly_EPS`, others `BEst EPS`.** v4 §12b shows P/E × EPS reproduces the S&P 500 exactly, so it must be the same forward consensus, but vendor metadata is absent. | The micro pillar — the strongest signal — depends on this series for the market driving most P&L. | No — needs Bloomberg field verification. |
| 7 | **Point-in-time status of the consensus series is unverifiable.** Cannot tell whether stored EPS/P/E are original snapshots or restated. | Restated consensus would inject look-ahead into the micro and valuation pillars. | No — needs vendor metadata. |
| 8 | **Switzerland's credit spread and FCI are euro-area series.** | Two of five markets share macro inputs, weakening genuine cross-sectional variation. | No — no Swiss-specific series supplied. |
| 9 | **Five markets, 78 % first principal component.** Effective cross-sectional breadth is ~4 degrees of freedom per month. | Caps the statistical power available; a true IC of 0.10 is hard to separate from noise. | No — structural to the assignment. |
| 10 | **Technical pillar has no independent content.** Residualised on EPS revisions it retains 22 % of its IC (val IC +0.025, t 0.39). | The brief requires a technical signal; the evidence says it restates the micro pillar. | Resolved as a finding — must be disclosed, not fixed. |
