# Methodology and Research Process
## A relative-performance scorecard for five developed equity markets

---

## 1. Investment objective

I set out to rank five developed equity markets — the **US, Eurozone, UK, Switzerland and Japan** — by their likely performance *relative to each other* over the following three to six months, and to turn that ranking into an allocation view.

The objective is deliberately relative rather than absolute. A scorecard that ranks five markets against one another does not need to forecast the direction of global equities; it needs to identify which markets are better placed than the others. Every signal is therefore standardised across the five markets each month, and every return is measured against the five-market average.

I report two horizons throughout, three months and six months, because the brief spans that range and because the two horizons do not always agree.

---

## 2. Data and preparation

### 2.1 Sources

I used only the data supplied with the assignment: five country workbooks and one combined price workbook. No external market, macroeconomic or alternative data was introduced at any stage.

The common panel runs from **2005-12 to 2026-04**, which is **245 months**. The end date is set by the earliest-ending workbook; it is the last month in which all five markets report.

### 2.2 Alignment

Each workbook is collapsed to one observation per calendar month, keeping the **last dated observation** in each month. The workbooks have slightly different observation dates — some run to the second or third of the following month — so taking the last observation in each calendar month puts every market on a common month-end footing without interpolating anything.

Missing values are not filled. Where a series does not cover a month, that month is dropped from any calculation that needs it, and the resulting sample size is reported alongside the result.

### 2.3 Data-quality findings

Five findings from the audit materially constrained what I could build.

**The combined price workbook does not contain index prices.** Its five columns are labelled with price tickers but the values range between 8 and 39 and track each workbook's forward price/earnings ratio to a median difference of approximately zero. A genuine index level for the US market over this period would be in the thousands. The workbook holds a second vintage of the same valuation ratio, not a price.

**Prices therefore had to be reconstructed** as forward price/earnings multiplied by forward earnings per share. This is an identity rather than a model, since the price/earnings ratio is defined as price divided by earnings. I validated the reconstruction for the one market where a published comparison is possible: the reconstructed US series matches published monthly index returns to a mean absolute difference of **0.039 percentage points** across eight well-known months. The other four reconstructions cannot be validated against a published index using the supplied data, so their plausibility rests on the identity holding for the same index and vintage, and on the realistic volatility and drawdown profiles reported in the notebook.

**Several series are shared across workbooks.** The equity volatility column is numerically identical in three workbooks, and the crude oil series is identical in four. The Swiss credit spread is the euro-area series, and the Swiss financial-conditions index is the euro-area index. A variable that takes the same value in every market carries no cross-sectional information for a five-market ranking, so none of these is used as a country-level signal.

**The volatility column in the UK workbook is not an equity volatility index.** It correlates 0.04 with the identical series in the other workbooks and shows no spike in October 2008 or March 2020, which any equity volatility index must. I could not identify what the series is, so I excluded it from all signal construction rather than use an unknown input.

**Returns are price returns.** No dividend data is supplied, so total returns cannot be constructed. This understates higher-yielding markets.

### 2.4 Return target

The target is the forward return of the reconstructed index in US dollars, measured relative to the five-market mean of the same month. I also computed every result on local-currency returns as a check; the conclusions do not depend on the currency choice.

---

## 3. Economic framework

I organised the research around four channels, each capturing a different reason one equity market might outperform another.

**Macro — the financial-conditions impulse.** Equity markets are claims on future cash flows discounted at a rate that moves with funding costs, credit spreads, currency levels and market volatility. When financial conditions ease, the discount rate falls and the credit available to companies and investors expands. The effect shows up in prices with a lag, which is what makes a *change* in conditions potentially useful for a three-to-six-month view rather than merely descriptive.

**Micro — earnings revision behaviour.** Analysts adjust forecasts gradually rather than all at once, and the empirical literature on post-earnings-announcement drift and revision momentum documents that prices under-react to this process [1], [2]. A market where forward earnings estimates are being raised is, on this reasoning, more likely to continue outperforming than one where they are being cut.

**Valuation — what an investor is paid to hold the market.** The forward earnings yield relative to the local risk-free rate measures the compensation for holding equities rather than government bonds. Valuation measures work over longer horizons than three to six months, so I expected this to be the weakest of the four, but a scorecard that ignores price paid would be incomplete.

**Technical — the quality of the price path.** A market trending smoothly is absorbing information gradually; a market moving in jumps is repricing in response to shocks. Smooth trends have historically been more likely to persist, which is the basis of the cross-sectional momentum literature [3].

---

## 4. Signal construction

Each pillar contributes one indicator. Every indicator is converted to a cross-sectional z-score across the five markets each month, so a score always states relative standing:

$$z_{i,t}=\frac{x_{i,t}-\bar{x}_t}{s_t}$$

A higher z is always more attractive, whatever the sign convention of the raw series.

### 4.1 Timing control

A score dated month-end *t* is matched to returns beginning at *t+1*. This one-month implementation lag is the conservative assumption: the point-in-time status of the consensus earnings data cannot be verified from the workbooks, so I do not assume a score can be acted on the moment it is observed. Every information coefficient and every backtest below uses the lag. The notebook reports the no-lag variant as a sensitivity; removing the lag changes the pillar information coefficients by between 0.001 and 0.028.

### 4.2 Macro: financial conditions impulse, six months

| | |
|---|---|
| **Formula** | (FCI_t - FCI_{t-6}) / expanding sd of that change, min 36 obs; FCI oriented so higher = easier |
| **Lookback** | 6-month change, expanding scaling |
| **Direction** | More easing is more attractive |
| **Standardisation** | Own-history scaling, then cross-sectional z |
| **Source** | Financial conditions index for each market |
| **Limitations** | Switzerland uses the euro-area index, so its macro reading is not Swiss-specific. Index construction differs between providers, which the own-history scaling partly offsets. |

Scaling the six-month change by each market's own expanding standard deviation matters because the financial-conditions indices are not on a common scale: four are index levels near 100 and one is expressed as a standard-deviation score. Without the own-history scaling, the cross-sectional z-score would be dominated by differences in index construction rather than differences in conditions.

### 4.3 Micro: earnings revision persistence, twelve months

| | |
|---|---|
| **Formula** | Share of the last 12 monthly changes in forward consensus EPS that are positive |
| **Lookback** | 12 months |
| **Direction** | A higher share of up-months is more attractive |
| **Standardisation** | Cross-sectional z |
| **Source** | Forward consensus EPS for each market |
| **Limitations** | The US uses a different EPS field from the other four markets, and that series is smoother. The point-in-time status of the consensus history cannot be verified. |

This specification replaced my original indicator, the six-month percentage change in forward earnings. Section 5 sets out the reasoning and the evidence.

### 4.4 Valuation: earnings yield spread versus own history

| | |
|---|---|
| **Formula** | (100 / forward P/E - 2-year government yield), standardised by each market's expanding mean and sd, min 36 obs |
| **Lookback** | Expanding window |
| **Direction** | A wider spread than usual is more attractive |
| **Standardisation** | Own-history z, then cross-sectional z |
| **Source** | Forward P/E and 2-year government yield for each market |
| **Limitations** | It is a valuation proxy, not an observed equity risk premium: there is no dividend or payout data and forward EPS is a consensus estimate. Its out-of-sample relationship is negative and driven by one market (§7). |

Standardising against each market's own history rather than against the other four is deliberate. Markets carry persistent valuation differences that reflect sector composition — a market heavy in technology will trade at a higher multiple than one heavy in banks for reasons that have nothing to do with whether it is currently cheap. Comparing each market against its own history isolates the part of the valuation that is unusual.

### 4.5 Technical: signed trend quality, twelve months

| | |
|---|---|
| **Formula** | sign(slope) x R-squared from a regression of log reconstructed price on a 12-month time trend |
| **Lookback** | 12 months |
| **Direction** | A smooth rising trend is more attractive |
| **Standardisation** | Cross-sectional z |
| **Source** | Reconstructed index = forward P/E x forward EPS |
| **Limitations** | Built on reconstructed prices because the dataset contains no index levels. It is arithmetically a function of the Valuation and Micro inputs and is not independent of them (§3.3, §7). |

The signing matters. An unsigned R-squared measures how *cleanly* a market is trending without regard to direction, which scores a smooth decline as attractive. Multiplying by the sign of the slope fixes that.

**I want to be explicit about what this pillar can and cannot be.** Because the reconstructed price is forward price/earnings multiplied by forward earnings, any price-based signal decomposes exactly:

$$\log\frac{P_t}{P_{t-k}} = \log\frac{PE_t}{PE_{t-k}} + \log\frac{EPS_t}{EPS_{t-k}}$$

A technical signal built on this series is arithmetically a function of the same inputs that drive the Valuation and Micro pillars. It is not an independent fourth source of information, and I do not present it as one.

---

## 5. Research and hypothesis testing

### 5.1 How the research proceeded

I began with one candidate per pillar and a straightforward design: build the indicator, standardise it across markets, and measure whether it ranked forward relative returns. The early results were encouraging in the discovery window and considerably weaker afterwards, which sent me back to the construction of the signals rather than forward to the portfolio.

The research then went through several rounds. I tested alternative lookbacks and alternative standardisation routes; I compared candidates on matched samples once I realised that different constructions start at different dates; I ran leave-one-country-out tests after finding that several apparently strong results rested on a single market; and I added walk-forward evaluation once it became clear that choosing among candidates is itself a decision that has to be tested.

Three methodological corrections changed conclusions along the way, and I record them because they matter more than any individual number.

**Matched samples.** Comparing two constructions on their own available months confounds the method with the sample. A measure needing twelve months of history starts later than one needing six, and the later sample may simply be an easier one. When I re-ran an apparently improved Micro specification on identical months, the improvement disappeared — it had been a sample-start artefact. Every comparison in this document is on matched months.

**A low regression R-squared does not establish independence.** I had argued at one point that the Technical pillar carried information independent of the others because it regressed weakly on them. That argument is wrong when the series is a deterministic non-linear function of the same inputs, which it is here. I withdrew the claim; the decomposition in section 4.5 is the honest statement.

**Choosing a construction is part of the strategy.** Evaluating the best-performing specification over the full sample overstates what could have been achieved, because the choice of specification used the whole sample. I added a walk-forward test that re-selects the specification each year using only prior data, and the gap between the two is informative in its own right.

### 5.2 Macro research

I tested five economically distinct macro channels and a composite, asking whether activity, credit or rates improved on the financial-conditions impulse.

| Candidate | IC, 6-month horizon, full sample |
|---|---|
| Financial conditions impulse 6M (retained) | +0.160 |
| Financial conditions impulse 3M | +0.106 |
| Financial conditions impulse 12M | +0.107 |
| PMI momentum 3M | -0.010 |
| PMI level versus 50 | +0.082 |
| Credit spread tightening 6M | +0.040 |
| 2Y yield decline 6M | +0.030 |
| Activity plus conditions | +0.084 |

No alternative beat the financial-conditions impulse. The result I had expected to work did not: combining activity momentum with financial conditions — the intuitive "economy accelerating *and* money easing" story — **lowered** the information coefficient from +0.160 to +0.084. PMI momentum has an information coefficient indistinguishable from zero (-0.010, t = -0.23), and the PMI level is only mildly positive and not significant. Credit spread tightening and the change in the two-year yield are weakly positive and not significant.

Credit also has a construction problem in any case: the US series is a high-yield spread while the other four are investment grade, so the markets are not being compared on the same quantity.

An earlier stage of this research, using a different scaling of the same inputs, found PMI momentum and credit tightening *negative*. I mention it because it shows how sensitive the sign of a weak signal is to construction choices. The conclusion that matters is the stable one: none of them is a reliable ranking input in this dataset, and the financial-conditions impulse is.

I retained the six-month financial-conditions impulse unchanged.

### 5.3 Micro research: the change that mattered

My original Micro indicator was the six-month percentage change in forward consensus earnings. It performed respectably in the discovery window and then weakened at the six-month horizon in the examined window, which is the pattern that usually indicates a specification is picking up something fragile.

The hypothesis I tested: **the frequency of upgrades is more informative than their size.** A single large revision can reflect an accounting change, a currency move, an index reconstitution or one dominant constituent. A market where forward earnings have been marked up in most of the last twelve months is more plausibly in a sustained upgrade cycle, and that is the thing a three-to-six-month view wants to capture.

I built two persistence measures. The first counts the share of the last twelve monthly earnings changes that are positive — equal weight on each month, no free parameters beyond the window. The second applies exponentially decaying weights to the same up-month indicator, so recent months count more.

Compared on matched months in the examined window — **100 months at the three-month horizon and 97 at six**, US dollar returns:

| Micro specification | IC, 3-month | IC, 6-month |
|---|---|---|
| EPS revision 6M (original) | +0.153 | +0.042 |
| **EPS persistence 12M (retained)** | **+0.191** | **+0.200** |
| EPS up-month EWMA12 (robustness) | +0.242 | +0.268 |

The improvement at the six-month horizon is substantial: the information coefficient rises from +0.042 to +0.200 on identical months. The persistence measure also holds up under leave-one-country-out testing, staying positive at both horizons with any single market removed.

**Why I retained the simple persistence measure rather than the exponentially weighted one.** The weighted version scores higher on this sample. I did not promote it for three reasons. It adds a decay parameter that nothing in the data pins down, and on a sample this short I cannot distinguish a genuinely better weighting scheme from a fortunate one. Both measures express the same economic idea, and when two specifications of one hypothesis differ only in degree, the one with fewer free choices is the safer thing to carry forward. And the gap between them sits well inside the bootstrap interval of either. The weighted version is kept as a robustness comparison throughout, and the original revision signal stays in every comparison table so that the change remains visible.

I also tested revision acceleration and revision momentum — the second derivative of the revision process. Neither adds information. Their six-month information coefficients are -0.016 and -0.017, and blending either with the persistence measure lowers the combined coefficient (by 0.069 and 0.064 at three months). Both were rejected.

**One result I want to state plainly, because it cuts against my choice.** I also ran a walk-forward test: each January I re-selected among the original revision signal, the persistence measure and the weighted persistence measure using only months whose forward return was already realised. At the six-month horizon that procedure chose the **weighted** version in 92% of years and never chose the simple persistence measure. Retaining the simple measure is therefore a parsimony judgement, not the evidence-ranked choice. It is a conservative one, and it does not affect the central finding: both persistence measures beat the original revision signal by a wide margin, so the improvement does not depend on which of the two I carry forward.

### 5.4 Valuation research

The earnings yield spread is a better construction than the cross-market price/earnings comparison I started with, but it does not survive out of sample.

The pattern is sharp: strongly positive in discovery (+0.295 at six months) and negative in the examined window (-0.044). I investigated whether this was driven by outliers, by the negative-policy-rate period, or by a single market.

Outliers are not the explanation: the median monthly information coefficient is +0.100, and dropping the six worst months raises the result to +0.163 while dropping the six best leaves +0.107. The negative-policy-rate hypothesis — that a nominal two-year yield behaves differently when it is below zero, which it was for a large share of the panel between 2014 and 2022 — I tested directly and it does not hold: the information coefficient is +0.106 in months with no negative yield and +0.137 in months when some market had one.

The explanation is **one market**. The US contributes -0.074 of the -0.044 examined-window total. It stayed the most expensive market on this measure for most of the period and kept outperforming. Excluding the US, the examined-window information coefficient is +0.082, which is positive and consistent with the economic hypothesis. That is a genuine finding but a narrower one than it sounds, because a five-market scorecard cannot avoid ranking the US.

A further diagnostic: the signal still ranks future *multiple expansion* out of sample. What fails is total return, because the earnings leg moves against the multiple leg. Cheap markets re-rated and simultaneously saw earnings disappoint.

I kept the pillar on the scorecard and labelled it diagnostic.

### 5.5 Technical research

I tested six price-path measures — six-month momentum, twelve-minus-one-month momentum, one-month and three-month returns, signed trend quality, and volatility-adjusted momentum — treating trend continuation and reversal as separate hypotheses. The direction of each measure was fixed on discovery-window evidence and frozen before the examined window was read, so no sign was flipped after seeing the answer.

Signed trend quality is the strongest of the six on raw numbers (+0.130 at six months, t = 2.50). The one-month and three-month returns have information coefficients close to zero in either direction, so I found no support for short-horizon reversal at country level.

Two checks stop me promoting it. First, removing the Micro and Valuation content takes away 32% of its six-month information coefficient and 52% of its three-month one — a substantial fraction of the signal is the other two pillars restated. Second, and more decisive, **excluding the US leaves -0.003** at six months. The same collapse appears across the other momentum variants: their ex-US six-month coefficients are -0.043, +0.009 and +0.006. The pillar is almost entirely a US effect.

A walk-forward re-selection among the six measures earns +0.150 at six months, against +0.164 for signed trend quality alone on the same months, so the choice among technical measures is not the problem. The problem is the dependence on one market and the arithmetic overlap with the other pillars.

This is a limitation of the supplied dataset rather than a verdict on technical signals in general. The dataset contains no index prices, so a technical pillar here cannot be independent of the pillars built from the same two inputs.

### 5.6 Machine-learning comparison

I fitted a Ridge regression on all four pillar scores, refitted monthly on an expanding window and using only months whose forward return was already realised, so that the model never sees its own future.

It did not improve on the simple equal-weight combination at either horizon (+0.112 at three months and +0.097 at six, against +0.195 and +0.219 for the equal-weight model), and it underperforms in the backtest as well. A plausible reason is that, with four correlated features, a short sample and a noisy target, the regression gives weight to the two pillars that do not generalise out of sample. I did not adopt it.

### 5.7 Original versus revised predictive model

| | Original: FCI + EPS revision 6M | Revised: FCI + EPS persistence 12M |
|---|---|---|
| IC, 3-month, examined | +0.145 | **+0.195** |
| IC, 6-month, examined | +0.079 | **+0.219** |
| 95% interval, 6-month | [-0.112, +0.254] | [+0.036, +0.391] |
| Long-short Sharpe, examined | 0.46 | **0.79** |
| Long-only information ratio, full | 0.51 | **0.59** |
| Turnover per year | 4.3x | 3.7x |

The revised model ranks better at both horizons, has the higher long-short Sharpe in the examined window, and its six-month confidence interval is the only one of the two that excludes zero. It is not better on everything: in the long-only book its volatility and maximum drawdown are slightly higher than the original's (see section 8.2).

---

## 6. Predictive-power assessment

### 6.1 Method

Predictive power is measured by the monthly **rank information coefficient**: the Spearman correlation between the five scores and the five forward relative returns in that month, averaged over months. Because scores are standardised and returns demeaned each month, the measure is scale-free and comparable across signals.

Forward returns overlap — a six-month return observed this month shares five months with the one observed next month — so adjacent monthly information coefficients are dependent. Significance therefore uses a **HAC t-statistic** [4] with lags equal to the horizon and a **moving-block bootstrap** with block length twice the horizon, a close relative of the stationary bootstrap [5], which preserves the dependence structure when resampling.

The sample is split into a **discovery window** ending December 2016 and an **examined window** starting July 2017, with a six-month embargo between them so that no training observation's forward return overlaps the examined period.

### 6.2 Results

| Pillar | IC 3M, discovery → examined | IC 6M, discovery → examined | 95% interval, 6M examined | Label |
|---|---|---|---|---|
| Macro | +0.076 → +0.158 | +0.175 → +0.150 | [-0.018, +0.336] | PREDICTIVE (provisional) |
| Micro | +0.129 → +0.191 | +0.174 → +0.200 | [+0.019, +0.398] | PREDICTIVE (provisional) |
| Valuation | +0.171 → -0.063 | +0.295 → -0.044 | [-0.254, +0.146] | DIAGNOSTIC |
| Technical | +0.035 → +0.149 | +0.137 → +0.140 | [+0.005, +0.297] | DIAGNOSTIC |

### 6.3 What this does and does not establish

Three limits apply to every number above, and I state them rather than bury them.

The indicators were selected through an extended research process. In a sample this short, a nominal five per cent test over-rejects, and in an earlier audit the selection-adjusted p-values for the strongest candidates sat in the region of 0.16 to 0.20. **No pillar is statistically significant** once the search is accounted for.

The examined window has been looked at repeatedly across the research. It is **not untouched holdout data** and I do not describe it as such. This is precisely why leave-one-country-out and walk-forward tests carry more weight in my conclusions than the examined information coefficient on its own.

What the evidence supports is an **improved and more stable historical relationship** that justifies running the model forward under monitoring. It does not support a claim of established predictive power. The distinction is not a formality: the first implies a hypothesis worth testing on new data, the second implies a result one can size positions against with confidence.

---

## 7. Scorecard construction

### 7.1 Method

**Pillar score.** The cross-sectional z-score of each indicator across the five markets, each month.

**Diagnostic score.** The equal-weight average of all four pillar scores. Each pillar contributes one quarter of its z-score, so contributions are additive and can be read directly off a chart.

**Predictive score.** The equal-weight average of the two pillars that carry evidence — Macro and Micro. The two diagnostic pillars keep their scores and their contributions on the scorecard but receive **no predictive weight**. They are neither deleted nor given artificial importance.

**Weights are equal and fixed.** I did not fit weights to historical performance. With four correlated pillars, roughly seventeen independent six-month periods in the examined window and no pillar statistically significant on its own, any fitted weighting would be optimisation on the same data used to judge the result. The Ridge comparison in section 5.6 is the test of whether fitting weights helps, and it does not.

**Rankings** run from 1 (most attractive) to 5. Ranks one and two are overweight, three is neutral, four and five are underweight. The three-month and six-month rankings are identical because the scores are horizon-independent; what differs between horizons is the evidence supporting them.

### 7.2 Predictive power of the two scores

| Score | IC 3M, discovery → examined | IC 6M, discovery → examined |
|---|---|---|
| Diagnostic (four pillars) | +0.204 → +0.095 | +0.333 → +0.113 |
| Predictive (Macro + Micro) | +0.163 → +0.195 | +0.278 → +0.219 |

The four-pillar score is stronger in discovery and weaker in the examined window. That is exactly what carrying two pillars that fail out of sample should do, and it is the reason both views are reported side by side rather than one being presented alone.

---

## 8. Backtesting

### 8.1 Portfolio rules

The rules were fixed before testing and not adjusted afterwards.

- A score dated month-end *t* is acted on from *t+1*.
- **Long only:** 50 per cent in each of the two highest-ranked markets, against an equal-weight benchmark of 20 per cent in each of the five.
- **Long short:** plus 50 per cent in each of the top two and minus 50 per cent in each of the bottom two. The book is self-financing, so its Sharpe ratio uses a zero financing rate.
- **Six-month overlapping tranches.** Each month one sixth of the book is formed and held for six months. This matches the forecast horizon and avoids betting the whole portfolio on a single month's reading.
- Positions **drift with prices** inside a tranche, and turnover includes the re-trading that drift creates.
- **Costs** are charged one-way on traded weight across both legs, at 0, 5, 10 and 20 basis points.
- The benchmark is carried cost-free, which is conservative for the strategy.

### 8.2 Results, net of 10 basis points

| | Revised, long only | Original, long only | Equal-weight benchmark | Revised, long short |
|---|---|---|---|---|
| Return % p.a. | 9.9 | 9.2 | 7.2 | 4.8 |
| Volatility % p.a. | 14.4 | 13.9 | 14.3 | 7.0 |
| Sharpe | 0.73 | 0.70 | 0.56 | 0.71 |
| Maximum drawdown % | -28.5 | -27.4 | -27.2 | -15.5 |
| Turnover per year | 1.8x | 2.1x | — | 3.7x |
| Information ratio vs benchmark | 0.59 | 0.51 | — | — |
| **Examined-window Sharpe** | 0.76 | 0.65 | 0.55 | 0.79 |

Backtest returns run from 2009-07 to 2026-04.

### 8.3 How the revised Micro signal changes the result

The clearest effect is in the long-short book over the examined window, where the Sharpe ratio rises from 0.46 to 0.79. In the long-only book the information ratio against the benchmark rises from 0.51 to 0.59. The revised signal also trades less than the original, at 3.7 times a year against 4.3, which is consistent with a measure built on a twelve-month count rather than a six-month change.

### 8.4 Model comparison in the backtest

| Model | Long-only Sharpe | Long-only IR | Long-short Sharpe, full | Long-short Sharpe, examined | Turnover |
|---|---|---|---|---|---|
| Original: FCI + EPS revision 6M | 0.70 | 0.51 | 0.55 | 0.46 | 4.3x |
| Macro only: FCI 6M | 0.70 | 0.66 | 0.75 | 0.74 | 4.9x |
| Micro only: EPS persistence 12M | 0.75 | 0.28 | 0.54 | 0.69 | 2.7x |
| Revised: FCI + EPS persistence | 0.73 | 0.59 | 0.71 | 0.79 | 3.7x |
| Ridge challenger (4 pillars) | 0.60 | 0.36 | 0.36 | 0.26 | 3.0x |

### 8.5 Transaction-cost sensitivity

The revised long-short book returns a Sharpe ratio of 0.76 gross, 0.74 at 5 basis points, 0.71 at 10 and 0.66 at 20. Costs are not the binding constraint on this strategy at any plausible level for developed-market index exposure.

---

## 9. Investment view

**As of 2026-04.** This is the latest ranking the supplied dataset supports. The panel ends on 30 April 2026 because that is the last month in which all five markets report. It is not a reading of current market conditions, and I do not present it as one.

| Rank | Market | Predictive score | Four-pillar score | Classification | Principal reason |
|---|---|---|---|---|---|
| 1 | US | +1.16 | +0.56 | OVERWEIGHT | Forward earnings were marked up in every one of the last twelve months, the only market in the panel to do so, and it has the strongest financial-conditions impulse. It leads on both pillars that carry weight. |
| 2 | Eurozone | +0.33 | -0.04 | OVERWEIGHT | Eleven upgrade months out of twelve, level with the UK for second on earnings persistence, and a positive financial-conditions impulse. |
| 3 | Japan | -0.36 | -0.13 | NEUTRAL | Below average on both pillars that carry weight, but not by enough to justify an underweight: ten upgrade months and a mildly negative financial-conditions impulse. |
| 4 | Switzerland | -0.51 | -0.17 | UNDERWEIGHT | The weakest earnings persistence in the panel at nine upgrade months out of twelve, with no offsetting macro support. |
| 5 | UK | -0.62 | -0.21 | UNDERWEIGHT | Earnings persistence is respectable at eleven months, but the financial-conditions impulse is much the worst in the panel and dominates its score. |

The two views — the four-pillar diagnostic scorecard and the predictive score — agree on **all five** classifications this month. That is not always the case, and when they diverge the predictive view is the one carrying out-of-sample evidence while the four-pillar view is the complete framework.

**Conviction is highest on the United States and low on the ordering of the rest.** The US leads on both pillars that carry evidence, and it has held first place in 6 of the last eight months. The Eurozone is separated from third place by 0.70 on the predictive score, but the bottom three are tightly bunched — Japan, Switzerland and the UK sit within about 0.26 of one another — so the ordering among them carries little information. The UK's underweight is the best supported of the three because its financial-conditions reading is genuinely the weakest in the panel; Switzerland's rests on a narrower margin over Japan.

Rankings are also not stable month to month. In the final month the UK moved from rank 1 to rank 5, and the Eurozone from rank 3 to rank 2. The six-month tranche construction in the backtest exists precisely because single-month rankings are noisy, and a position taken from one month's ranking should be sized accordingly.

The main risk to this view is that it rests on two pillars, neither statistically significant, measured on a dataset that ends seven months before the submission date.

---

## 10. Limitations and further improvements

**Synthetic prices.** The dataset contains no index levels. Prices are reconstructed from an identity and validated against a published index for one market only. The Technical pillar is consequently a function of the Valuation and Micro inputs rather than an independent source.

**Currency and dividends.** Returns are price returns in US dollars. Without dividend data, higher-yielding markets are understated in both the target and the backtest. Results were also computed in local currency and do not depend on the choice.

**Earnings comparability.** The US uses a different forward-earnings field from the other four markets, and that series is noticeably smoother with fewer declining months. This affects the Micro pillar directly, which is why the leave-one-country-out test matters so much in section 5.3.

**Point-in-time history.** Whether the consensus valuation and earnings series are point-in-time snapshots or have been restated cannot be verified from the workbooks. The one-month implementation lag limits but does not eliminate the exposure to this.

**Sample size.** Five markets and roughly seventeen independent six-month periods in the examined window. Confidence intervals are wide, and a single market can move a result materially — as the Valuation pillar demonstrates.

**Multiple testing.** A long research process preceded these four indicators. The honest reading of every statistic here is that it is provisional.

**Country concentration.** Several results depend heavily on the US. I tested for this systematically rather than discovering it late, and the two retained pillars are the two that survive it.

### What I would do next

Run the frozen specification forward on new months without refitting, and track its information coefficient. That is the only test that has not already been contaminated by the research process.

Obtain total-return indices and a point-in-time consensus history. Both remove a limitation rather than working around it.

Widen the cross-section. Five markets is the binding constraint on how much any ranking signal can deliver [6], and it is the reason confidence intervals here are as wide as they are.

### What I take from the research

The most useful thing I learned was methodological rather than economic: **how a signal is measured can matter more than what it measures.** The Micro pillar did not change its economic content between the original and revised specifications — both are statements about forward earnings revisions. Changing from the size of revisions to their frequency raised the six-month examined information coefficient from +0.042 to +0.200. The second lesson was how easily a comparison can mislead when two constructions are evaluated on different samples, and how often an apparently strong result turns out to rest on a single market.

The hypotheses that remain provisional are both of the ones I retained. The financial-conditions impulse and earnings-revision persistence are supported by the evidence available, they survive the robustness tests I could run, and neither is proven.

---

## References

[1] Post-earnings-announcement drift: delayed price response or risk premium? *Journal of Accounting Research*, 27 (Supplement), 1989, 1–36.

[2] Momentum strategies. *Journal of Finance*, 51(5), 1996, 1681–1713.

[3] Value and momentum everywhere. *Journal of Finance*, 68(3), 2013, 929–985.

[4] A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 1987, 703–708.

[5] The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1994, 1303–1313.

[6] *Active Portfolio Management: A Quantitative Approach for Producing Superior Returns and Controlling Risk*, 2nd edition. McGraw-Hill, 2000.
