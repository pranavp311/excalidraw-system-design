#!/usr/bin/env python3
"""Keep native scenes out of the toolkit's shorthand converter (2.0.0 only)."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('package', type=Path, help='Installed mcp-excalidraw-server directory')
args = parser.parse_args()
if json.loads((args.package / 'package.json').read_text()).get('version') != '2.0.0':
    parser.exit(1, 'This compatibility patch only supports version 2.0.0.\n')
needle = 'B3=e=>{if(e.length===0)return[];const t=Ove(e)'
replacement = ('B3=e=>{if(e.length===0)return[];'
    'if(e.every(x=>typeof x.versionNonce==="number"&&typeof x.isDeleted==="boolean"))'
    'return Ove(e.filter(x=>!x.isDeleted)).map(x=>({...x,version:x.version||1}));'
    'const t=Ove(e)')
matches = []
for path in (args.package / 'dist/frontend/assets').glob('index-*.js'):
    contents = path.read_text()
    if replacement in contents:
        print('Compatibility patch already applied.')
        raise SystemExit(0)
    if needle in contents:
        matches.append((path, contents))
if len(matches) != 1 or matches[0][1].count(needle) != 1:
    parser.exit(1, 'Unexpected frontend build; no files changed.\n')
path, contents = matches[0]
backup = path.with_suffix('.js.original')
if backup.exists():
    parser.exit(1, 'Backup already exists; inspect before retrying.\n')
backup.write_text(contents)
path.write_text(contents.replace(needle, replacement))
print('Patched local frontend; original saved alongside it. Reload the canvas.')
