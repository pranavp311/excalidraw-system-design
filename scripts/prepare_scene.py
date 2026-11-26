#!/usr/bin/env python3
"""Prepare a separate active-only Excalidraw copy for canvas import."""
import argparse
import json
from pathlib import Path


def prepare(source, destination):
    if source.resolve() == destination.resolve():
        raise ValueError('Use a separate output file; originals are never overwritten.')
    data = json.loads(source.read_text())
    if data.get('type') != 'excalidraw' or not isinstance(data.get('elements'), list):
        raise ValueError('Expected an Excalidraw scene with an elements array.')
    elements = [e for e in data['elements'] if not e.get('isDeleted')]
    ids = [e.get('id') for e in elements]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Active elements require unique nonempty string IDs.')
    active = set(ids)
    for element in elements:
        # The 2.0.0 export writes invalid order keys (a0..a301); Excalidraw rebuilds them from array order.
        element.pop('index', None)
        if element.get('boundElements'):
            element['boundElements'] = [b for b in element['boundElements'] if b.get('id') in active]
        for field in ('startBinding', 'endBinding'):
            if element.get(field) and element[field].get('elementId') not in active:
                element[field] = None
        for field in ('containerId', 'frameId'):
            if element.get(field) and element[field] not in active:
                element[field] = None
    missing = {e.get('fileId') for e in elements if e.get('type') == 'image'} - set(data.get('files', {}))
    if missing:
        raise ValueError(f'Missing embedded image files: {sorted(str(x) for x in missing)}')
    removed = len(data['elements']) - len(elements)
    data['elements'] = elements
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x') as output:
        json.dump(data, output, ensure_ascii=False, indent=2)
    print(f'{len(elements)} active elements; {removed} deleted elements removed; wrote {destination}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        prepare(args.source, args.destination)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
