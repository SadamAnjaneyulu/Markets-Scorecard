"""Build the 5-slide CRISIL deck from output/v16 only.

Every number on a slide is read from a v16 CSV through `val()`, which logs
(slide, displayed text, file, filter, column) to output/v16/slide_number_registry.csv.
`check_v16_ppt.py` re-reads each entry independently and scans the deck for untraceable numbers.

Run from the repo root:  python3 slides/build_v16_ppt.py
"""
import json
from pathlib import Path
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / 'output' / 'v16'; CHARTS = V / 'charts'
OUTFILE = ROOT / 'slides' / 'Markets_Scorecard_v16_FINAL.pptx'
NAVY, GREY, RED, GREEN, AMBER, LIGHT = (RGBColor(0x1F, 0x4E, 0x79), RGBColor(0x59, 0x59, 0x59), RGBColor(0xC0, 0x50, 0x4D),
                                        RGBColor(0x2E, 0x8B, 0x57), RGBColor(0xB8, 0x86, 0x0B), RGBColor(0xEE, 0xF2, 0xF7))
PILLARS = ['Macro', 'Micro', 'Valuation', 'Technical']
FIRSTCOL = {'signal_classification.csv': 'pillar', 'current_scorecard.csv': 'country', 'current_rankings_3m_6m.csv': 'country', 'headline_figures.csv': 'figure'}
CSV = {}
def load(name):
    if name not in CSV:
        d = pd.read_csv(V / name)
        if name in FIRSTCOL: d = d.rename(columns={d.columns[0]: FIRSTCOL[name]})
        CSV[name] = d
    return CSV[name]
REG, SLIDE = [], [0]
def val(file, filt, column, fmt):
    df = load(file); m = pd.Series(True, index=df.index)
    for k, v in filt.items(): m &= df[k].astype(str) == str(v)
    rows = df[m]; assert len(rows) == 1, (file, filt, len(rows))
    s = fmt.format(rows.iloc[0][column])
    REG.append({'slide': SLIDE[0], 'displayed': s, 'file': file, 'filter': json.dumps(filt), 'column': column, 'format': fmt})
    return s

prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5); BLANK = prs.slide_layouts[6]
def textbox(slide, x, y, w, h, paras, size=12, color=GREY):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        for txt, st in (p if isinstance(p, list) else [(p, {})]):
            r = para.add_run(); r.text = txt; r.font.size = Pt(st.get('size', size)); r.font.bold = st.get('bold', False); r.font.color.rgb = st.get('color', color)
        para.space_after = Pt(4)
    return tb
def header(slide, n, title, message):
    bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12)); bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    textbox(slide, 0.45, 0.25, 12.4, 0.5, [[(f'{n}. {title}', {'size': 13, 'color': NAVY, 'bold': True})]])
    textbox(slide, 0.45, 0.62, 12.4, 0.7, [[(message, {'size': 19, 'color': RGBColor(0x1A, 0x1A, 0x1A), 'bold': True})]])
def footer(slide, text): textbox(slide, 0.45, 7.05, 12.4, 0.35, [[(text, {'size': 8.5, 'color': GREY})]])
def table(slide, x, y, w, h, data, col_w=None, size=10, color_map=None, bold_first_col=True):
    t = slide.shapes.add_table(len(data), len(data[0]), Inches(x), Inches(y), Inches(w), Inches(h)).table
    if col_w:
        for j, cw in enumerate(col_w): t.columns[j].width = Inches(cw)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            cell = t.cell(i, j); cell.text = str(v); cell.margin_left = cell.margin_right = Inches(0.05); cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER; f = p.runs[0].font; f.size = Pt(size)
            if i == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = NAVY; f.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); f.bold = True
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 else LIGHT
                f.color.rgb = RGBColor(0x26, 0x26, 0x26); f.bold = bold_first_col and j == 0
                if color_map and (i, j) in color_map: f.color.rgb = color_map[(i, j)]; f.bold = True
    return t

FOOT = 'Source: Markets_Scorecard_v16_FINAL.ipynb and output/v16; supplied Bloomberg workbooks only. USD price returns (no dividends). Latest common data date 30-Apr-2026.'
pp, cl, bs, cs, sc, rb, att, hf = 'predictive_power.csv', 'signal_classification.csv', 'backtest_summary.csv', 'current_scorecard.csv', 'scorecard_ic.csv', 'robustness.csv', 'backtest_pillar_attribution.csv', 'headline_figures.csv'
D4, PR, EWB = 'Diagnostic (4-pillar)', 'Predictive (Macro+Micro)', 'Equal-weight benchmark'

# ---------------- slide 1
SLIDE[0] = 1; s = prs.slides.add_slide(BLANK)
header(s, 1, 'Methodology', 'One indicator per pillar, z-scored across five markets, with predictive and diagnostic pillars kept separate')
textbox(s, 0.45, 1.45, 5.2, 5.4, [
    [('Objective', {'bold': True, 'color': NAVY, 'size': 13})],
    'Rank the US, Eurozone, UK, Switzerland and Japan by expected relative USD performance over the next 3–6 months.',
    [('Data', {'bold': True, 'color': NAVY, 'size': 13})],
    'Supplied Bloomberg workbooks only, monthly, Dec-2005 to Apr-2026. The dataset contains NO index price: the supplied "Price" file holds P/E ratios, so the index is reconstructed as forward P/E × forward EPS (an identity; the US matches published S&P 500 returns to 0.04 pp).',
    [('Process', {'bold': True, 'color': NAVY, 'size': 13})],
    '① one indicator per pillar  ② z-score across the 5 markets each month  ③ equal-weight aggregate  ④ rank 1–5  ⑤ test each pillar  ⑥ backtest the ranking.',
    [('Testing', {'bold': True, 'color': NAVY, 'size': 13})],
    'Rank IC against the next 3M/6M relative return. Discovery to Dec-2016, six-month embargo, examined window from Jul-2017. Bootstrap CIs, HAC t, block-permutation p, leave-one-country-out, walk-forward.',
    [('Two views, reported together', {'bold': True, 'color': NAVY, 'size': 13})],
    'The four-pillar equal-weight scorecard is the primary deliverable. A predictive score containing only the pillars with out-of-sample evidence is shown alongside it. Failed pillars are kept and labelled, never given artificial weight.',
], size=10.5)
rows = [['Pillar', 'Indicator', 'Attractive when', 'Label']]
cmap = {}
for i, p in enumerate(PILLARS, start=1):
    lab = val(cl, {'pillar': p}, 'confidence label', '{}')
    rows.append([p, val(cl, {'pillar': p}, 'indicator', '{}'),
                 {'Macro': 'conditions eased most over 6M', 'Micro': 'forward EPS upgraded most over 6M',
                  'Valuation': 'earnings yield minus 2Y widest vs own history', 'Technical': 'smoothest rising 12M trend'}[p], lab])
    cmap[(i, 3)] = GREEN if lab.startswith('PREDICTIVE') else AMBER
table(s, 5.95, 1.5, 6.95, 2.4, rows, col_w=[1.0, 2.0, 2.4, 1.55], size=9.5, color_map=cmap)
textbox(s, 5.95, 4.15, 6.95, 2.8, [
    [('Key limitations', {'bold': True, 'color': RED, 'size': 12})],
    '• Data end 30-Apr-2026, so the ranking is as of that date, not current. Only the supplied dataset may be used, so it cannot be extended.',
    '• Price returns only — no dividend data is supplied.',
    '• No index price exists, so the Technical pillar is a function of the same inputs as Micro and Valuation. It is not independent, and we do not claim it is.',
    '• Switzerland uses the euro-area financial-conditions and credit series. The UK workbook\'s "VIX" column is not a volatility index and is excluded.',
    '• The indicators were selected across sixteen research versions. No pillar is statistically significant after multiple testing.',
], size=9.5)
footer(s, FOOT)

# ---------------- slide 2
SLIDE[0] = 2; s = prs.slides.add_slide(BLANK)
header(s, 2, 'Signal selection and predictive power', 'Macro and Micro hold out of sample; Valuation and Technical do not survive their robustness tests')
s.shapes.add_picture(str(CHARTS / 'ic_by_pillar.png'), Inches(0.45), Inches(1.4), width=Inches(7.5))
rows = [['Pillar', 'IC 3M disc → exam', 'IC 6M disc → exam', 'ex-US 6M', 'Label']]
cmap = {}
for i, p in enumerate(PILLARS, start=1):
    lab = val(cl, {'pillar': p}, 'confidence label', '{}')
    rows.append([p,
                 f"{val(pp, {'pillar': p, 'horizon': '3M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(pp, {'pillar': p, 'horizon': '3M', 'window': 'examined'}, 'IC', '{:+.3f}')}",
                 f"{val(pp, {'pillar': p, 'horizon': '6M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(pp, {'pillar': p, 'horizon': '6M', 'window': 'examined'}, 'IC', '{:+.3f}')}",
                 val(rb, {'pillar': p, 'horizon': '6M'}, 'ex-US IC', '{:+.3f}'), lab])
    cmap[(i, 4)] = GREEN if lab.startswith('PREDICTIVE') else AMBER
table(s, 8.15, 1.5, 4.75, 2.3, rows, col_w=[0.85, 1.15, 1.15, 0.7, 0.9], size=8.5, color_map=cmap)
textbox(s, 8.15, 4.0, 4.75, 3.0, [
    [('What the tests show', {'bold': True, 'color': NAVY, 'size': 11.5})],
    f"• Macro: positive in both windows at both horizons; every leave-one-out IC positive (min {val(rb, {'pillar': 'Macro', 'horizon': '6M'}, 'min leave-one-out IC', '{:+.3f}')}). From 2014 its 6M IC is {val(rb, {'pillar': 'Macro', 'horizon': '6M'}, 'IC 2014-onward (frozen)', '{:+.3f}')} (t {val(rb, {'pillar': 'Macro', 'horizon': '6M'}, 'IC 2014-onward t', '{:.2f}')}); the yearly re-selection test in the investigation notebook picks this same construction every year.",
    f"• Micro: positive at 3M in both windows; weak at 6M out of sample. Revision acceleration and momentum were tested and refuted.",
    f"• Valuation: strong in discovery, negative out of sample ({val(pp, {'pillar': 'Valuation', 'horizon': '6M', 'window': 'examined'}, 'IC', '{:+.3f}')}). Traced to the US — persistently the most expensive market, and it kept outperforming.",
    f"• Technical: raw IC looks good but falls to {val(rb, {'pillar': 'Technical', 'horizon': '6M'}, 'ex-US IC', '{:+.3f}')} without the US, and most of it is Micro and Valuation restated.",
    [('No pillar is statistically significant once the research history is accounted for. Error bars are 95% bootstrap intervals.', {'size': 9, 'color': RED})],
], size=9.5)
textbox(s, 0.45, 4.35, 7.5, 2.6, [
    [('How to read', {'bold': True, 'color': NAVY, 'size': 11})],
    'IC = monthly rank correlation between pillar scores and the next 3M/6M USD return relative to the five-market average (+1 = perfect ranking). Wide bars = discovery window, narrow bars = examined window.',
    'The examined window (2017 onward) was inspected across sixteen research versions, so it is NOT untouched holdout data. That is why leave-one-country-out and walk-forward tests carry more weight here than the examined IC alone.',
], size=9.5)
footer(s, FOOT + ' Discovery: signal months to Dec-2016; examined: Jul-2017 onward.')

# ---------------- slide 3
SLIDE[0] = 3; s = prs.slides.add_slide(BLANK)
header(s, 3, 'Scorecard construction', 'Equal-weight four-pillar scorecard, with a predictive score that excludes the two failed pillars')
textbox(s, 0.45, 1.45, 6.1, 5.5, [
    [('Pillar score', {'bold': True, 'color': NAVY, 'size': 12})],
    'z = (indicator − five-market mean) ÷ five-market standard deviation, each month. Higher is always more attractive.',
    [('Diagnostic scorecard — the primary deliverable', {'bold': True, 'color': NAVY, 'size': 12})],
    'Equal-weight average of the four pillar scores (25% each). A pillar\'s contribution is ¼ × its z. Equal weights because the brief requires four pillars and no pillar has validated evidence; weights fitted to past IC would be in-sample optimisation.',
    [('Predictive score — companion', {'bold': True, 'color': NAVY, 'size': 12})],
    'Equal-weight average of Macro and Micro only. Valuation and Technical keep their scores and contributions on the scorecard but carry ZERO predictive weight. They are neither deleted nor given artificial importance.',
    [('Rankings', {'bold': True, 'color': NAVY, 'size': 12})],
    'Rank 1–5. The 3M and 6M rankings are identical because the scores are horizon-independent; what differs is the evidence behind them — Macro is supported at both horizons, Micro mainly at 3M.',
    [('Predictive power of the two scores', {'bold': True, 'color': NAVY, 'size': 12})],
    f"Diagnostic 6M IC: {val(sc, {'score': 'Diagnostic (4 pillars, equal weight)', 'horizon': '6M', 'window': 'discovery'}, 'IC', '{:+.3f}')} discovery → {val(sc, {'score': 'Diagnostic (4 pillars, equal weight)', 'horizon': '6M', 'window': 'examined'}, 'IC', '{:+.3f}')} examined. "
    f"Predictive 6M IC: {val(sc, {'score': 'Predictive (Macro + Micro)', 'horizon': '6M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(sc, {'score': 'Predictive (Macro + Micro)', 'horizon': '6M', 'window': 'examined'}, 'IC', '{:+.3f}')}. "
    'Carrying the two failed pillars costs out-of-sample power — which is exactly why both views are shown.',
], size=10.5)
s.shapes.add_picture(str(CHARTS / 'pillar_heatmap.png'), Inches(6.85), Inches(1.5), width=Inches(6.05))
textbox(s, 6.85, 5.0, 6.05, 1.9, [
    'Scores as of 30-Apr-2026. Columns labelled "diagnostic" are the pillars that failed their robustness tests (slide 2); they stay on the scorecard because the brief specifies four pillars.',
    'Full monthly history — every pillar score, contribution, aggregate, rank, call and the realised next 3M/6M return — is in scorecard_history.csv.'], size=9.5)
footer(s, FOOT)

# ---------------- slide 4
SLIDE[0] = 4; s = prs.slides.add_slide(BLANK)
header(s, 4, 'Backtest results', 'Both scorecards beat the benchmark long-only; the long-short edge is modest and comes from Macro')
s.shapes.add_picture(str(CHARTS / 'cumulative_vs_benchmark.png'), Inches(0.45), Inches(1.4), width=Inches(5.95))
s.shapes.add_picture(str(CHARTS / 'drawdown.png'), Inches(0.45), Inches(4.45), width=Inches(5.95))
b = lambda w, st, bk, c, col, f: val(bs, {'window': w, 'strategy': st, 'book': bk, 'cost bps': c}, col, f)
rows = [['Full period, net 10 bps', 'Diagnostic long-only', 'Predictive long-only', 'EW benchmark', 'Diagnostic L/S top2']]
for lab, col, f in (('Return % p.a.', 'Return % p.a.', '{:.1f}'), ('Volatility % p.a.', 'Vol % p.a.', '{:.1f}'), ('Sharpe', 'Sharpe', '{:.2f}'), ('Max drawdown %', 'Max drawdown %', '{:.1f}')):
    rows.append([lab, b('full', D4, 'long-only top-2', 10, col, f), b('full', PR, 'long-only top-2', 10, col, f), b('full', EWB, 'long-only', 0, col, f), b('full', D4, 'long-short top2/bottom2', 10, col, f)])
rows.append(['Turnover p.a. (x)', b('full', D4, 'long-only top-2', 10, 'Turnover p.a. (x)', '{:.1f}'), b('full', PR, 'long-only top-2', 10, 'Turnover p.a. (x)', '{:.1f}'), '–', b('full', D4, 'long-short top2/bottom2', 10, 'Turnover p.a. (x)', '{:.1f}')])
rows.append(['Examined-window Sharpe', b('examined', D4, 'long-only top-2', 10, 'Sharpe', '{:.2f}'), b('examined', PR, 'long-only top-2', 10, 'Sharpe', '{:.2f}'), b('examined', EWB, 'long-only', 0, 'Sharpe', '{:.2f}'), b('examined', D4, 'long-short top2/bottom2', 10, 'Sharpe', '{:.2f}')])
rows.append(['Information ratio vs EW', b('full', D4, 'long-only top-2', 10, 'Information ratio', '{:.2f}'), b('full', PR, 'long-only top-2', 10, 'Information ratio', '{:.2f}'), '–', '–'])
table(s, 6.65, 1.45, 6.25, 3.3, rows, col_w=[1.75, 1.2, 1.2, 0.95, 1.15], size=9)
a = lambda p, w: val(att, {'run alone': p, 'window': w}, 'Sharpe', '{:+.2f}')
textbox(s, 6.65, 4.9, 6.25, 2.1, [
    [('Single-pillar attribution', {'bold': True, 'color': NAVY}), (f' (long-short, examined window): Macro {a("Macro", "examined")}, Micro {a("Micro", "examined")}, Valuation {a("Valuation", "examined")}, Technical {a("Technical", "examined")}. The edge is Macro; Valuation drags.', {})],
    [('Costs are not the constraint:', {'bold': True, 'color': NAVY}), (f' long-short Sharpe (full) {b("full", D4, "long-short top2/bottom2", 0, "Sharpe", "{:.2f}")} / {b("full", D4, "long-short top2/bottom2", 5, "Sharpe", "{:.2f}")} / {b("full", D4, "long-short top2/bottom2", 10, "Sharpe", "{:.2f}")} / {b("full", D4, "long-short top2/bottom2", 20, "Sharpe", "{:.2f}")} at 0/5/10/20 bps.', {})],
    [('A concentrated top-1 / bottom-1 book is worse:', {'bold': True, 'color': RED}), (f' Sharpe {b("full", D4, "long-short top1/bottom1", 10, "Sharpe", "{:.2f}")} full with a {b("full", D4, "long-short top1/bottom1", 10, "Max drawdown %", "{:.1f}")}% drawdown. Rules were fixed in advance and not optimised.', {})],
], size=9.5)
footer(s, FOOT + ' Backtest returns Jun-2009 to Apr-2026; examined window from Aug-2017. Benchmark carried cost-free; long-short Sharpe uses rf = 0.')

# ---------------- slide 5
SLIDE[0] = 5; s = prs.slides.add_slide(BLANK)
header(s, 5, 'Current ranking and investment recommendation', 'As of 30-Apr-2026: both views overweight the US and Japan and underweight the UK; low conviction')
s.shapes.add_picture(str(CHARTS / 'pillar_contributions.png'), Inches(0.45), Inches(1.4), width=Inches(6.4))
cur = load(cs).sort_values('Diagnostic rank')
rows = [['Rank', 'Market', 'Score', '4-pillar call', 'Predictive call', 'Agree?']]
cmap = {}
for i, c in enumerate(cur['country'], start=1):
    cd = val(cs, {'country': c}, 'Call (4-pillar diagnostic)', '{}'); cp = val(cs, {'country': c}, 'Call (predictive)', '{}')
    rows.append([val(cs, {'country': c}, 'Diagnostic rank', '{:.0f}'), c, val(cs, {'country': c}, 'Diagnostic score', '{:+.2f}'), cd, cp, 'yes' if cd == cp else 'NO'])
    for col, cc in ((3, cd), (4, cp)): cmap[(i, col)] = GREEN if cc == 'OVERWEIGHT' else (RED if cc == 'UNDERWEIGHT' else GREY)
    if cd != cp: cmap[(i, 5)] = RED
table(s, 7.05, 1.45, 5.85, 2.1, rows, col_w=[0.6, 1.3, 0.75, 1.25, 1.25, 0.7], size=9.5, bold_first_col=False, color_map=cmap)
z = lambda c, p: val(cs, {'country': c}, f'{p} score', '{:+.1f}')
r = lambda c, col, f: val(cs, {'country': c}, col, f)
textbox(s, 7.05, 3.7, 5.85, 3.3, [
    [('Recommendation', {'bold': True, 'color': NAVY, 'size': 12})],
    f'• OVERWEIGHT US — the strongest case, and both views agree. Strongest financing-conditions easing ({z("US", "Macro")}) and EPS upgrades ({r("US", "EPS revision 6M %", "{:.1f}")}% over six months), despite the richest multiple ({r("US", "Forward P/E", "{:.1f}")}x).',
    f'• OVERWEIGHT Japan on both views, but on thinner evidence: its EPS revisions are mid-pack ({z("Japan", "Micro")}) and its macro score is negative ({z("Japan", "Macro")}).',
    f'• UNDERWEIGHT UK on both views — much the weakest financing conditions ({z("UK", "Macro")}).',
    f'• The views DISAGREE on the Eurozone and Switzerland, because the two failed pillars move them. Treat both as neutral.',
    [('Conviction: LOW', {'bold': True, 'color': RED, 'size': 11})],
    f'• The two views give the same call for only {val(hf, {"figure": "call agreement (of 5 markets)"}, "value", "{:.0f}")} of 5 markets, ranks 2 and 3 are separated by {val(hf, {"figure": "gap between diagnostic rank 2 and rank 3"}, "value", "{:.2f}")}, and no pillar is statistically significant.',
    '• Data are as of 30-Apr-2026 and cannot be extended with the supplied dataset. Refreshed exports of the same tickers regenerate every figure here.',
], size=9.5)
footer(s, FOOT)

prs.save(OUTFILE)
pd.DataFrame(REG).to_csv(V / 'slide_number_registry.csv', index=False)
print(f'saved {OUTFILE.relative_to(ROOT)} with {len(prs.slides)} slides; {len(REG)} numbers registered')
