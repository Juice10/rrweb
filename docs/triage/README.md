# Triage board

Build the self-contained page with Python 3, without network access:

```sh
python3 docs/triage/build_board.py
python3 docs/triage/test_board.py
node docs/triage/test_board.cjs
```

The generator retains the original September recommendations. The checked-in
`snapshot-2026-09-03.json` contains the metadata needed to reproduce those rows,
extracted from the published board at commit
`6a9b3f3e3dc2e6f24767bc952b557b08828cb9ec`. The original markdown report remains
unchanged.

`refresh-2026-10-23.json` records public upstream PR status and provisional notes
for the 19 newly listed open PRs. It reconciles the 138 original PRs with 140 open
PRs: 121 retained, 19 additions, 11 merged and 6 closed without merging.
It does not include PRs both opened and closed between snapshots.

Original recommendations, review tags and downstream evidence remain historical.
The 289 issue states and the original PRs' CI/reviews were not refreshed.
New PR checks refer to the recorded head SHA; `action_required` does not mean a
failed test. New priorities are not merge approval. Requested work in PostHog's
public tracker is distinguished from verified adoption.

Resolved PRs remain accessible in **Merged / closed** but are excluded from
active filters. **Done here** is still a separate browser-local meeting aid;
refreshing upstream state does not change saved selections. Additional refresh
context and check details use native, initially collapsed disclosure controls.

Open `docs/triage/index.html` in a browser to check filters, sorting, search,
Done/Undo and disclosure controls. No recorder or player runtime code is changed.
