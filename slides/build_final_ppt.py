"""Build the 5-slide CRISIL deck from output/v14 only.

Every number shown on a slide is read from a v14 CSV through `val()`, which logs
(slide, displayed text, file, row filter, column) to output/v14/slide_number_registry.csv.
`check_ppt_reconciliation.py` re-reads every entry independently and scans the deck for any
number that is not in the registry.

Run from the repo root:  python3 slides/build_final_ppt.py
"""
import json
from pathlib import Path
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / 'output' / 'v14'
CHARTS = V / 'charts'
OUTFILE = ROOT / 'slides' / 'Markets_Scorecard_FINAL.pptx'
NAVY, GREY, RED, GREEN, AMBER, LIGHT = (RGBColor(0x1F, 0x4E, 0x79), RGBColor(0x59, 0x59, 0x59), RGBColor(0xC0, 0x50, 0x4D),
                                         RGBColor(0x2E, 0x8B, 0x57), RGBColor(0xB8, 0x86, 0x0B), RGBColor(0xEE, 0xF2, 0xF7))
COUNTRIES = ['US', 'Eurozone', 'UK', 'Switzerland', 'Japan']
PILLARS = ['Macro', 'Micro', 'Valuation', 'Technical']

CSV = {}
def load(name, **kw):
    if name not in CSV:
        CSV[name] = pd.read_csv(V / name, **kw)
    return CSV[name]
REG = []
SLIDE = [0]
def val(file, filt, column, fmt):
    """Read one cell from a v14 CSV, format it, and log it for reconciliation."""
    df = load(file)
    m = pd.Series(True, index=df.index)
    for k, v in filt.items():
        m &= df[k].astype(str) == str(v)
    rows = df[m]
    assert len(rows) == 1, (file, filt, len(rows))
    x = rows.iloc[0][column]
    s = fmt.format(x)
    REG.append({'slide': SLIDE[0], 'displayed': s, 'file': file, 'filter': json.dumps(filt), 'column': column, 'format': fmt})
    return s

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def textbox(slide, x, y, w, h, paras, size=12, color=GREY, bold_first=False, fill=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    if fill is not None:
        tb.fill.solid(); tb.fill.fore_color.rgb = fill
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        runs = p if isinstance(p, list) else [(p, {})]
        for txt, st in runs:
            r = para.add_run(); r.text = txt
            r.font.size = Pt(st.get('size', size)); r.font.bold = st.get('bold', bold_first and i == 0)
            r.font.color.rgb = st.get('color', color)
        para.space_after = Pt(st.get('after', 4) if runs else 4)
    return tb

def header(slide, n, title, message):
    bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12)); bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    textbox(slide, 0.45, 0.25, 12.4, 0.5, [[(f'{n}. {title}', {'size': 13, 'color': NAVY, 'bold': True})]])
    textbox(slide, 0.45, 0.62, 12.4, 0.7, [[(message, {'size': 20, 'color': RGBColor(0x1A, 0x1A, 0x1A), 'bold': True})]])

def footer(slide, text):
    textbox(slide, 0.45, 7.05, 12.4, 0.35, [[(text, {'size': 8.5, 'color': GREY})]])

def table(slide, x, y, w, h, data, col_w=None, size=10, header_fill=NAVY, first_col_bold=True, color_map=None):
    rows, cols = len(data), len(data[0])
    t = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h)).table
    if col_w:
        for j, cw in enumerate(col_w):
            t.columns[j].width = Inches(cw)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            cell = t.cell(i, j); cell.text = str(v); cell.margin_left = cell.margin_right = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            f = p.runs[0].font; f.size = Pt(size)
            if i == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_fill; f.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); f.bold = True
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 else LIGHT
                f.color.rgb = RGBColor(0x26, 0x26, 0x26); f.bold = first_col_bold and j == 0
                if color_map and (i, j) in color_map:
                    f.color.rgb = color_map[(i, j)]; f.bold = True
    return t

FOOT = 'Source: Markets_Scorecard_v14_FINAL.ipynb; supplied Bloomberg workbooks; latest common data date 30-Apr-2026. USD price returns (no dividends).'
pp = 'predictive_power.csv'; bs = 'backtest_summary.csv'; cs = 'current_scorecard.csv'; cl = 'signal_classification.csv'
load(cs).rename(columns={load(cs).columns[0]: 'country'}, inplace=True)
load(cl).rename(columns={load(cl).columns[0]: 'pillar'}, inplace=True)

# ---------------------------------------------------------------- slide 1: methodology
SLIDE[0] = 1; s = prs.slides.add_slide(BLANK)
header(s, 1, 'Methodology', 'One signal per pillar, z-scored across five markets, combined with equal weights')
textbox(s, 0.45, 1.45, 5.3, 5.4, [
    [('Objective', {'bold': True, 'color': NAVY, 'size': 13})],
    'Rank US, Eurozone, UK, Switzerland and Japan by expected relative USD equity performance over the next 3–6 months.',
    [('Data', {'bold': True, 'color': NAVY, 'size': 13})],
    'Supplied Bloomberg workbooks, monthly, Dec-2005 to Apr-2026. Index level = forward P/E × forward EPS (an identity; US matches published S&P 500 returns).',
    [('Process', {'bold': True, 'color': NAVY, 'size': 13})],
    '① Build one indicator per pillar  ② z-score across the 5 markets each month  ③ aggregate = equal-weight average (25% each)  ④ rank 1–5  ⑤ test each pillar\'s predictive power  ⑥ backtest the ranking.',
    [('Testing', {'bold': True, 'color': NAVY, 'size': 13})],
    'Monthly rank IC vs next 3M and 6M relative USD returns. Discovery to Dec-2016; validation from Jul-2017 after a 6-month embargo. Bootstrap CIs, HAC t, block-permutation p.',
    [('Backtest', {'bold': True, 'color': NAVY, 'size': 13})],
    'Long-only top-2 vs equal-weight benchmark; long-short top-2 / bottom-2. Monthly signal, 6-month overlapping tranches, costs 0–20 bps one-way.',
], size=11)
sig = load('signal_definitions.csv')
rows = [['Pillar', 'Indicator', 'Investment rationale', 'Attractive when']]
short = {'Macro': 'Easier financing conditions support earnings and risk appetite with a lag',
         'Micro': 'Analyst revisions persist (anchoring); prices under-react to upgrades',
         'Valuation': 'Relative cheapness vs own history should mean-revert',
         'Technical': 'Low-volatility anomaly; calm markets carry lower risk-premium shocks'}
when = {'Macro': 'FCI eased most over 6M', 'Micro': 'Forward EPS upgraded most over 6M', 'Valuation': 'P/E vs peers cheapest vs own history', 'Technical': 'Lowest 12M realised vol'}
for p in PILLARS:
    rows.append([p, sig.loc[sig.pillar == p, 'indicator'].iloc[0], short[p], when[p]])
table(s, 6.0, 1.5, 6.9, 3.2, rows, col_w=[1.05, 1.55, 2.75, 1.55], size=10)
textbox(s, 6.0, 4.95, 6.9, 1.9, [
    [('Key limitations', {'bold': True, 'color': RED, 'size': 12})],
    '• Data end 30-Apr-2026: rankings are as of that date, not current. The proprietary inputs (BEst, GS/Bloomberg FCI) have no comparable free source to update them.',
    '• Price return only (no dividends). Switzerland uses the euro-area FCI and credit series.',
    '• The indicators were chosen during extensive research; no result survives a full multiple-testing adjustment.',
], size=10)
footer(s, FOOT)

# ---------------------------------------------------------------- slide 2: signal selection & predictive power
SLIDE[0] = 2; s = prs.slides.add_slide(BLANK)
header(s, 2, 'Signal selection and predictive power', 'Macro and Micro stay positive out of sample; Valuation and Technical reverse')
s.shapes.add_picture(str(CHARTS / 'ic_by_pillar.png'), Inches(0.45), Inches(1.45), width=Inches(7.6))
rows = [['Pillar', 'Val IC 3M [95% CI]', 'Val IC 6M [95% CI]', 'Perm p 3M / 6M', 'Status']]
cmap = {}
for i, p in enumerate(PILLARS, start=1):
    f3 = {'pillar': p, 'horizon': '3M', 'window': 'validation'}; f6 = {'pillar': p, 'horizon': '6M', 'window': 'validation'}
    stt = val(cl, {'pillar': p}, 'classification', '{}')
    rows.append([p, f'{val(pp, f3, "IC", "{:+.3f}")} [{val(pp, f3, "CI 2.5%", "{:+.2f}")}, {val(pp, f3, "CI 97.5%", "{:+.2f}")}]',
                 f'{val(pp, f6, "IC", "{:+.3f}")} [{val(pp, f6, "CI 2.5%", "{:+.2f}")}, {val(pp, f6, "CI 97.5%", "{:+.2f}")}]',
                 f'{val(pp, f3, "perm p", "{:.3f}")} / {val(pp, f6, "perm p", "{:.3f}")}', stt])
    cmap[(i, 4)] = AMBER if stt == 'PROVISIONAL' else RED
table(s, 8.25, 1.5, 4.65, 2.3, rows, col_w=[0.8, 1.15, 1.15, 0.7, 0.85], size=8.5, color_map=cmap)
d3 = lambda p, w, h: val(pp, {'pillar': p, 'horizon': h, 'window': w}, 'IC', '{:+.2f}')
textbox(s, 8.25, 4.0, 4.65, 2.9, [
    [('Reading the evidence', {'bold': True, 'color': NAVY, 'size': 12})],
    f'• Macro (FCI): positive in both windows (6M: {d3("Macro", "discovery", "6M")} discovery, {d3("Macro", "validation", "6M")} validation). Strongest pillar.',
    f'• Micro (EPS): positive at 3M ({d3("Micro", "validation", "3M")}), weak at 6M ({d3("Micro", "validation", "6M")}). Partly a persistent US/Japan tilt.',
    f'• Valuation: {d3("Valuation", "discovery", "3M")} → {d3("Valuation", "validation", "3M")} at 3M. Mostly the US: expensive throughout, yet the best performer.',
    f'• Technical: {d3("Technical", "discovery", "3M")} → {d3("Technical", "validation", "3M")} at 3M. No stable mechanism at country level.',
    [('Caveat: no pillar has a validation CI entirely above zero (Valuation 3M lies almost entirely below it), and the signals were selected from many tested alternatives. No pillar is statistically significant after multiple testing.', {'size': 9.5, 'color': RED})],
], size=10)
textbox(s, 0.45, 4.25, 7.6, 2.7, [
    [('How to read', {'bold': True, 'color': NAVY, 'size': 11})],
    'IC = monthly Spearman correlation between pillar scores and the next 3M / 6M USD return relative to the 5-market average, averaged over months (+1 = perfect ranking). '
    'Error bars: 95% moving-block bootstrap. Perm p: one-sided, country labels shuffled in horizon-length blocks.',
    'Classification rule (fixed in advance): PROVISIONAL = validation IC > 0 at both horizons and p < 0.05 at one or more; REJECTED = validation IC ≤ 0 at either horizon. '
    'RETAIN would also require CIs excluding zero — no pillar meets it.',
], size=9.5)
footer(s, FOOT + ' Discovery: signal months to Dec-2016; validation: Jul-2017 onward.')

# ---------------------------------------------------------------- slide 3: scorecard construction
SLIDE[0] = 3; s = prs.slides.add_slide(BLANK)
header(s, 3, 'Scorecard construction', 'Equal-weight aggregate of four pillar z-scores; weak pillars are kept but flagged')
aic = 'aggregate_score_ic.csv'
ag = lambda h, w, c='IC', f='{:+.2f}': val(aic, {'score': 'Aggregate (4-pillar)', 'horizon': h, 'window': w}, c, f)
textbox(s, 0.45, 1.45, 6.0, 5.5, [
    [('Pillar score', {'bold': True, 'color': NAVY, 'size': 12})],
    'z = (indicator − 5-market mean) ÷ 5-market sd, each month. Higher = more attractive for every pillar.',
    [('Aggregate country score', {'bold': True, 'color': NAVY, 'size': 12})],
    'Aggregate = ¼ Macro + ¼ Micro + ¼ Valuation + ¼ Technical. Contribution of a pillar = ¼ × its z.',
    'Equal weights because the brief requires four pillars and no pillar has validated evidence. Weights fitted to past ICs would be in-sample optimisation.',
    [('Ranking', {'bold': True, 'color': NAVY, 'size': 12})],
    'Rank 1–5 by aggregate. Calls: ranks 1–2 overweight, 3 neutral, 4–5 underweight.',
    [('Companion model (shown separately)', {'bold': True, 'color': NAVY, 'size': 12})],
    'FCI-only ranking (Macro z alone): the one pillar with consistent out-of-sample evidence. It does not replace the scorecard.',
    [('Predictive power of the aggregate', {'bold': True, 'color': NAVY, 'size': 12})],
    f'IC 3M: discovery {ag("3M", "discovery")}, validation {ag("3M", "validation")}. IC 6M: discovery {ag("6M", "discovery")}, validation {ag("6M", "validation")}. '
    'The two weak pillars that helped in discovery reversed after 2017 and dilute Macro and Micro.',
], size=10.5)
s.shapes.add_picture(str(CHARTS / 'pillar_heatmap.png'), Inches(6.75), Inches(1.5), width=Inches(6.15))
textbox(s, 6.75, 5.45, 6.15, 1.4, [
    'Scores as of 30-Apr-2026. Columns flagged "weak" are rejected predictors (Slide 2). They are retained because the brief specifies a four-pillar scorecard.',
    'Full monthly history (all pillar scores, aggregate, rank, call and the realised next 3M / 6M return) is in scorecard_history.csv.'], size=9.5)
footer(s, FOOT)

# ---------------------------------------------------------------- slide 4: backtest
SLIDE[0] = 4; s = prs.slides.add_slide(BLANK)
header(s, 4, 'Backtest results', 'Long-only modestly beats the benchmark; the long-short edge disappears after 2017')
s.shapes.add_picture(str(CHARTS / 'cumulative_vs_benchmark.png'), Inches(0.45), Inches(1.4), width=Inches(5.9))
s.shapes.add_picture(str(CHARTS / 'drawdown.png'), Inches(0.45), Inches(4.45), width=Inches(5.9))
b = lambda w, st, bk, c, col, f: val(bs, {'window': w, 'strategy': st, 'book': bk, 'cost bps': c}, col, f)
SC, CO, EWB = 'Scorecard (4-pillar)', 'Companion (FCI-only)', 'Equal-weight benchmark'
LO, LS = 'long-only top-2', 'long-short top2/bottom2'
rows = [['Full period, net 10 bps', 'Scorecard long-only', 'EW benchmark', 'Scorecard long-short', 'FCI-only long-short']]
for lab, col, f in (('Return % p.a.', 'Ann. return %', '{:.1f}'), ('Volatility % p.a.', 'Ann. vol %', '{:.1f}'), ('Sharpe ratio', 'Sharpe', '{:.2f}'),
                    ('Max drawdown %', 'Max drawdown %', '{:.1f}'), ('Turnover p.a. (x)', 'Turnover p.a. (x)', '{:.1f}')):
    rows.append([lab, b('full', SC, LO, 10, col, f), b('full', EWB, 'long-only', 0, col, f) if col != 'Turnover p.a. (x)' else '–',
                 b('full', SC, LS, 10, col, f), b('full', CO, LS, 10, col, f)])
rows.append(['Validation Sharpe', b('validation', SC, LO, 10, 'Sharpe', '{:.2f}'), b('validation', EWB, 'long-only', 0, 'Sharpe', '{:.2f}'),
             b('validation', SC, LS, 10, 'Sharpe', '{:.2f}'), b('validation', CO, LS, 10, 'Sharpe', '{:.2f}')])
rows.append(['Info ratio vs EW (LO)', b('full', SC, LO, 10, 'Information ratio', '{:.2f}'), '–', '–', '–'])
table(s, 7.2, 1.45, 5.7, 3.1, rows, col_w=[1.6, 1.05, 1.0, 1.05, 1.0], size=9)
att = 'backtest_pillar_attribution.csv'
pa = lambda name, w: val(att, {'pillar alone': name, 'window': w}, 'Sharpe', '{:+.2f}')
textbox(s, 7.2, 4.7, 5.7, 2.3, [
    [('Costs:', {'bold': True, 'color': NAVY}), (f' long-short Sharpe (full) {b("full", SC, LS, 0, "Sharpe", "{:.2f}")} / {b("full", SC, LS, 5, "Sharpe", "{:.2f}")} / '
                                              f'{b("full", SC, LS, 10, "Sharpe", "{:.2f}")} / {b("full", SC, LS, 20, "Sharpe", "{:.2f}")} at 0 / 5 / 10 / 20 bps. Costs are not the problem.', {})],
    [('Why the composite fails after 2017:', {'bold': True, 'color': RED}), (' run alone with the same rules, validation long-short Sharpe is '
        f'Macro {pa("Macro (FCI 6M easing)", "validation")}, Micro {pa("Micro (EPS revisions 6M)", "validation")}, Valuation {pa("Valuation (P/E relative to peers)", "validation")}, '
        f'Technical {pa("Technical (Low realised volatility 12M)", "validation")}. The two rejected pillars cancel the two that work.', {})],
    [('Not optimised:', {'bold': True, 'color': NAVY}), (' rules were fixed in advance. Equal-weight benchmark carried cost-free. Long-short Sharpe uses rf = 0 (self-financing).', {})],
], size=9.5)
footer(s, FOOT + ' Backtest returns Dec-2010 to Apr-2026; validation Aug-2017 onward.')

# ---------------------------------------------------------------- slide 5: current ranking & recommendation
SLIDE[0] = 5; s = prs.slides.add_slide(BLANK)
header(s, 5, 'Current ranking and investment recommendation', 'As of 30-Apr-2026: overweight US and UK, underweight Switzerland and Japan — low conviction')
s.shapes.add_picture(str(CHARTS / 'pillar_contributions.png'), Inches(0.45), Inches(1.4), width=Inches(6.3))
cur = load(cs).sort_values('Rank')
rows = [['Rank', 'Market', 'Aggregate', 'Call', 'FCI-only rank']]
cmap = {}
for i, c in enumerate(cur['country'], start=1):
    call = val(cs, {'country': c}, 'Scorecard call', '{}')
    rows.append([val(cs, {'country': c}, 'Rank', '{:.0f}'), c, val(cs, {'country': c}, 'Aggregate score', '{:+.2f}'), call, val(cs, {'country': c}, 'Companion FCI-only rank', '{:.0f}')])
    cmap[(i, 3)] = GREEN if call == 'OVERWEIGHT' else (RED if call == 'UNDERWEIGHT' else GREY)
table(s, 7.0, 1.45, 5.9, 2.1, rows, col_w=[0.7, 1.5, 1.2, 1.4, 1.1], size=10, first_col_bold=False, color_map=cmap)
z = lambda c, p: val(cs, {'country': c}, f'{p} score', '{:+.1f}')
r = lambda c, col, f: val(cs, {'country': c}, col, f)
textbox(s, 7.0, 3.7, 5.9, 3.3, [
    [('Recommendation (scorecard)', {'bold': True, 'color': NAVY, 'size': 12})],
    f'• OVERWEIGHT US: strongest FCI easing ({z("US", "Macro")}) and EPS upgrades ({r("US", "EPS revision 6M %", "{:.1f}")}% over 6M), despite the richest P/E ({r("US", "Forward P/E", "{:.1f}")}x).',
    f'• OVERWEIGHT UK: cheapest vs peers ({z("UK", "Valuation")}) and low volatility ({z("UK", "Technical")}), but tightest FCI ({z("UK", "Macro")}). Its case rests on the two weak pillars.',
    f'• NEUTRAL Eurozone. UNDERWEIGHT Switzerland (weakest EPS revisions, {r("Switzerland", "EPS revision 6M %", "{:+.1f}")}%) and Japan (highest 12M volatility, {r("Japan", "12M realised vol % (ann.)", "{:.1f}")}%).',
    [('Conviction: LOW', {'bold': True, 'color': RED, 'size': 11})],
    f'• US and UK are near-tied ({r("US", "Aggregate score", "{:+.2f}")} vs {r("UK", "Aggregate score", "{:+.2f}")}), and the US rose from #{val("scorecard_history.csv", {"month": "2026-03", "country": "US"}, "rank", "{:.0f}")} in March. '
    f'The companion FCI-only model, the only pillar that held up after 2017, ranks the UK last and Switzerland #{r("Switzerland", "Companion FCI-only rank", "{:.0f}")}.',
    '• Data are as of 30-Apr-2026. Refreshed Bloomberg exports (same tickers) regenerate this ranking automatically.',
], size=10)
footer(s, FOOT)

prs.save(OUTFILE)
pd.DataFrame(REG).to_csv(V / 'slide_number_registry.csv', index=False)
print(f'saved {OUTFILE.relative_to(ROOT)} with {len(prs.slides)} slides; {len(REG)} numbers registered')
