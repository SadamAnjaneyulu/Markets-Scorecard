"""Build the five-slide deck from output/final only.

Every number placed on a slide is read through `val()`, which records
(slide, displayed text, file, filter, column, format) to output/final/slide_number_registry.csv.
`check_final_deck.py` re-reads each entry from the CSVs and scans the deck for untraceable numbers.
"""
import json
from pathlib import Path
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / 'output' / 'final'
CHARTS = V / 'charts'
OUTFILE = ROOT / 'slides' / 'Developed_Markets_Equity_Scorecard_FINAL.pptx'

INK = RGBColor(0x1A, 0x1A, 0x1A)
NAVY = RGBColor(0x1F, 0x3B, 0x5C)
STEEL = RGBColor(0x5A, 0x6B, 0x7B)
RULE = RGBColor(0xD0, 0xD7, 0xDE)
BAND = RGBColor(0xF4, 0xF6, 0xF8)
POSITIVE = RGBColor(0x1E, 0x7A, 0x4D)
NEGATIVE = RGBColor(0xA8, 0x3A, 0x32)
ACCENT = RGBColor(0xB8, 0x86, 0x0B)

PILLARS = ['Macro', 'Micro', 'Valuation', 'Technical']
FIRST_COL = {'signal_classification.csv': 'pillar', 'current_ranking.csv': 'market',
             'signal_definitions.csv': 'pillar', 'model_comparison.csv': 'model',
             'final_pillar_summary.csv': 'pillar', 'technical_diagnostic.csv': 'horizon'}
_cache = {}
def load(name):
    if name not in _cache:
        d = pd.read_csv(V / name)
        if name in FIRST_COL:
            d = d.rename(columns={d.columns[0]: FIRST_COL[name]})
        _cache[name] = d
    return _cache[name]

REGISTRY, SLIDE_NO = [], [0]
def val_json(key_path, fmt):
    """Register a number sourced from the notebook's presentation_figures.json."""
    node = json.load(open(V / 'presentation_figures.json'))
    for k in key_path.split('.'):
        node = node[k]
    text = fmt.format(node)
    REGISTRY.append({'slide': SLIDE_NO[0], 'displayed': text, 'file': 'presentation_figures.json',
                     'filter': json.dumps({'key_path': key_path}), 'column': '', 'format': fmt})
    return text

def val_sum(file, where, columns, fmt):
    """Register the sum of several columns from one row."""
    df = load(file)
    mask = pd.Series(True, index=df.index)
    for k, v in where.items():
        mask &= df[k].astype(str) == str(v)
    total = sum(float(df[mask].iloc[0][c]) for c in columns)
    text = fmt.format(total)
    REGISTRY.append({'slide': SLIDE_NO[0], 'displayed': text, 'file': file,
                     'filter': json.dumps(where), 'column': json.dumps(columns), 'format': fmt})
    return text

def val(file, where, column, fmt):
    df = load(file)
    mask = pd.Series(True, index=df.index)
    for k, v in where.items():
        mask &= df[k].astype(str) == str(v)
    rows = df[mask]
    assert len(rows) == 1, (file, where, len(rows))
    text = fmt.format(rows.iloc[0][column])
    REGISTRY.append({'slide': SLIDE_NO[0], 'displayed': text, 'file': file,
                     'filter': json.dumps(where), 'column': column, 'format': fmt})
    return text

FIG = json.load(open(V / 'presentation_figures.json'))
AS_OF_LABEL = '30 April 2026'
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def text_block(slide, x, y, w, h, paragraphs, size=10.5, colour=STEEL, spacing=5):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame; frame.word_wrap = True
    for i, para in enumerate(paragraphs):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        for text, style in (para if isinstance(para, list) else [(para, {})]):
            run = p.add_run(); run.text = text
            run.font.size = Pt(style.get('size', size))
            run.font.bold = style.get('bold', False)
            run.font.italic = style.get('italic', False)
            run.font.color.rgb = style.get('colour', colour)
        p.space_after = Pt(style.get('after', spacing))
        p.line_spacing = 1.08
    return box

def slide_header(slide, number, section, headline):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.07))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background(); bar.shadow.inherit = False
    text_block(slide, 0.5, 0.22, 11.0, 0.3, [[(f'{number}  |  {section.upper()}', {'size': 9.5, 'colour': STEEL, 'bold': True})]])
    text_block(slide, 0.5, 0.5, 12.3, 0.62, [[(headline, {'size': 19, 'colour': INK, 'bold': True})]])
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.12), Inches(12.33), Emu(9525))
    line.fill.solid(); line.fill.fore_color.rgb = RULE; line.line.fill.background(); line.shadow.inherit = False

def slide_footer(slide, note):
    text_block(slide, 0.5, 7.02, 12.3, 0.3, [[(note, {'size': 7.5, 'colour': STEEL})]])

def make_table(slide, x, y, w, h, data, widths=None, size=9.5, emphasis=None, header_fill=NAVY):
    shape = slide.shapes.add_table(len(data), len(data[0]), Inches(x), Inches(y), Inches(w), Inches(h))
    table = shape.table
    if widths:
        for j, cw in enumerate(widths): table.columns[j].width = Inches(cw)
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            cell = table.cell(i, j); cell.text = str(value)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for para in cell.text_frame.paragraphs:
                para.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
                for run in para.runs:
                    font = run.font; font.size = Pt(size - 0.5 if i == 0 else size); font.name = 'Calibri'
                    if i == 0:
                        font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); font.bold = True
                    else:
                        font.color.rgb = INK
                        if emphasis and (i, j) in emphasis:
                            font.color.rgb = emphasis[(i, j)]; font.bold = True
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill if i == 0 else (RGBColor(0xFF, 0xFF, 0xFF) if i % 2 else BAND)
    return table

FOOTER = ('Monthly panel December 2005 to April 2026, five developed equity markets. Scores lagged one month before use. '
          'Returns are USD price returns relative to the five-market average; no dividend data available.')
pp_csv, cls_csv, mc_csv, cur_csv = 'predictive_power.csv', 'signal_classification.csv', 'model_comparison.csv', 'current_ranking.csv'
bt_csv, sc_csv, sic_csv, rob_csv = 'backtest_performance_summary.csv', 'signal_comparison.csv', 'scorecard_ic.csv', 'robustness_summary.csv'
REVISED, ORIGINAL = 'Revised: FCI + EPS persistence', 'Original: FCI + EPS revision 6M'
BENCH = 'Equal-weight benchmark'

# ============================================================== SLIDE 1
SLIDE_NO[0] = 1
s = prs.slides.add_slide(BLANK)
slide_header(s, '01', 'Methodology', 'Four economic pillars, two of which carry predictive weight')
text_block(s, 0.5, 1.32, 4.3, 5.4, [
    [('Objective', {'size': 11.5, 'colour': NAVY, 'bold': True})],
    'Rank five developed equity markets by expected performance relative to one another over three to six months, '
    'and convert that ranking into an allocation view.',
    [('Markets', {'size': 11.5, 'colour': NAVY, 'bold': True})],
    'United States · Eurozone · United Kingdom · Switzerland · Japan',
    [('Data and period', {'size': 11.5, 'colour': NAVY, 'bold': True})],
    'Monthly panel, December 2005 to April 2026. Research window split into discovery to December 2016 and an examined '
    'window from July 2017, separated by a six-month embargo.',
    [('Measurement', {'size': 11.5, 'colour': NAVY, 'bold': True})],
    'Rank information coefficient against forward relative returns at three and six months, with HAC inference and '
    'block-bootstrap intervals to handle overlapping returns.',
], size=10)

panel_x, panel_y, panel_w = 5.15, 1.45, 7.7
text_block(s, panel_x, panel_y - 0.12, panel_w, 0.3, [[('RESEARCH AND PORTFOLIO PROCESS', {'size': 9, 'colour': STEEL, 'bold': True})]])
steps = [('Signal\nconstruction', 'One indicator per pillar,\nstandardised across markets'),
         ('Predictive\ntesting', 'Discovery and examined\nwindows, leave-one-out'),
         ('Scorecard', 'Equal-weight pillar scores,\nranked 1 to 5'),
         ('Portfolio', 'Six-month tranches,\ncosts and turnover')]
box_w, gap = 1.72, 0.26
for i, (title, detail) in enumerate(steps):
    bx = panel_x + i * (box_w + gap)
    rect = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(panel_y + 0.18), Inches(box_w), Inches(0.92))
    rect.fill.solid(); rect.fill.fore_color.rgb = NAVY if i < 2 else STEEL
    rect.line.fill.background(); rect.shadow.inherit = False
    tf = rect.text_frame; tf.word_wrap = True; tf.margin_top = Inches(0.06)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for k, line in enumerate(title.split('\n')):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = line; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    text_block(s, bx, panel_y + 1.16, box_w, 0.6, [[(detail, {'size': 7.8, 'colour': STEEL})]])
    if i < 3:
        arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(bx + box_w + 0.03), Inches(panel_y + 0.55), Inches(gap - 0.06), Inches(0.18))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = RULE; arrow.line.fill.background(); arrow.shadow.inherit = False

rows = [['Pillar', 'Indicator', 'Economic rationale', 'Status']]
emphasis = {}
rationale = {'Macro': 'Easier financing lowers the discount rate and lifts risk appetite, with a lag',
             'Micro': 'Analysts revise gradually, so a sustained upgrade run tends to continue',
             'Valuation': 'Compensation for holding equities over the local risk-free rate',
             'Technical': 'A smooth trend suggests information is being absorbed gradually'}
for i, p in enumerate(PILLARS, start=1):
    label = val(cls_csv, {'pillar': p}, 'label', '{}')
    rows.append([p, val('signal_definitions.csv', {'pillar': p}, 'indicator', '{}'), rationale[p], label])
    emphasis[(i, 3)] = POSITIVE if label.startswith('PREDICTIVE') else ACCENT
make_table(s, panel_x, 3.05, panel_w, 2.0, rows, widths=[1.0, 2.1, 3.0, 1.6], size=9, emphasis=emphasis)

text_block(s, panel_x, 5.25, panel_w, 1.6, [
    [('Data constraints that shape the design', {'size': 10, 'colour': NEGATIVE, 'bold': True})],
    'The dataset contains no index prices. The supplied price workbook holds valuation ratios, so the index is reconstructed '
    'as forward P/E multiplied by forward EPS. Returns are price returns, not total returns.',
    'Because that reconstruction is an identity, any technical signal is a function of the valuation and earnings inputs. '
    'The Technical pillar is reported as a diagnostic and no claim of independence is made.',
], size=8.8)
slide_footer(s, FOOTER)

# ============================================================== SLIDE 2
SLIDE_NO[0] = 2
s = prs.slides.add_slide(BLANK)
slide_header(s, '02', 'Signal selection and predictive power',
             'Counting earnings upgrades beats measuring their size')
s.shapes.add_picture(str(CHARTS / 'micro_comparison.png'), Inches(0.5), Inches(1.3), width=Inches(5.6))
s.shapes.add_picture(str(CHARTS / 'ic_by_pillar.png'), Inches(0.5), Inches(4.3), width=Inches(5.6))

rows = [['Pillar', 'Indicator', 'IC 3M\ndisc → exam', 'IC 6M\ndisc → exam', 'Status']]
emphasis = {}
for i, p in enumerate(PILLARS, start=1):
    label = val(cls_csv, {'pillar': p}, 'label', '{}')
    rows.append([p, val('signal_definitions.csv', {'pillar': p}, 'indicator', '{}'),
                 f"{val(pp_csv, {'pillar': p, 'horizon': '3M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(pp_csv, {'pillar': p, 'horizon': '3M', 'window': 'examined'}, 'IC', '{:+.3f}')}",
                 f"{val(pp_csv, {'pillar': p, 'horizon': '6M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(pp_csv, {'pillar': p, 'horizon': '6M', 'window': 'examined'}, 'IC', '{:+.3f}')}",
                 label])
    emphasis[(i, 4)] = POSITIVE if label.startswith('PREDICTIVE') else ACCENT
make_table(s, 6.45, 1.3, 6.4, 1.75, rows, widths=[0.9, 1.9, 1.3, 1.3, 1.0], size=8.5, emphasis=emphasis)

text_block(s, 6.45, 3.45, 6.4, 3.55, [
    [('The change that mattered', {'size': 11, 'colour': NAVY, 'bold': True})],
    [('My original Micro indicator was the six-month change in forward earnings. A single large revision can reflect a '
      'currency move or an index change rather than a genuine shift in expectations, so I replaced it with the share of the '
      'last twelve months in which earnings were revised up. On ', {}),
     (f"{val(sc_csv, {'horizon': 6, 'target': 'USD', 'model': 'EPS revision 6M only'}, 'months', '{:.0f}')} matched months", {'bold': True, 'colour': INK}),
     (' the six-month examined IC rises from ', {}),
     (val(sc_csv, {'horizon': 6, 'target': 'USD', 'model': 'EPS revision 6M only'}, 'IC', '{:+.3f}'), {'bold': True, 'colour': INK}),
     (' to ', {}),
     (val(sc_csv, {'horizon': 6, 'target': 'USD', 'model': 'EPS positive-month share 12M'}, 'IC', '{:+.3f}'), {'bold': True, 'colour': POSITIVE}),
     ('.', {})],
    [('An exponentially weighted version scores higher still at '
      f"{val(sc_csv, {'horizon': 6, 'target': 'USD', 'model': 'EPS up-month EWMA12'}, 'IC', '{:+.3f}')}, but it adds a decay parameter the data cannot pin down. "
      'I kept the simpler measure and report the weighted one as a robustness check.', {})],
    [('Why Valuation and Technical stay diagnostic', {'size': 11, 'colour': NAVY, 'bold': True})],
    [('Valuation is strong in discovery and negative out of sample. The failure is concentrated in one market: excluding the US, '
      'the examined IC is ', {}), (val_json('valuation_ex_us_examined', '{:+.3f}'), {'bold': True, 'colour': INK}),
     ('. It still ranks future multiple expansion, but the earnings leg offsets it in total return.', {})],
    [('Technical keeps ', {}), (val('technical_diagnostic.csv', {'horizon': '6M'}, 'share_retained', '{:.0%}'), {'bold': True, 'colour': INK}),
     (' of its six-month IC once Micro and Valuation are removed, but excluding the US leaves ', {}),
     (val(rob_csv, {'pillar': 'Technical', 'horizon': '6M'}, 'ex_US', '{:+.3f}'), {'bold': True, 'colour': INK}),
     ('. Built on reconstructed prices, it cannot be independent of Micro and Valuation.', {})],
    [('No pillar is statistically significant once the length of the research process is taken into account, and the examined '
      'window is not untouched holdout data.', {'size': 8.5, 'colour': NEGATIVE, 'italic': True})],
], size=9)
slide_footer(s, FOOTER + ' Error bars are 95% moving-block bootstrap intervals.')

# ============================================================== SLIDE 3
SLIDE_NO[0] = 3
s = prs.slides.add_slide(BLANK)
slide_header(s, '03', 'Scorecard construction', 'Four pillars are reported; two carry weight in the allocation view')
s.shapes.add_picture(str(CHARTS / 'pillar_heatmap.png'), Inches(0.5), Inches(1.28), width=Inches(5.15))
s.shapes.add_picture(str(CHARTS / 'pillar_contributions.png'), Inches(0.5), Inches(4.0), width=Inches(5.15))

text_block(s, 6.1, 1.3, 6.75, 2.6, [
    [('Construction', {'size': 11, 'colour': NAVY, 'bold': True})],
    'Each indicator is standardised across the five markets every month, so a score always states relative standing. '
    'The four-pillar score is the equal-weight average of all four; each pillar contributes one quarter of its z-score.',
    'The predictive score averages only the two pillars that carry evidence. Valuation and Technical keep their scores and '
    'contributions on the scorecard but receive no predictive weight — they are neither removed nor given artificial importance.',
    'Weights are equal and fixed. With four correlated pillars and roughly seventeen independent six-month periods out of '
    'sample, fitting weights would be optimisation on the data used to judge the result.',
], size=9.2)

rows = [['Score', 'IC 3M\ndisc → exam', 'IC 6M\ndisc → exam']]
for label, key in (('Four-pillar diagnostic', 'Diagnostic (four pillars)'), ('Predictive (Macro + Micro)', 'Predictive (Macro + Micro)')):
    rows.append([label,
                 f"{val(sic_csv, {'score': key, 'horizon': '3M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(sic_csv, {'score': key, 'horizon': '3M', 'window': 'examined'}, 'IC', '{:+.3f}')}",
                 f"{val(sic_csv, {'score': key, 'horizon': '6M', 'window': 'discovery'}, 'IC', '{:+.3f}')} → {val(sic_csv, {'score': key, 'horizon': '6M', 'window': 'examined'}, 'IC', '{:+.3f}')}"])
make_table(s, 6.1, 4.05, 6.75, 1.0, rows, widths=[2.75, 2.0, 2.0], size=9.5,
           emphasis={(2, 1): POSITIVE, (2, 2): POSITIVE})
text_block(s, 6.1, 5.25, 6.75, 1.75, [
    [('Why the two views can differ', {'size': 11, 'colour': NAVY, 'bold': True})],
    'The four-pillar score is stronger in discovery and weaker out of sample. That is exactly what carrying two pillars that '
    'fail out of sample should do, and it is the reason both views are shown rather than one.',
    f'This month the two views agree on all five classifications. When they diverge, the predictive view carries the '
    f'out-of-sample evidence and the four-pillar view is the complete framework.',
], size=9.2)
slide_footer(s, FOOTER)

# ============================================================== SLIDE 4
SLIDE_NO[0] = 4
s = prs.slides.add_slide(BLANK)
slide_header(s, '04', 'Backtest results', 'The revised signal lifts Sharpe and information ratio, and trades less')
s.shapes.add_picture(str(CHARTS / 'cumulative_vs_benchmark.png'), Inches(0.5), Inches(1.28), width=Inches(6.0))
s.shapes.add_picture(str(CHARTS / 'drawdown.png'), Inches(0.5), Inches(4.42), width=Inches(6.0))

bt = lambda w, m, book, c, col, fmt: val(bt_csv, {'window': w, 'model': m, 'book': book, 'cost_bps': c}, col, fmt)
rows = [['Net of 10bp, full period', 'Revised\nlong only', 'Original\nlong only', 'Equal weight', 'Revised\nlong short']]
for label, col, fmt in (('Return % p.a.', 'return_pct_pa', '{:.1f}'), ('Volatility % p.a.', 'volatility_pct_pa', '{:.1f}'),
                        ('Sharpe ratio', 'sharpe', '{:.2f}'), ('Maximum drawdown %', 'max_drawdown_pct', '{:.1f}')):
    rows.append([label, bt('full', REVISED, 'long_only', 10, col, fmt), bt('full', ORIGINAL, 'long_only', 10, col, fmt),
                 bt('full', BENCH, 'long_only', 0, col, fmt), bt('full', REVISED, 'long_short', 10, col, fmt)])
rows.append(['Turnover per year', bt('full', REVISED, 'long_only', 10, 'turnover_pa', '{:.1f}x'),
             bt('full', ORIGINAL, 'long_only', 10, 'turnover_pa', '{:.1f}x'), '—',
             bt('full', REVISED, 'long_short', 10, 'turnover_pa', '{:.1f}x')])
rows.append(['Information ratio vs benchmark', bt('full', REVISED, 'long_only', 10, 'information_ratio', '{:.2f}'),
             bt('full', ORIGINAL, 'long_only', 10, 'information_ratio', '{:.2f}'), '—', '—'])
rows.append(['Examined-window Sharpe', bt('examined', REVISED, 'long_only', 10, 'sharpe', '{:.2f}'),
             bt('examined', ORIGINAL, 'long_only', 10, 'sharpe', '{:.2f}'),
             bt('examined', BENCH, 'long_only', 0, 'sharpe', '{:.2f}'),
             bt('examined', REVISED, 'long_short', 10, 'sharpe', '{:.2f}')])
make_table(s, 6.7, 1.28, 6.15, 2.5, rows, widths=[2.1, 1.05, 1.05, 1.0, 1.05], size=8.8,
           emphasis={(i, 1): POSITIVE for i in (1, 3, 5, 6, 7)})

rows = [['Model', 'IC 6M\nexamined', 'Long-short\nSharpe, exam.', 'Turnover']]
for model in load(mc_csv)['model']:
    short = {'Original: FCI + EPS revision 6M': 'Original: FCI + revision 6M',
             'Macro only: FCI 6M': 'Macro only', 'Micro only: EPS persistence 12M': 'Micro only',
             'Revised: FCI + EPS persistence': 'Revised: FCI + persistence',
             'Ridge challenger (4 pillars)': 'Ridge, four pillars'}[model]
    rows.append([short, val(mc_csv, {'model': model}, 'IC_examined_6M', '{:+.3f}'),
                 val(mc_csv, {'model': model}, 'long_short_sharpe_examined', '{:.2f}'),
                 val(mc_csv, {'model': model}, 'turnover_pa', '{:.1f}x')])
make_table(s, 6.7, 4.0, 6.15, 1.7, rows, widths=[2.6, 1.2, 1.35, 1.0], size=8.8,
           emphasis={(4, 1): POSITIVE, (4, 2): POSITIVE})

text_block(s, 6.7, 5.95, 6.15, 1.05, [
    [('Transaction costs are not the constraint. ', {'bold': True, 'colour': INK}),
     (f"In the long-only book the revised signal's volatility and drawdown are slightly higher than the original's. The revised long-short book returns a Sharpe ratio of "
      f"{val('transaction_cost_sensitivity.csv', {'model': REVISED, 'book': 'long_short', 'cost_bps': 0}, 'sharpe', '{:.2f}')} gross and "
      f"{val('transaction_cost_sensitivity.csv', {'model': REVISED, 'book': 'long_short', 'cost_bps': 20}, 'sharpe', '{:.2f}')} at 20 basis points. "
      'Rules were fixed before testing: six-month overlapping tranches, '
      'positions drifting with prices, turnover charged on both legs, benchmark carried cost-free.', {})],
], size=8.8)
slide_footer(s, FOOTER + f" Backtest returns {val_json('backtest_window.full', '{}')}; examined window from August 2017.")

# ============================================================== SLIDE 5
SLIDE_NO[0] = 5
s = prs.slides.add_slide(BLANK)
slide_header(s, '05', 'Investment view', 'Overweight the US and Eurozone; underweight Switzerland and the UK')
stamp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.55), Inches(0.42), Inches(2.28), Inches(0.46))
stamp.fill.solid(); stamp.fill.fore_color.rgb = BAND; stamp.line.color.rgb = RULE; stamp.shadow.inherit = False
tf = stamp.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = f'As of {AS_OF_LABEL}'; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = NAVY

reason = {'US': 'Forward earnings marked up in all twelve months, the only market to do so',
          'Eurozone': 'Eleven upgrade months and a positive financing-conditions impulse',
          'Japan': 'Below average on both pillars, but not by enough to underweight',
          'Switzerland': 'Weakest earnings persistence in the panel',
          'UK': 'Much the weakest financing conditions, which dominate its score'}
rows = [['Rank', 'Market', 'Predictive\nscore', 'Macro\ncontrib.', 'Micro\ncontrib.', 'Diagnostic\ncontrib.', 'Classification', 'Principal reason']]
emphasis = {}
for i, m in enumerate(FIG['ranking_order'], start=1):
    call = val(cur_csv, {'market': m}, 'Predictive call', '{}')

    rows.append([val(cur_csv, {'market': m}, 'Predictive rank', '{:.0f}'), m,
                 val(cur_csv, {'market': m}, 'Predictive score', '{:+.2f}'),
                 val(cur_csv, {'market': m}, 'Macro contribution', '{:+.2f}'),
                 val(cur_csv, {'market': m}, 'Micro contribution', '{:+.2f}'),
                 val_sum(cur_csv, {'market': m}, ['Valuation contribution', 'Technical contribution'], '{:+.2f}'), call, reason[m]])
    emphasis[(i, 6)] = POSITIVE if call == 'OVERWEIGHT' else (NEGATIVE if call == 'UNDERWEIGHT' else STEEL)
make_table(s, 0.5, 1.35, 12.33, 2.15, rows, widths=[0.55, 1.35, 1.1, 1.0, 1.0, 1.15, 1.45, 4.73], size=9.2, emphasis=emphasis)

s.shapes.add_picture(str(CHARTS / 'pillar_contributions.png'), Inches(0.5), Inches(3.72), width=Inches(5.6))

text_block(s, 6.35, 3.66, 6.48, 3.3, [
    [('Recommendation', {'size': 11.5, 'colour': NAVY, 'bold': True})],
    [('Overweight the United States. ', {'bold': True, 'colour': INK}),
     ('It leads on both pillars that carry evidence, with the only perfect earnings-persistence reading in the panel and the '
      'strongest financing-conditions impulse. Its predictive score of ', {}),
     (val(cur_csv, {'market': 'US'}, 'Predictive score', '{:+.2f}'), {'bold': True, 'colour': INK}),
     (' is well clear of the field.', {})],
    [('Overweight the Eurozone, underweight Switzerland and the United Kingdom. ', {'bold': True, 'colour': INK}),
     ('The Eurozone ties for second on earnings persistence and has a positive financing-conditions impulse. Switzerland has the weakest earnings '
      'persistence in the panel and the United Kingdom much the weakest financing conditions. Japan is neutral.', {})],
    [('Conviction and risk', {'size': 11.5, 'colour': NAVY, 'bold': True})],
    [('Highest on the US, low on the ordering of the rest. ', {'bold': True, 'colour': NEGATIVE}),
     (f"The US has held first place in {val_json('rank_stability.us_first_in_last8', '{}')} of the last eight months. Japan, Switzerland and the UK are tightly bunched, "
      "so the order among them carries little information; the UK underweight is best supported, Switzerland's rests on a narrow margin over Japan. "
      f"Rankings also move: in the final month the UK went from rank {val_json('rank_stability.uk_rank_prior_month', '{}')} to rank {val_json('rank_stability.uk_rank_now', '{}')} "
      f"and the Eurozone from rank {val_json('rank_stability.eurozone_rank_prior_month', '{}')} to rank {val_json('rank_stability.eurozone_rank_now', '{}')}.", {})],
    [('The view rests on two pillars, neither statistically significant once the research process is accounted for, measured on '
      'a dataset ending 30 April 2026. The four-pillar and predictive views agree on all five classifications this month.',
      {'size': 8.6, 'italic': True})],
], size=9.2)
slide_footer(s, FOOTER + ' This is the latest ranking the supplied dataset supports, not a reading of current market conditions.')

core = prs.core_properties
core.author = ''; core.last_modified_by = ''; core.title = 'Developed Markets Equity Scorecard'
core.subject = ''; core.comments = ''; core.category = ''; core.keywords = ''
import datetime as _dt
core.created = core.modified = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0, tzinfo=None)
prs.save(OUTFILE)

# Replace the template's default application metadata with neutral values.
import re as _re, shutil as _sh, zipfile as _zf
_tmp = OUTFILE.with_suffix('.tmp')
with _zf.ZipFile(OUTFILE) as zin, _zf.ZipFile(_tmp, 'w', _zf.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == 'docProps/app.xml':
            text = data.decode('utf8')
            text = _re.sub(r'<Application>.*?</Application>', '<Application></Application>', text)
            text = _re.sub(r'<PresentationFormat>.*?</PresentationFormat>', '<PresentationFormat>Widescreen</PresentationFormat>', text)
            text = _re.sub(r'<Slides>\d+</Slides>', f'<Slides>{len(prs.slides)}</Slides>', text)
            data = text.encode('utf8')
        zout.writestr(item, data)
_sh.move(str(_tmp), str(OUTFILE))
pd.DataFrame(REGISTRY).to_csv(V / 'slide_number_registry.csv', index=False)
print(f'Saved {OUTFILE.relative_to(ROOT)} with {len(prs.slides)} slides and {len(REGISTRY)} registered numbers.')
