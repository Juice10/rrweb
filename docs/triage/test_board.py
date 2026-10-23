"""Offline snapshot consistency and deterministic generation checks."""
import copy
import json
import unittest
from collections import Counter

import build_board as board


class BoardTest(unittest.TestCase):
    def test_refresh(self):
        historical = board.assemble()
        items = board.apply_refresh(copy.deepcopy(historical))
        counts = Counter(p['upstreamState'] for p in items)
        self.assertEqual(counts, {'Open': 140, 'Merged': 11, 'Closed unmerged': 6, 'Issue status not refreshed': 289})
        self.assertEqual(len({(p['kind'], p['id']) for p in items}), 446)
        self.assertEqual(sum(not p['historical'] for p in items), 19)
        by_id = {(p['kind'], p['id']): p for p in items}
        for old in historical:
            new = by_id[(old['kind'], old['id'])]
            for field in ('triage', 'reason', 'next', 'notes', 'downstream', 'downstreamLinks', 'related', 'message', 'tags', 'reviewDecision'):
                self.assertEqual(old[field], new[field], (old['id'], field))
        for p in items:
            if not p['historical']:
                self.assertEqual(p['triage'], 'review')
                self.assertNotIn('approved', p['tags'])
                self.assertEqual(p['message'], '')

    def test_generated_html_matches(self):
        items = board.apply_refresh(board.assemble())
        payload = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')
        expected = board.HTML_HEAD + f'const ITEMS = {payload};\n' + board.HTML_TAIL
        self.assertEqual(board.OUT_HTML.read_text(), expected)


if __name__ == '__main__':
    unittest.main()
