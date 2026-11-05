"""Reconcile every number in slides/Markets_Scorecard_FINAL.pptx with the v14 CSVs.

1. Re-read every registered number from its source CSV and re-format it (must match exactly).
2. Extract every numeric token from the deck's text and tables; each must be a registered value
   or a structural constant (dates, horizons, cost levels, weights, slide numbers).
Run from the repo root:  python3 slides/check_ppt_reconciliation.py
"""
import json, re
from pathlib import Path
import pandas as pd
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]; V = ROOT / 'output' / 'v14'
reg = pd.read_csv(V / 'slide_number_registry.csv')
fails = []
for _, r in reg.iterrows():
    df = pd.read_csv(V / r['file']); df = df.rename(columns={df.columns[0]: {'current_scorecard.csv': 'country', 'signal_classification.csv': 'pillar'}.get(r['file'], df.columns[0])})
    m = pd.Series(True, index=df.index)
    for k, v in json.loads(r['filter']).items(): m &= df[k].astype(str) == str(v)
    got = r['format'].format(df[m].iloc[0][r['column']])
    if got != str(r['displayed']): fails.append(('value mismatch', r['slide'], r['displayed'], got))
print(f'1) {len(reg)} registered numbers re-read from CSV: {len(reg) - len(fails)} match')
prs = Presentation(ROOT / 'slides' / 'Markets_Scorecard_FINAL.pptx')
STRUCT = {'1', '2', '3', '4', '5', '6', '0', '10', '12', '20', '25', '100', '2005', '2010', '2016', '2017', '2026', '3M', '6M', '12M', '30', '0.05', '500', '95', '14'}   # '500' = 'S&P 500' name; '95' = CI level; '14' = notebook version v14
tok = re.compile(r'[+\-−]?\d+(?:\.\d+)?')
norm = lambda x: x.replace('−', '-').lstrip('+')
allowed = {norm(x) for d in reg['displayed'].astype(str) for x in tok.findall(d)} | STRUCT
unreg = []
for i, slide in enumerate(prs.slides, 1):
    texts = []
    for sh in slide.shapes:
        if sh.has_text_frame: texts.append(sh.text_frame.text)
        if sh.has_table: texts += [c.text for row in sh.table.rows for c in row.cells]
    for t in texts:
        for x in tok.findall(t.replace('−', '-')):
            if norm(x) not in allowed and norm(x).lstrip('-') not in STRUCT: unreg.append((i, x, t[:60]))
print(f'2) numeric tokens on slides not traceable to the registry or a structural constant: {len(unreg)}')
for u in unreg: print('   ', u)
print(f'3) slide count = {len(prs.slides)} (brief: 4-5)')
ok = not fails and not unreg and 4 <= len(prs.slides) <= 5
print('RECONCILIATION', 'PASSED' if ok else 'FAILED', fails[:5])
raise SystemExit(0 if ok else 1)
