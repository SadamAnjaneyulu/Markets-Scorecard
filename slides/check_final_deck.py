"""Verify every number on the deck against output/final, and scan for identifying names."""
import json, re, zipfile
from pathlib import Path
import pandas as pd
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / 'output' / 'final'
DECK = ROOT / 'slides' / 'Developed_Markets_Equity_Scorecard_FINAL.pptx'
FIRST_COL = {'signal_classification.csv': 'pillar', 'current_ranking.csv': 'market',
             'signal_definitions.csv': 'pillar', 'model_comparison.csv': 'model',
             'final_pillar_summary.csv': 'pillar', 'technical_diagnostic.csv': 'horizon'}
registry = pd.read_csv(V / 'slide_number_registry.csv')
mismatches = []
figures_json = json.load(open(V / 'presentation_figures.json'))
for _, row in registry.iterrows():
    if row['file'] == 'presentation_figures.json':
        node = figures_json
        for k in json.loads(row['filter'])['key_path'].split('.'):
            node = node[k]
        if row['format'].format(node) != str(row['displayed']):
            mismatches.append((row['slide'], row['file'], row['displayed'], row['format'].format(node)))
        continue
    df = pd.read_csv(V / row['file'])
    if row['file'] in FIRST_COL:
        df = df.rename(columns={df.columns[0]: FIRST_COL[row['file']]})
    mask = pd.Series(True, index=df.index)
    for k, v in json.loads(row['filter']).items():
        mask &= df[k].astype(str) == str(v)
    column = row['column']
    if isinstance(column, str) and column.startswith('['):
        produced = row['format'].format(sum(float(df[mask].iloc[0][c]) for c in json.loads(column)))
    else:
        produced = row['format'].format(df[mask].iloc[0][column])
    if produced != str(row['displayed']):
        mismatches.append((row['slide'], row['file'], row['displayed'], produced))
print(f'1. Registered numbers re-read from CSV: {len(registry) - len(mismatches)} of {len(registry)} match')
for m in mismatches: print('   MISMATCH', m)

prs = Presentation(DECK)
STRUCTURAL = {'1', '2', '3', '4', '5', '6', '01', '02', '03', '04', '05', '10', '12', '17', '20', '25', '30', '95',
              '2005', '2009', '2016', '2017', '2026'}
token = re.compile(r'[+\-−]?\d+(?:\.\d+)?')
norm = lambda x: x.replace('−', '-').lstrip('+')
allowed = {norm(t) for d in registry['displayed'].astype(str) for t in token.findall(d)} | STRUCTURAL
untraceable = []
for i, slide in enumerate(prs.slides, 1):
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame: texts.append(shape.text_frame.text)
        if shape.has_table: texts += [c.text for r in shape.table.rows for c in r.cells]
    for t in texts:
        for x in token.findall(t.replace('−', '-')):
            if norm(x) not in allowed and norm(x).lstrip('-') not in STRUCTURAL:
                untraceable.append((i, x, t[:70].replace('\n', ' ')))
print(f'2. Numeric tokens not traceable to the registry or a structural constant: {len(untraceable)}')
for u in untraceable: print('   ', u)
print(f'3. Slide count: {len(prs.slides)} (required: 4 to 5)')

import os
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
extra_terms = [t.strip().lower() for t in os.environ.get('DECK_FORBIDDEN_TERMS', '').split(',') if t.strip()]
blob = zipfile.ZipFile(DECK).read('docProps/core.xml').decode('utf8', 'ignore')
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame: blob += ' ' + shape.text_frame.text
        if shape.has_table: blob += ' ' + ' '.join(c.text for r in shape.table.rows for c in r.cells)
    if slide.has_notes_slide: blob += ' ' + slide.notes_slide.notes_text_frame.text
hits = sorted({m for m in EMAIL.findall(blob)} | {t for t in extra_terms if t in blob.lower()})
print(f'4. Email addresses and any terms in DECK_FORBIDDEN_TERMS found in deck text, notes or properties: {hits if hits else "none"}')

ok = not mismatches and not untraceable and 4 <= len(prs.slides) <= 5 and not hits
print('DECK CHECK', 'PASSED' if ok else 'FAILED')
raise SystemExit(0 if ok else 1)
