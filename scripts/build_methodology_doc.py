import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]; V = ROOT / 'output' / 'final'
F = json.load(open(V / 'presentation_figures.json'))
_sc = pd.read_csv(V / 'signal_comparison.csv').set_index(['horizon', 'target', 'model'])
F.setdefault('micro_matched_months_6M', int(_sc.loc[(6, 'USD', 'EPS revision 6M only'), 'months']))
F.setdefault('micro_old_6M', float(_sc.loc[(6, 'USD', 'EPS revision 6M only'), 'IC']))
F.setdefault('micro_new_6M', float(_sc.loc[(6, 'USD', 'EPS positive-month share 12M'), 'IC']))
F.setdefault('micro_ewma_6M', float(_sc.loc[(6, 'USD', 'EPS up-month EWMA12'), 'IC']))
F.setdefault('micro_old_3M', float(_sc.loc[(3, 'USD', 'EPS revision 6M only'), 'IC']))
F.setdefault('micro_new_3M', float(_sc.loc[(3, 'USD', 'EPS positive-month share 12M'), 'IC']))
pp = pd.read_csv(V / 'predictive_power.csv').set_index(['pillar', 'horizon', 'window'])
sig = pd.read_csv(V / 'signal_definitions.csv').set_index('pillar')
mc = pd.read_csv(V / 'model_comparison.csv').set_index('model')
sc = pd.read_csv(V / 'signal_comparison.csv').set_index(['horizon', 'target', 'model'])
cls = pd.read_csv(V / 'signal_classification.csv', index_col=0)
rob = pd.read_csv(V / 'robustness_summary.csv').set_index(['pillar', 'horizon'])
cur = pd.read_csv(V / 'current_ranking.csv').set_index('market')
sic = pd.read_csv(V / 'scorecard_ic.csv').set_index(['score', 'horizon', 'window'])
bt = pd.read_csv(V / 'backtest_performance_summary.csv').set_index(['window', 'model', 'book', 'cost_bps'])
mac = pd.read_csv(V / 'macro_research_comparison.csv').set_index(['candidate', 'horizon'])
ts = pd.read_csv(V / 'timing_sensitivity.csv').set_index(['pillar', 'horizon'])
PILLARS = ['Macro', 'Micro', 'Valuation', 'Technical']
sec = pd.read_csv(V / 'micro_second_order_test.csv').set_index(['candidate', 'horizon'])
mwf = pd.read_csv(V / 'micro_walk_forward.csv').set_index('horizon')
vs = pd.read_csv(V / 'valuation_sensitivity.csv').set_index('check')
ta = pd.read_csv(V / 'technical_alternatives.csv').set_index(['measure', 'horizon'])
td = pd.read_csv(V / 'technical_diagnostic.csv').set_index('horizon')
twf = pd.read_csv(V / 'technical_walk_forward.csv').iloc[0]
vcc = pd.read_csv(V / 'valuation_country_contribution.csv').set_index('market')
MK = F['ranking_order']
n = lambda x: f'{x:+.3f}'
b = lambda w, m, bk, c, col: float(bt.loc[(w, m, bk, c), col])
REV, ORIG = 'Revised: FCI + EPS persistence', 'Original: FCI + EPS revision 6M'

reason = {
 'US': 'Forward earnings were marked up in every one of the last twelve months, the only market in the panel to do so, and it has the strongest financial-conditions impulse. It leads on both pillars that carry weight.',
 'Eurozone': 'Eleven upgrade months out of twelve, level with the UK for second on earnings persistence, and a positive financial-conditions impulse.',
 'Japan': 'Below average on both pillars that carry weight, but not by enough to justify an underweight: ten upgrade months and a mildly negative financial-conditions impulse.',
 'Switzerland': 'The weakest earnings persistence in the panel at nine upgrade months out of twelve, with no offsetting macro support.',
 'UK': 'Earnings persistence is respectable at eleven months, but the financial-conditions impulse is much the worst in the panel and dominates its score.'}

doc = f"""# Methodology and Research Process
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

The common panel runs from **{F['panel_start']} to {F['as_of']}**, which is **{F['panel_months']} months**. The end date is set by the earliest-ending workbook; it is the last month in which all five markets report.

### 2.2 Alignment

Each workbook is collapsed to one observation per calendar month, keeping the **last dated observation** in each month. The workbooks have slightly different observation dates — some run to the second or third of the following month — so taking the last observation in each calendar month puts every market on a common month-end footing without interpolating anything.

Missing values are not filled. Where a series does not cover a month, that month is dropped from any calculation that needs it, and the resulting sample size is reported alongside the result.

### 2.3 Data-quality findings

Five findings from the audit materially constrained what I could build.

**The combined price workbook does not contain index prices.** Its five columns are labelled with price tickers but the values range between 8 and 39 and track each workbook's forward price/earnings ratio to a median difference of approximately zero. A genuine index level for the US market over this period would be in the thousands. The workbook holds a second vintage of the same valuation ratio, not a price.

**Prices therefore had to be reconstructed** as forward price/earnings multiplied by forward earnings per share. This is an identity rather than a model, since the price/earnings ratio is defined as price divided by earnings. I validated the reconstruction for the one market where a published comparison is possible: the reconstructed US series matches published monthly index returns to a mean absolute difference of **{F['reconstruction_mad_pp']:.3f} percentage points** across eight well-known months. The other four reconstructions cannot be validated against a published index using the supplied data, so their plausibility rests on the identity holding for the same index and vintage, and on the realistic volatility and drawdown profiles reported in the notebook.

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

$$z_{{i,t}}=\\frac{{x_{{i,t}}-\\bar{{x}}_t}}{{s_t}}$$

A higher z is always more attractive, whatever the sign convention of the raw series.

### 4.1 Timing control

A score dated month-end *t* is matched to returns beginning at *t+1*. This one-month implementation lag is the conservative assumption: the point-in-time status of the consensus earnings data cannot be verified from the workbooks, so I do not assume a score can be acted on the moment it is observed. Every information coefficient and every backtest below uses the lag. The notebook reports the no-lag variant as a sensitivity; removing the lag changes the pillar information coefficients by between {ts['difference'].abs().min():.3f} and {ts['difference'].abs().max():.3f}.

### 4.2 Macro: financial conditions impulse, six months

| | |
|---|---|
| **Formula** | {sig.loc['Macro', 'formula']} |
| **Lookback** | {sig.loc['Macro', 'lookback']} |
| **Direction** | {sig.loc['Macro', 'direction']} |
| **Standardisation** | {sig.loc['Macro', 'standardisation']} |
| **Source** | {sig.loc['Macro', 'source']} |
| **Limitations** | {sig.loc['Macro', 'limitations']} |

Scaling the six-month change by each market's own expanding standard deviation matters because the financial-conditions indices are not on a common scale: four are index levels near 100 and one is expressed as a standard-deviation score. Without the own-history scaling, the cross-sectional z-score would be dominated by differences in index construction rather than differences in conditions.

### 4.3 Micro: earnings revision persistence, twelve months

| | |
|---|---|
| **Formula** | {sig.loc['Micro', 'formula']} |
| **Lookback** | {sig.loc['Micro', 'lookback']} |
| **Direction** | {sig.loc['Micro', 'direction']} |
| **Standardisation** | {sig.loc['Micro', 'standardisation']} |
| **Source** | {sig.loc['Micro', 'source']} |
| **Limitations** | {sig.loc['Micro', 'limitations']} |

This specification replaced my original indicator, the six-month percentage change in forward earnings. Section 5 sets out the reasoning and the evidence.

### 4.4 Valuation: earnings yield spread versus own history

| | |
|---|---|
| **Formula** | {sig.loc['Valuation', 'formula']} |
| **Lookback** | {sig.loc['Valuation', 'lookback']} |
| **Direction** | {sig.loc['Valuation', 'direction']} |
| **Standardisation** | {sig.loc['Valuation', 'standardisation']} |
| **Source** | {sig.loc['Valuation', 'source']} |
| **Limitations** | {sig.loc['Valuation', 'limitations']} |

Standardising against each market's own history rather than against the other four is deliberate. Markets carry persistent valuation differences that reflect sector composition — a market heavy in technology will trade at a higher multiple than one heavy in banks for reasons that have nothing to do with whether it is currently cheap. Comparing each market against its own history isolates the part of the valuation that is unusual.

### 4.5 Technical: signed trend quality, twelve months

| | |
|---|---|
| **Formula** | {sig.loc['Technical', 'formula']} |
| **Lookback** | {sig.loc['Technical', 'lookback']} |
| **Direction** | {sig.loc['Technical', 'direction']} |
| **Standardisation** | {sig.loc['Technical', 'standardisation']} |
| **Source** | {sig.loc['Technical', 'source']} |
| **Limitations** | {sig.loc['Technical', 'limitations']} |

The signing matters. An unsigned R-squared measures how *cleanly* a market is trending without regard to direction, which scores a smooth decline as attractive. Multiplying by the sign of the slope fixes that.

**I want to be explicit about what this pillar can and cannot be.** Because the reconstructed price is forward price/earnings multiplied by forward earnings, any price-based signal decomposes exactly:

$$\\log\\frac{{P_t}}{{P_{{t-k}}}} = \\log\\frac{{PE_t}}{{PE_{{t-k}}}} + \\log\\frac{{EPS_t}}{{EPS_{{t-k}}}}$$

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
| Financial conditions impulse 6M (retained) | {n(mac.loc[('FCI easing 6M (retained)', '6M'), 'IC_full'])} |
| Financial conditions impulse 3M | {n(mac.loc[('FCI easing 3M', '6M'), 'IC_full'])} |
| Financial conditions impulse 12M | {n(mac.loc[('FCI easing 12M', '6M'), 'IC_full'])} |
| PMI momentum 3M | {n(mac.loc[('PMI momentum 3M', '6M'), 'IC_full'])} |
| PMI level versus 50 | {n(mac.loc[('PMI level versus 50', '6M'), 'IC_full'])} |
| Credit spread tightening 6M | {n(mac.loc[('Credit spread tightening 6M', '6M'), 'IC_full'])} |
| 2Y yield decline 6M | {n(mac.loc[('2Y yield decline 6M', '6M'), 'IC_full'])} |
| Activity plus conditions | {n(mac.loc[('Activity plus conditions (PMI 3M + FCI 6M)', '6M'), 'IC_full'])} |

No alternative beat the financial-conditions impulse. The result I had expected to work did not: combining activity momentum with financial conditions — the intuitive "economy accelerating *and* money easing" story — **lowered** the information coefficient from {n(mac.loc[('FCI easing 6M (retained)', '6M'), 'IC_full'])} to {n(mac.loc[('Activity plus conditions (PMI 3M + FCI 6M)', '6M'), 'IC_full'])}. PMI momentum has an information coefficient indistinguishable from zero ({n(mac.loc[('PMI momentum 3M', '6M'), 'IC_full'])}, t = {mac.loc[('PMI momentum 3M', '6M'), 'HAC_t_full']:.2f}), and the PMI level is only mildly positive and not significant. Credit spread tightening and the change in the two-year yield are weakly positive and not significant.

Credit also has a construction problem in any case: the US series is a high-yield spread while the other four are investment grade, so the markets are not being compared on the same quantity.

An earlier stage of this research, using a different scaling of the same inputs, found PMI momentum and credit tightening *negative*. I mention it because it shows how sensitive the sign of a weak signal is to construction choices. The conclusion that matters is the stable one: none of them is a reliable ranking input in this dataset, and the financial-conditions impulse is.

I retained the six-month financial-conditions impulse unchanged.

### 5.3 Micro research: the change that mattered

My original Micro indicator was the six-month percentage change in forward consensus earnings. It performed respectably in the discovery window and then weakened at the six-month horizon in the examined window, which is the pattern that usually indicates a specification is picking up something fragile.

The hypothesis I tested: **the frequency of upgrades is more informative than their size.** A single large revision can reflect an accounting change, a currency move, an index reconstitution or one dominant constituent. A market where forward earnings have been marked up in most of the last twelve months is more plausibly in a sustained upgrade cycle, and that is the thing a three-to-six-month view wants to capture.

I built two persistence measures. The first counts the share of the last twelve monthly earnings changes that are positive — equal weight on each month, no free parameters beyond the window. The second applies exponentially decaying weights to the same up-month indicator, so recent months count more.

Compared on matched months in the examined window — **{F['micro_matched_months_3M']} months at the three-month horizon and {F['micro_matched_months_6M']} at six**, US dollar returns:

| Micro specification | IC, 3-month | IC, 6-month |
|---|---|---|
| EPS revision 6M (original) | {n(F['micro_old_3M'])} | {n(F['micro_old_6M'])} |
| **EPS persistence 12M (retained)** | **{n(F['micro_new_3M'])}** | **{n(F['micro_new_6M'])}** |
| EPS up-month EWMA12 (robustness) | {n(float(sc.loc[(3, 'USD', 'EPS up-month EWMA12'), 'IC']))} | {n(F['micro_ewma_6M'])} |

The improvement at the six-month horizon is substantial: the information coefficient rises from {n(F['micro_old_6M'])} to {n(F['micro_new_6M'])} on identical months. The persistence measure also holds up under leave-one-country-out testing, staying positive at both horizons with any single market removed.

**Why I retained the simple persistence measure rather than the exponentially weighted one.** The weighted version scores higher on this sample. I did not promote it for three reasons. It adds a decay parameter that nothing in the data pins down, and on a sample this short I cannot distinguish a genuinely better weighting scheme from a fortunate one. Both measures express the same economic idea, and when two specifications of one hypothesis differ only in degree, the one with fewer free choices is the safer thing to carry forward. And the gap between them sits well inside the bootstrap interval of either. The weighted version is kept as a robustness comparison throughout, and the original revision signal stays in every comparison table so that the change remains visible.

I also tested revision acceleration and revision momentum — the second derivative of the revision process. Neither adds information. Their six-month information coefficients are {n(sec.iloc[1]['IC_full'])} and {n(sec.iloc[3]['IC_full'])}, and blending either with the persistence measure lowers the combined coefficient (by {abs(sec.iloc[0]['change_in_IC_when_added_to_persistence']):.3f} and {abs(sec.iloc[2]['change_in_IC_when_added_to_persistence']):.3f} at three months). Both were rejected.

**One result I want to state plainly, because it cuts against my choice.** I also ran a walk-forward test: each January I re-selected among the original revision signal, the persistence measure and the weighted persistence measure using only months whose forward return was already realised. At the six-month horizon that procedure chose the **weighted** version in {mwf.loc['6M','share_of_years_EWMA_chosen']:.0%} of years and never chose the simple persistence measure. Retaining the simple measure is therefore a parsimony judgement, not the evidence-ranked choice. It is a conservative one, and it does not affect the central finding: both persistence measures beat the original revision signal by a wide margin, so the improvement does not depend on which of the two I carry forward.

### 5.4 Valuation research

The earnings yield spread is a better construction than the cross-market price/earnings comparison I started with, but it does not survive out of sample.

The pattern is sharp: strongly positive in discovery ({n(float(pp.loc[('Valuation', '6M', 'discovery'), 'IC']))} at six months) and negative in the examined window ({n(float(pp.loc[('Valuation', '6M', 'examined'), 'IC']))}). I investigated whether this was driven by outliers, by the negative-policy-rate period, or by a single market.

Outliers are not the explanation: the median monthly information coefficient is {n(vs.loc['Median monthly IC','value'])}, and dropping the six worst months raises the result to {n(vs.loc['IC after dropping the six worst months','value'])} while dropping the six best leaves {n(vs.loc['IC after dropping the six best months','value'])}. The negative-policy-rate hypothesis — that a nominal two-year yield behaves differently when it is below zero, which it was for a large share of the panel between 2014 and 2022 — I tested directly and it does not hold: the information coefficient is {n(vs.iloc[4]['value'])} in months with no negative yield and {n(vs.iloc[5]['value'])} in months when some market had one.

The explanation is **one market**. The US contributes {n(vcc.loc['US','examined_contribution'])} of the {n(vcc.loc['Total = IC','examined_contribution'])} examined-window total. It stayed the most expensive market on this measure for most of the period and kept outperforming. Excluding the US, the examined-window information coefficient is {n(F['valuation_ex_us_examined'])}, which is positive and consistent with the economic hypothesis. That is a genuine finding but a narrower one than it sounds, because a five-market scorecard cannot avoid ranking the US.

A further diagnostic: the signal still ranks future *multiple expansion* out of sample. What fails is total return, because the earnings leg moves against the multiple leg. Cheap markets re-rated and simultaneously saw earnings disappoint.

I kept the pillar on the scorecard and labelled it diagnostic.

### 5.5 Technical research

I tested six price-path measures — six-month momentum, twelve-minus-one-month momentum, one-month and three-month returns, signed trend quality, and volatility-adjusted momentum — treating trend continuation and reversal as separate hypotheses. The direction of each measure was fixed on discovery-window evidence and frozen before the examined window was read, so no sign was flipped after seeing the answer.

Signed trend quality is the strongest of the six on raw numbers ({n(ta.loc[('Signed trend quality 12M','6M'),'IC_full'])} at six months, t = {ta.loc[('Signed trend quality 12M','6M'),'HAC_t_full']:.2f}). The one-month and three-month returns have information coefficients close to zero in either direction, so I found no support for short-horizon reversal at country level.

Two checks stop me promoting it. First, removing the Micro and Valuation content takes away {1-td.loc['6M','share_retained']:.0%} of its six-month information coefficient and {1-td.loc['3M','share_retained']:.0%} of its three-month one — a substantial fraction of the signal is the other two pillars restated. Second, and more decisive, **excluding the US leaves {n(td.loc['6M','ex_US_IC'])}** at six months. The same collapse appears across the other momentum variants: their ex-US six-month coefficients are {n(ta.loc[('6M momentum','6M'),'ex_US_IC'])}, {n(ta.loc[('12-1M momentum','6M'),'ex_US_IC'])} and {n(ta.loc[('Volatility-adjusted 12-1M momentum','6M'),'ex_US_IC'])}. The pillar is almost entirely a US effect.

A walk-forward re-selection among the six measures earns {n(twf['walk_forward_IC_6M'])} at six months, against {n(twf['IC_of_signed_trend_quality_on_same_months'])} for signed trend quality alone on the same months, so the choice among technical measures is not the problem. The problem is the dependence on one market and the arithmetic overlap with the other pillars.

This is a limitation of the supplied dataset rather than a verdict on technical signals in general. The dataset contains no index prices, so a technical pillar here cannot be independent of the pillars built from the same two inputs.

### 5.6 Machine-learning comparison

I fitted a Ridge regression on all four pillar scores, refitted monthly on an expanding window and using only months whose forward return was already realised, so that the model never sees its own future.

It did not improve on the simple equal-weight combination at either horizon ({n(float(mc.loc['Ridge challenger (4 pillars)', 'IC_examined_3M']))} at three months and {n(float(mc.loc['Ridge challenger (4 pillars)', 'IC_examined_6M']))} at six, against {n(float(mc.loc[REV, 'IC_examined_3M']))} and {n(float(mc.loc[REV, 'IC_examined_6M']))} for the equal-weight model), and it underperforms in the backtest as well. A plausible reason is that, with four correlated features, a short sample and a noisy target, the regression gives weight to the two pillars that do not generalise out of sample. I did not adopt it.

### 5.7 Original versus revised predictive model

| | Original: FCI + EPS revision 6M | Revised: FCI + EPS persistence 12M |
|---|---|---|
| IC, 3-month, examined | {n(float(mc.loc[ORIG, 'IC_examined_3M']))} | **{n(float(mc.loc[REV, 'IC_examined_3M']))}** |
| IC, 6-month, examined | {n(float(mc.loc[ORIG, 'IC_examined_6M']))} | **{n(float(mc.loc[REV, 'IC_examined_6M']))}** |
| 95% interval, 6-month | [{float(mc.loc[ORIG, 'IC_CI_low_6M']):+.3f}, {float(mc.loc[ORIG, 'IC_CI_high_6M']):+.3f}] | [{float(mc.loc[REV, 'IC_CI_low_6M']):+.3f}, {float(mc.loc[REV, 'IC_CI_high_6M']):+.3f}] |
| Long-short Sharpe, examined | {float(mc.loc[ORIG, 'long_short_sharpe_examined']):.2f} | **{float(mc.loc[REV, 'long_short_sharpe_examined']):.2f}** |
| Long-only information ratio, full | {float(mc.loc[ORIG, 'long_only_IR_full']):.2f} | **{float(mc.loc[REV, 'long_only_IR_full']):.2f}** |
| Turnover per year | {float(mc.loc[ORIG, 'turnover_pa']):.1f}x | {float(mc.loc[REV, 'turnover_pa']):.1f}x |

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
""" + "\n".join(
 f"| {p} | {n(float(pp.loc[(p,'3M','discovery'),'IC']))} → {n(float(pp.loc[(p,'3M','examined'),'IC']))} | "
 f"{n(float(pp.loc[(p,'6M','discovery'),'IC']))} → {n(float(pp.loc[(p,'6M','examined'),'IC']))} | "
 f"[{float(pp.loc[(p,'6M','examined'),'CI_low']):+.3f}, {float(pp.loc[(p,'6M','examined'),'CI_high']):+.3f}] | {cls.loc[p,'label']} |"
 for p in PILLARS) + f"""

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
| Diagnostic (four pillars) | {n(float(sic.loc[('Diagnostic (four pillars)','3M','discovery'),'IC']))} → {n(float(sic.loc[('Diagnostic (four pillars)','3M','examined'),'IC']))} | {n(float(sic.loc[('Diagnostic (four pillars)','6M','discovery'),'IC']))} → {n(float(sic.loc[('Diagnostic (four pillars)','6M','examined'),'IC']))} |
| Predictive (Macro + Micro) | {n(float(sic.loc[('Predictive (Macro + Micro)','3M','discovery'),'IC']))} → {n(float(sic.loc[('Predictive (Macro + Micro)','3M','examined'),'IC']))} | {n(float(sic.loc[('Predictive (Macro + Micro)','6M','discovery'),'IC']))} → {n(float(sic.loc[('Predictive (Macro + Micro)','6M','examined'),'IC']))} |

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
| Return % p.a. | {b('full',REV,'long_only',10,'return_pct_pa'):.1f} | {b('full',ORIG,'long_only',10,'return_pct_pa'):.1f} | {b('full','Equal-weight benchmark','long_only',0,'return_pct_pa'):.1f} | {b('full',REV,'long_short',10,'return_pct_pa'):.1f} |
| Volatility % p.a. | {b('full',REV,'long_only',10,'volatility_pct_pa'):.1f} | {b('full',ORIG,'long_only',10,'volatility_pct_pa'):.1f} | {b('full','Equal-weight benchmark','long_only',0,'volatility_pct_pa'):.1f} | {b('full',REV,'long_short',10,'volatility_pct_pa'):.1f} |
| Sharpe | {b('full',REV,'long_only',10,'sharpe'):.2f} | {b('full',ORIG,'long_only',10,'sharpe'):.2f} | {b('full','Equal-weight benchmark','long_only',0,'sharpe'):.2f} | {b('full',REV,'long_short',10,'sharpe'):.2f} |
| Maximum drawdown % | {b('full',REV,'long_only',10,'max_drawdown_pct'):.1f} | {b('full',ORIG,'long_only',10,'max_drawdown_pct'):.1f} | {b('full','Equal-weight benchmark','long_only',0,'max_drawdown_pct'):.1f} | {b('full',REV,'long_short',10,'max_drawdown_pct'):.1f} |
| Turnover per year | {b('full',REV,'long_only',10,'turnover_pa'):.1f}x | {b('full',ORIG,'long_only',10,'turnover_pa'):.1f}x | — | {b('full',REV,'long_short',10,'turnover_pa'):.1f}x |
| Information ratio vs benchmark | {b('full',REV,'long_only',10,'information_ratio'):.2f} | {b('full',ORIG,'long_only',10,'information_ratio'):.2f} | — | — |
| **Examined-window Sharpe** | {b('examined',REV,'long_only',10,'sharpe'):.2f} | {b('examined',ORIG,'long_only',10,'sharpe'):.2f} | {b('examined','Equal-weight benchmark','long_only',0,'sharpe'):.2f} | {b('examined',REV,'long_short',10,'sharpe'):.2f} |

Backtest returns run from {F['backtest_window']['full']}.

### 8.3 How the revised Micro signal changes the result

The clearest effect is in the long-short book over the examined window, where the Sharpe ratio rises from {float(mc.loc[ORIG,'long_short_sharpe_examined']):.2f} to {float(mc.loc[REV,'long_short_sharpe_examined']):.2f}. In the long-only book the information ratio against the benchmark rises from {float(mc.loc[ORIG,'long_only_IR_full']):.2f} to {float(mc.loc[REV,'long_only_IR_full']):.2f}. The revised signal also trades less than the original, at {float(mc.loc[REV,'turnover_pa']):.1f} times a year against {float(mc.loc[ORIG,'turnover_pa']):.1f}, which is consistent with a measure built on a twelve-month count rather than a six-month change.

### 8.4 Model comparison in the backtest

| Model | Long-only Sharpe | Long-only IR | Long-short Sharpe, full | Long-short Sharpe, examined | Turnover |
|---|---|---|---|---|---|
""" + "\n".join(
 f"| {m} | {float(mc.loc[m,'long_only_sharpe_full']):.2f} | {float(mc.loc[m,'long_only_IR_full']):.2f} | "
 f"{float(mc.loc[m,'long_short_sharpe_full']):.2f} | {float(mc.loc[m,'long_short_sharpe_examined']):.2f} | {float(mc.loc[m,'turnover_pa']):.1f}x |"
 for m in mc.index) + f"""

### 8.5 Transaction-cost sensitivity

The revised long-short book returns a Sharpe ratio of {F['cost_sensitivity']['0']:.2f} gross, {F['cost_sensitivity']['5']:.2f} at 5 basis points, {F['cost_sensitivity']['10']:.2f} at 10 and {F['cost_sensitivity']['20']:.2f} at 20. Costs are not the binding constraint on this strategy at any plausible level for developed-market index exposure.

---

## 9. Investment view

**As of {F['as_of']}.** This is the latest ranking the supplied dataset supports. The panel ends on 30 April 2026 because that is the last month in which all five markets report. It is not a reading of current market conditions, and I do not present it as one.

| Rank | Market | Predictive score | Four-pillar score | Classification | Principal reason |
|---|---|---|---|---|---|
""" + "\n".join(
 f"| {int(cur.loc[m,'Predictive rank'])} | {m} | {float(cur.loc[m,'Predictive score']):+.2f} | {float(cur.loc[m,'Diagnostic score']):+.2f} | "
 f"{cur.loc[m,'Predictive call']} | {reason[m]} |" for m in MK) + f"""

The two views — the four-pillar diagnostic scorecard and the predictive score — agree on **all five** classifications this month. That is not always the case, and when they diverge the predictive view is the one carrying out-of-sample evidence while the four-pillar view is the complete framework.

**Conviction is highest on the United States and low on the ordering of the rest.** The US leads on both pillars that carry evidence, and it has held first place in {F['rank_stability']['us_first_in_last8']} of the last eight months. The Eurozone is separated from third place by {F['gap_rank2_rank3']:.2f} on the predictive score, but the bottom three are tightly bunched — Japan, Switzerland and the UK sit within about {float(cur['Predictive score'].iloc[2] - cur['Predictive score'].iloc[4]):.2f} of one another — so the ordering among them carries little information. The UK's underweight is the best supported of the three because its financial-conditions reading is genuinely the weakest in the panel; Switzerland's rests on a narrower margin over Japan.

Rankings are also not stable month to month. In the final month the UK moved from rank {F['rank_stability']['uk_rank_prior_month']} to rank {F['rank_stability']['uk_rank_now']}, and the Eurozone from rank {F['rank_stability']['eurozone_rank_prior_month']} to rank {F['rank_stability']['eurozone_rank_now']}. The six-month tranche construction in the backtest exists precisely because single-month rankings are noisy, and a position taken from one month's ranking should be sized accordingly.

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

The most useful thing I learned was methodological rather than economic: **how a signal is measured can matter more than what it measures.** The Micro pillar did not change its economic content between the original and revised specifications — both are statements about forward earnings revisions. Changing from the size of revisions to their frequency raised the six-month examined information coefficient from {n(F['micro_old_6M'])} to {n(F['micro_new_6M'])}. The second lesson was how easily a comparison can mislead when two constructions are evaluated on different samples, and how often an apparently strong result turns out to rest on a single market.

The hypotheses that remain provisional are both of the ones I retained. The financial-conditions impulse and earnings-revision persistence are supported by the evidence available, they survive the robustness tests I could run, and neither is proven.

---

## References

[1] Post-earnings-announcement drift: delayed price response or risk premium? *Journal of Accounting Research*, 27 (Supplement), 1989, 1–36.

[2] Momentum strategies. *Journal of Finance*, 51(5), 1996, 1681–1713.

[3] Value and momentum everywhere. *Journal of Finance*, 68(3), 2013, 929–985.

[4] A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 1987, 703–708.

[5] The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1994, 1303–1313.

[6] *Active Portfolio Management: A Quantitative Approach for Producing Superior Returns and Controlling Risk*, 2nd edition. McGraw-Hill, 2000.
"""
(ROOT / 'METHODOLOGY_AND_RESEARCH_PROCESS.md').write_text(doc, encoding='utf8')
print('Methodology document written:', len(doc.split()), 'words')
