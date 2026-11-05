"""Reconcile every number in the v16 deck with the v16 CSVs. Run: python3 slides/check_v16_ppt.py"""
import json, re
from pathlib import Path
import pandas as pd
from pptx import Presentation
ROOT = Path(__file__).resolve().parents[1]; V = ROOT / 'output' / 'v16'
FIRSTCOL = {'signal_classification.csv': 'pillar', 'current_scorecard.csv': 'country', 'current_rankings_3m_6m.csv': 'country', 'headline_figures.csv': 'figure'}
reg = pd.read_csv(V / 'slide_number_registry.csv'); fails = []
for _, r in reg.iterrows():
    df = pd.read_csv(V / r['file'])
    if r['file'] in FIRSTCOL: df = df.rename(columns={df.columns[0]: FIRSTCOL[r['file']]})
    m = pd.Series(True, index=df.index)
    for k, v in json.loads(r['filter']).items(): m &= df[k].astype(str) == str(v)
    got = r['format'].format(df[m].iloc[0][r['column']])
    if got != str(r['displayed']): fails.append((r['slide'], r['file'], r['displayed'], got))
print(f'1) {len(reg)} registered numbers re-read from CSV: {len(reg) - len(fails)} match')
for f in fails: print('   MISMATCH', f)
prs = Presentation(ROOT / 'slides' / 'Markets_Scorecard_v16_FINAL.pptx')
STRUCT = {'1', '2', '3', '4', '5', '6', '0', '10', '12', '20', '25', '95', '2005', '2009', '2016', '2017', '2026', '0.04', '0.05', '500', '16', '30', '2014'}   # '30' = 30-Apr-2026; '2014' = start year of the from-2014 window
tok = re.compile(r'[+\-−]?\d+(?:\.\d+)?'); norm = lambda x: x.replace('−', '-').lstrip('+')
allowed = {norm(x) for d in reg['displayed'].astype(str) for x in tok.findall(d)} | STRUCT
unreg = []
for i, slide in enumerate(prs.slides, 1):
    texts = []
    for sh in slide.shapes:
        if sh.has_text_frame: texts.append(sh.text_frame.text)
        if sh.has_table: texts += [c.text for row in sh.table.rows for c in row.cells]
    for t in texts:
        for x in tok.findall(t.replace('−', '-')):
            if norm(x) not in allowed and norm(x).lstrip('-') not in STRUCT: unreg.append((i, x, t[:70]))
print(f'2) numeric tokens not traceable to the registry or a structural constant: {len(unreg)}')
for u in unreg: print('   ', u)
print(f'3) slide count = {len(prs.slides)} (brief: 4-5)')
ok = not fails and not unreg and 4 <= len(prs.slides) <= 5
print('RECONCILIATION', 'PASSED' if ok else 'FAILED')
raise SystemExit(0 if ok else 1)
