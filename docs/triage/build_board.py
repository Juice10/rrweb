#!/usr/bin/env python3
"""Build the triage board from the historical snapshot and dated PR refresh."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_HTML = ROOT / "index.html"

MAINTAINERS = {
    "eoghanmurray": "Eoghan",
    "Juice10": "Justin",
    "YunFeng0817": "Yun",
}

TRIAGE_RANK = {
    "merge-now": 0,
    "adopt": 1,
    "review": 2,
    "discuss": 3,
    "cleanup": 4,
    "reject": 5,
    "bulk": 6,
}

TRIAGE_LABEL = {
    "merge-now": "Merge now",
    "adopt": "Adopt",
    "review": "Review individually",
    "discuss": "Discuss in team",
    "cleanup": "Request clean-up",
    "reject": "Reject",
    "bulk": "Bulk hygiene",
}

# Semantic overlay. Computed tags (who, draft, review state, GitHub labels)
# are added in assemble().
# Fields: triage, reason, notes, next, tags, downstream, related
PR = {}


def pr(
    number: int,
    triage: str,
    *,
    reason: str,
    next_step: str,
    notes: str = "",
    tags: tuple[str, ...] = (),
    downstream: str = "",
    related: tuple[int, ...] = (),
    message: str = "",
) -> None:
    PR[number] = {
        "triage": triage,
        "reason": reason,
        "notes": notes,
        "next": next_step,
        "tags": list(tags),
        "downstream": downstream,
        "related": list(related),
        "message": message,
    }


# --- Merge now --------------------------------------------------------------
pr(
    1712,
    "merge-now",
    reason="console.log → warn. Two-line change. Justin and Eoghan both APPROVED.",
    next_step="Merge now. Review gate is already clear.",
    notes="Still open only because nobody pressed the button.",
    tags=("approved", "posthog-backed"),
    downstream="In PostHog production. Their own two-line warn fix (posthog-js 3765).",
)
pr(
    1656,
    "merge-now",
    reason="Vitest 1.6.1 CVE pin. Justin APPROVED; Eoghan earlier dismissed. DIRTY vs current tree.",
    next_step="Decide today: merge if the pin is still the intent, otherwise close and rebump vitest in a new PR.",
    notes="Request-clean-up substance, but it is one of two already-approved PRs.",
    tags=("approved",),
    downstream="No PostHog signal.",
)

# --- Community adopt --------------------------------------------------------
pr(
    1921,
    "adopt",
    reason="ignoreAttribute tagName case. Tests + changeset. Fixes 1916.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review",),
    related=(1916,),
)
pr(
    1906,
    "adopt",
    reason="Regression tests only for CSS crash 1734/1692. Keep this; close 1735.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review",),
    related=(1734, 1692, 1735, 1920),
)
pr(
    1905,
    "adopt",
    reason="Omit iframe srcdoc on rebuild. Fixes a race and stops the browser parsing attacker HTML into the iframe. rrdom already omits srcdoc.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("strengthens-privacy", "waiting-on-review"),
    related=(1736,),
)
pr(
    1904,
    "adopt",
    reason="Console plugin this binding. Fixes Chrome extension crash 1772.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review",),
    related=(1772,),
)
pr(
    1903,
    "adopt",
    reason="repository.directory so npm README links resolve. Fixes 1738.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review",),
    related=(1738,),
)
pr(
    1856,
    "adopt",
    reason="Who's using rrweb? logos. Verify the two names, then merge.",
    next_step="Spot-check the two new names, then approve + merge.",
    tags=("waiting-on-review",),
)
pr(
    1771,
    "adopt",
    reason="autocomplete=off during replay so the reviewer's browser does not prompt-fill passwords.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("strengthens-privacy", "waiting-on-review", "posthog-backed"),
    downstream="In PostHog fork. High-trust heathdutton patch listed as PostHog-adjacent.",
    related=(1315,),
)
pr(
    1769,
    "adopt",
    reason="One-line: emit custom events when seeking. Fixes 1666.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review", "posthog-backed"),
    downstream="In PostHog fork. High-trust; they listed it as PostHog-adjacent.",
    related=(1666,),
)
pr(
    1737,
    "adopt",
    reason="image.currentSrc can be undefined. One-line guard.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review", "posthog-backed"),
    downstream="On PostHog planned batch-2 stability list. Never executed as a later port.",
)
pr(
    1802,
    "adopt",
    reason="querySelector as untainted methods.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("waiting-on-review", "posthog-backed"),
    downstream="Already in PostHog's vendored rrweb.",
)

# --- Maintainer adopt -------------------------------------------------------
pr(
    1673,
    "adopt",
    reason="Safer media play/pause. Pair with community 1688; close Justin 1462.",
    next_step="Eoghan: rebase, green CI, merge.",
    related=(1688, 1462, 1798),
)
pr(
    1891,
    "adopt",
    reason="master → main leftover refs. Mechanical.",
    next_step="Justin: merge.",
)
pr(
    1732,
    "adopt",
    reason="Long-term sponsor recognition.",
    next_step="Justin: merge.",
)
pr(
    1697,
    "adopt",
    reason="Video autoplay should not unfreeze the page. PostHog already runs this.",
    next_step="Eoghan: merge. Take their Set hoist. Guard checkoutEveryNth/Nms or document that those options still unfreeze.",
    notes="PostHog ignored the checkout hole because they do not use checkout.",
    tags=("posthog-backed", "posthog-shipped"),
    downstream="Shipped in posthog-js 4131 (near-verbatim plus a Set hoist). Checkout timers can still unfreeze.",
)

# --- PostHog-promoted community review → adopt ------------------------------
pr(
    1688,
    "adopt",
    reason="Invalid media processing. Pair with Eoghan 1673; close Justin 1462 and community 1798.",
    next_step="Approve + merge after rebase. Close 1462 and 1798 in the same pass.",
    tags=("posthog-backed",),
    downstream="Already in PostHog's fork. Mixpanel shipped the same MediaInteraction guard (their write-up cites 1798).",
    related=(1673, 1462, 1798),
)
pr(
    1691,
    "adopt",
    reason="Skip setAttribute when unchanged.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("posthog-backed",),
    downstream="Already in PostHog's fork. Grafana independently re-implemented the same skip-unchanged setAttribute in rrdom (grafana/rrweb 31).",
)
pr(
    1711,
    "adopt",
    reason="Inserting doctype.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("posthog-backed",),
    downstream="Already in PostHog's fork.",
)
pr(
    1770,
    "adopt",
    reason="Iframe cleanup in getUntaintedPrototype.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("posthog-backed",),
    downstream="Already in PostHog's fork.",
)
pr(
    1812,
    "adopt",
    reason="Always use native Proxy.",
    next_step="Approve + merge after rebase and green CI.",
    tags=("posthog-backed",),
    downstream="Next on PostHog batch-2 list after the July ports. Never executed as a later port; still in their fork.",
)
pr(
    1633,
    "adopt",
    reason="Untainted prototype access in Angular. Paul's own PR.",
    next_step="Nudge/merge. Already running in PostHog.",
    tags=("posthog-backed",),
    downstream="PostHog's own Angular untainted-prototype PR. Amplitude shipped a port; New Relic shipped a Safari-only variant of this PR.",
)
pr(
    1814,
    "adopt",
    reason="Untainted add/removeEventListener.",
    next_step="Nudge/merge. Already running in PostHog.",
    tags=("posthog-backed",),
    downstream="PostHog's own PR. In their fork.",
)

# --- Community review -------------------------------------------------------
pr(1920, "review", reason="Split _cssText on rule boundaries, not the middle of a rule. Related to 1692.", next_step="Assign one reviewer. Related to the CSS crash cluster; keep 1906 tests.", related=(1692, 1906))
pr(1917, "review", reason="adaptCssInTextMutations player option. Hover rewrite on style text mutations.", next_step="Assign one reviewer. Do not land together with 1897 and Eoghan 1480 — pick one hover approach.", notes="Hover / pseudo-class cluster.", related=(1897, 1480))
pr(1897, "review", reason="More pseudo-classes on rebuild. Replay quality buyers notice.", next_step="Assign one reviewer. Team still picks 1897 / 1917 / 1480.", tags=("commercial",), related=(1896, 1917, 1480))
pr(1796, "review", reason="Preserve class attribute text in hoverElements for [class=\"…\"] selectors.", next_step="Assign one reviewer.")
pr(1733, "review", reason="absolutifyURLs edge cases. DIRTY. Eoghan requested changes.", next_step="Author owes the perf/implementation fix. Do not re-review from scratch.", tags=("changes-requested",))
pr(1718, "review", reason="rrdom oldChild detach.", next_step="Assign one reviewer.")
pr(1681, "review", reason=":hover regex too large (1675). Tests exist; also listed under clean-up for a changeset.", next_step="Add changeset, then review. Fixes 1675.", related=(1675,))
pr(1641, "review", reason="Preserve adopted styles when nodes are removed (virtual DOM).", next_step="Assign one reviewer. PostHog listed this as a nudge, not a free merge. Amplitude already ships the full-snapshot half of this.", tags=("posthog-nudge",), downstream="PostHog wants tests. Amplitude shipped inline adoptedStyleSheets in the full snapshot (101) and has a mutation-add follow-up open (133).")
pr(1638, "review", reason="Parent missing during record/playback. Also listed under clean-up as untested.", next_step="Needs an explanation and tests before a real review.", related=())
pr(1635, "review", reason="Iframes + custom elements in Chrome.", next_step="Needs a browser regression test. PostHog nudge, not a free merge.", tags=("posthog-nudge",), downstream="On PostHog's own open-PR nudge list.")
pr(1586, "review", reason="Chrome grid-template inlining (1395).", next_step="Assign one reviewer. Amplitude independently wrote a grid-template-areas serializer for the same mobile-overlap hole.", related=(1395,), downstream="Amplitude rrweb 126 (unmerged) serializes grid-template-areas faithfully.")
pr(1357, "review", reason="Inserted styles lost when moving elements. Eoghan requested changes.", next_step="Author: isolate the fix; drop the innerText reflow cost.", tags=("changes-requested",))
pr(1814, "adopt", reason="Untainted add/removeEventListener.", next_step="Nudge/merge. Already running in PostHog.", tags=("posthog-backed",), downstream="PostHog's own PR. In their fork.")
pr(1755, "review", reason="Clear mutation buffer on iframe pagehide.", next_step="Review with 1791 as one iframe-lifecycle change. PostHog wants them folded together. Grafana already has a stop-path MutationBuffer reset open.", tags=("posthog-nudge",), downstream="PostHog: fold into a combined iframe-lifecycle PR with 1791. Grafana rrweb 32 resets mutationBuffers on stop.", related=(1791, 1770))
pr(1791, "review", reason="Iframe memory leaks. DIRTY. Related 1585/1628.", next_step="Review this branch, or fold with 1755. Mixpanel already shipped this PR plus a follow-up; Grafana has an independent IframeManager.reset(). Do not adopt from the PostHog fork — they solved it differently.", tags=("posthog-in-fork",), downstream="Mixpanel shipped this PR (mixpanel/rrweb 8 + 12). Grafana has the same leak class open. PostHog has it in-fork but solved the leak differently.", related=(1585, 1628, 1755, 1770))
pr(1356, "review", reason="Native setTimeout under zone.js. Justin requested changes.", next_step="Author owes the revision. Do not promote on PostHog's review — they declined.", tags=("changes-requested", "posthog-declined", "impacts-privacy"), downstream="PostHog declined: they have their own Zone path.")
pr(1463, "review", reason="Patched toString returns original. Detection-adjacent; still a correctness fix for apps that inspect native code.", next_step="Assign one reviewer. Weak stealth adjacency — read the privacy note.", tags=("impacts-privacy",), downstream="On PostHog planned batch-2 list; never executed.")
pr(1873, "review", reason="Native attributeFilter on MutationObserver. Can drop sensitive attribute mutations or drop the mutations masking depends on.", next_step="Privacy review required even though PostHog shipped a port. Fold in shadow bypassOptions + treat [] as unset.", tags=("impacts-privacy", "posthog-shipped"), downstream="Shipped posthog-js 4129. At port time: shadow roots were not filtered; empty [] observed no attributes. No later attributeFilter bugfix.")
pr(1373, "review", reason="Allow maskTextClass/blockClass: null to skip default class matching. Perf opt-out that disables a privacy default.", next_step="Privacy read required. Tiny and mergeable, but do not promote on PostHog's review — they declined.", tags=("impacts-privacy", "posthog-declined"), downstream="PostHog declined: unreachable under their hard-coded classes.")
pr(1726, "review", reason="emitFromIframe for nested iframes. More collection surface.", next_step="Assign one reviewer. Collection-surface change.", tags=("impacts-privacy",))
pr(1336, "review", reason="Packer compression level. Storage cost.", next_step="Assign one reviewer.", tags=("commercial",))
pr(1469, "review", reason="Wrap canvas bitmap errors in callbackWrapper.", next_step="Confirm it is still wanted; was on PostHog 3765 adopt-high. Needs tests or a cluster decision.", tags=("posthog-nudge",), downstream="On PostHog 3765 adopt-high; confirm still open and still wanted.")
pr(1907, "review", reason="Replay mutation DOMException / rrdom swallow.", next_step="Eoghan: review the replay cluster (1907, 1740, 1697, 1320, 1830, 1784, 1694).", related=(88,))
pr(1830, "review", reason="Canvas without recordCanvas must still affect layout. DIRTY.", next_step="Eoghan: review in the replay cluster.")
pr(1784, "review", reason="Strip postcss from record.js. Bundle-size win. Justin requested changes on Eoghan.", next_step="Maintainer-on-maintainer. Finish the thread.", tags=("commercial", "changes-requested"))
pr(1740, "review", reason="CDATA rebuild throw.", next_step="Eoghan: review in the replay cluster.")
pr(1694, "review", reason="Mutation emission throttle. Smaller than 1652.", next_step="Review independently. Do not promote on PostHog's review — they declined.", tags=("commercial", "posthog-declined"), downstream="PostHog declined: they already have SDK MutationThrottler; upstream wraps the same emit() checkout uses.")
pr(1320, "review", reason="500ms stylesheet timeout.", next_step="Eoghan: review in the replay cluster.")

# --- Discuss ----------------------------------------------------------------
pr(1914, "discuss", reason="Heatmap / click-track plugin. Extra semantic click payload (selector/text). PII in button labels.", next_step="Team meeting. Do not merge from the thread.", tags=("impacts-privacy", "commercial"))
pr(1900, "discuss", reason="Records alert/confirm/prompt. prompt() is often credentials or PII.", next_step="Team meeting. Completeness vs PII.", tags=("impacts-privacy", "commercial"))
pr(1909, "discuss", reason="Extension upload to api.rrweb.com with a stored bearer token. Data leaves the machine. Draft.", next_step="Team meeting with 1908. Close unless Cloud upload is a 2.x goal.", tags=("impacts-privacy", "commercial"), related=(1908,))
pr(1908, "discuss", reason="Chrome Web Store publish recovery. Pairs with 1909.", next_step="Team meeting with 1909.", tags=("commercial",), related=(1909,))
pr(1861, "discuss", reason="Cloud-bound sequence IDs / browser-client defaults.", next_step="Team meeting. Product + privacy defaults (maskAllInputs: true already in this repository).", tags=("impacts-privacy", "commercial"), related=(1848,))
pr(1848, "discuss", reason="Browser-client next release + assets. UNSTABLE draft.", next_step="Team meeting with 1475/1861. Do not land as-is.", tags=("impacts-privacy", "commercial"), related=(1475, 1861, 1239))
pr(1475, "discuss", reason="Asset events capture image/media bytes. Retention and PII-in-images. Successor to Justin 1239.", next_step="Team meeting. Close Justin draft 1239.", tags=("impacts-privacy", "commercial"), related=(1239, 1848, 860))
pr(1046, "discuss", reason="WebRTC streaming of <video>. Live biometric / meeting content. Draft, stale.", next_step="Close unless live video is a 2.x goal. Also a maintainer-close candidate.", tags=("impacts-privacy", "commercial", "maintainer-close"))
pr(1465, "discuss", reason="Parent forces a snapshot in a cross-origin iframe via postMessage. Eoghan requested changes.", next_step="Author + testcase needed. Security-origin discussion.", tags=("impacts-privacy", "changes-requested"))
pr(1023, "discuss", reason="Inject recorder from another frame / custom Window. Changes the security origin story.", next_step="Team meeting. Preferable to Eoghan 294 if this is needed at all.", tags=("impacts-privacy",), related=(294,))
pr(1739, "discuss", reason="Records attachShadow({mode:'closed'}). Closed shadow was an isolation boundary.", next_step="Team meeting. High replay-fidelity win, real privacy/ToS issue. Amplitude and Highlight both needed this in production.", tags=("impacts-privacy", "commercial"), downstream="Amplitude opened a closed-shadow mutation port (amplitude/rrweb 102, unmerged). Highlight has a Salesforce LWC / closed-shadow PR (highlight/rrweb 118).")
pr(1877, "discuss", reason="Changeset compress. Process, not product.", next_step="Agenda: process decision, not a code review.")
pr(1871, "discuss", reason="inlineStylesheet / inlineImages not deprecated. Ties to assets. Draft.", next_step="Discuss with the assets decision (1475).", tags=("impacts-privacy",), related=(1475,))
pr(1652, "discuss", reason="Large mutation-ordering refactor. Tests are good; blast radius is not a solo review.", next_step="Team meeting. Fold 1653/1300/1302 into this or land 1302 separately.", tags=("commercial",), related=(1653, 1300, 1302))
pr(1483, "discuss", reason="<link rel=stylesheet> + mutations. Collides with 1917/1897. Draft.", next_step="Team picks one hover/stylesheet approach.", related=(1917, 1897, 1480))
pr(1480, "discuss", reason="Hover rewrite via stylesheet mutation. Same collision. Draft.", next_step="Team picks 1897 / 1917 / 1480.", related=(1897, 1917, 1483))
pr(1015, "discuss", reason="Split monkeypatching into rrweb-init.js. Draft. Also a close-if-abandoned candidate.", next_step="Discuss isolation model, or close the stale draft.", tags=("impacts-privacy", "maintainer-close"))
pr(661, "discuss", reason="Rename rrweb-player → rrweb-playback-ui. 3.0.", next_step="Agenda for a 3.0 naming pass, not a drive-by merge.")
pr(1892, "discuss", reason="Plugin dependency metadata / host-neutral ReplayPlugin. DIRTY.", next_step="Team meeting. Plugin contract.")
pr(1874, "discuss", reason="Vite+ migration experiment. DIRTY draft. Close unless this is the 2.x tooling bet.", next_step="Decide yes/no. Maintainer-close candidate if not the tooling bet.", tags=("maintainer-close",))
pr(1843, "discuss", reason="yarn → pnpm. 158k-line lockfile.", next_step="Decide yes/no. Do not leave it open.")
pr(1839, "discuss", reason="Split snapshot utils. Codex-sized.", next_step="Team meeting. Scope / split.")
pr(1828, "discuss", reason="Next prerelease channel plan. Draft.", next_step="Team meeting with the 2.0 discussion.", tags=("commercial",), related=(1671, 1664))
pr(1800, "discuss", reason="allowedIframeOrigins allowlist. This is the security model to decide.", next_step="Agenda item. Prefer this over 1679 and 1256.", tags=("strengthens-privacy",), related=(1679, 1256, 1680))
pr(1642, "discuss", reason="blockElementFN whitelist/strict blocking. Enterprise control. Conflicts with privacy-at-capture selectors.", next_step="Discuss against the policy API. Do not land as a parallel knob.", tags=("strengthens-privacy", "commercial", "privacy-overlap"), related=(1644,))
pr(1257, "discuss", reason="Generic maskAttributesFn. Needed by PostHog-class vendors. Overlaps SENSITIVE_ATTRIBUTES / maskAttributeFn.", next_step="Do not land a second API if privacy-at-capture goes upstream.", tags=("strengthens-privacy", "commercial", "privacy-overlap"), related=(1581,))
pr(1164, "discuss", reason="Masks option/radio/checkbox values. Yun requested changes. Correct instinct; fold into the policy.", next_step="Author revision, then discuss as part of the masking API — not a one-off.", tags=("strengthens-privacy", "privacy-overlap", "changes-requested"))
pr(1097, "discuss", reason="Text-masking should apply to inputs; maskInputFn skipped on full snapshot.", next_step="Discuss with 874/1385/1488. Same hole, several reports.", tags=("strengthens-privacy", "privacy-overlap"), related=(874, 1385, 1488))
pr(1149, "discuss", reason="@rrweb/cutter + sync replayer. Huge, DIRTY, TODOs. Session clip is commercially real; this PR is not reviewable as-is.", next_step="Yun: split or close and re-file.", tags=("commercial",), related=(398, 160, 1560))

# --- Cleanup ----------------------------------------------------------------
pr(1912, "cleanup", reason="Masks placeholder when input masking is on. Real PII leak. This repository already treats placeholder as sensitive; upstream main does not.", next_step="Add changeset, rebase, then re-evaluate against privacy-at-capture. Do not land as a parallel knob.", tags=("strengthens-privacy", "privacy-overlap"), downstream="Mixpanel shipped this. New Relic opened the same mask-placeholder change (closed unmerged). Datadog hides placeholders in their own recorder.")
pr(1745, "cleanup", reason="maskAllInputs currently omits hidden. Tokens, CSRF, internal IDs leak. Fresher copy of 1610.", next_step="Add changeset and rebase. Close 1610. Re-evaluate against privacy-at-capture.", tags=("strengthens-privacy", "privacy-overlap"), related=(1610, 1609))
pr(1766, "cleanup", reason="Optional CSP on the replay iframe. Complements sandbox ADR.", next_step="Add tests, changeset, and a browser-support note. LaunchDarkly already ships a replayer CSP option (different API).", tags=("strengthens-privacy",), downstream="LaunchDarkly rrweb 36 shipped cspContent as a meta CSP on rebuild — same product need, not this PR’s iframe attribute.")
pr(1686, "cleanup", reason="stringifyRule fallback.", next_step="Needs a failing CSS-import test. PostHog nudge.", tags=("posthog-nudge",), downstream="On PostHog's own open-PR nudge list.")
pr(1313, "cleanup", reason="hookSetter recursion.", next_step="Add a reproduction. On PostHog planned batch-2; never executed.", downstream="PostHog batch-2 candidate; no later production write-up.")
pr(1879, "cleanup", reason="Svelte browser runtime. Likely superseded by merged 1901.", next_step="Confirm 1901 covered it, then close or rebase leftover.")
pr(1768, "cleanup", reason="Copilot timeout math. 27 files; needs a human to strip noise.", next_step="Try clean-up once, then reject if silent.")
pr(1748, "cleanup", reason="Broken docs links. DIRTY. One docs PR can replace 1748/1744/1709.", next_step="Close in favor of one new docs PR.", related=(1744, 1709))
pr(1744, "cleanup", reason="Docs guide wording. DIRTY. Fold into one docs PR.", next_step="Close in favor of one new docs PR.", related=(1748, 1709))
pr(1709, "cleanup", reason="Docs link rot. DIRTY. Fold into one docs PR.", next_step="Close in favor of one new docs PR.", related=(1748, 1744))
pr(1722, "cleanup", reason="REPL script “security.” Chinese-only, no tests.", next_step="Rewrite in English with tests, or close. Try clean-up once, then reject if silent.")
pr(1676, "cleanup", reason="Handle frames.", next_step="Labeled testcase needed.")
pr(1624, "cleanup", reason="Iframe parent workaround.", next_step="Needs a failing test.")
pr(1616, "cleanup", reason="Merge events. Draft. Needs design (see issue 1560).", next_step="Wait on the cutter/clip discussion.", related=(1560, 1149))
pr(1448, "cleanup", reason="Worker package for canvas/off-main-thread. Stale.", next_step="Rebase or extract the canvas-worker bugfix only.", tags=("commercial",))
pr(1439, "cleanup", reason="Smooth-scroll Y lag.", next_step="Needs a test.")
pr(1428, "cleanup", reason="Canvas inside iframe/shadow. More pixels. Best of the cluster.", next_step="Rebase. Close 1413 and 1235.", tags=("impacts-privacy",), related=(1413, 1235))
pr(1392, "cleanup", reason="Protocol URL regex. DIRTY, tiny.", next_step="Rebase the one-liner or close and re-file.")
pr(1212, "cleanup", reason="Custom mask selector / maskTextFn improvements. Stale, DIRTY.", next_step="Rebase onto the privacy discussion. Do not land as a parallel knob.", tags=("strengthens-privacy", "privacy-overlap"))
pr(815, "cleanup", reason="skipActivity on setConfig.", next_step="Testcase needed.")
pr(1302, "cleanup", reason="addList perf / addedSet order. Draft. 7-line fix PostHog already shipped.", next_step="Optional same-day: land this instead of waiting on 1652. Keep has→delete→add. Also take PostHog 4697 empty-payload reset (still missing in this tree).", tags=("posthog-shipped",), downstream="Shipped posthog-js 4130. They almost diverged to Set.delete; reverted to upstream has→delete→add. Later 4697: empty-payload early return skips addedSet/droppedSet reset — still present here.", related=(1652, 1300))
pr(1300, "cleanup", reason="addList perf sibling of 1302. Draft. Fold into 1652.", next_step="Fold into 1652 or close in favor of 1302.", related=(1652, 1302))
pr(1290, "cleanup", reason="rrvideo Chrome launch options.", next_step="Ask for rebase + why, or close.")
pr(960, "cleanup", reason="Custom event in checkout count. Draft, 4 lines, 2022.", next_step="Land the four lines or close as abandoned.")
pr(863, "cleanup", reason="Save/view snapshot scripts. Better as a recipe than a package dump.", next_step="Move to a recipe or close.")
pr(768, "cleanup", reason="Dynamic inline-style URLs. Eoghan requested changes. Very stale.", next_step="Author: rebase onto current transform utilities. Very stale — close if silent.", tags=("changes-requested",))
pr(1730, "cleanup", reason="rrdom-to-html trim. Rare CLEAN status; still needs a why.", next_step="Eoghan: add the why or close.")
pr(1653, "cleanup", reason="Micro perf. Fold into 1652 or drop.", next_step="Fold into 1652 or close.", related=(1652,))
pr(1534, "cleanup", reason="Export isBlocked. Lets hosts implement their own policy; easy to misuse. Draft.", next_step="Decide whether exporting the predicate is the API, then rebase.", tags=("impacts-privacy",))
pr(1466, "cleanup", reason="History-change tests only. Draft.", next_step="Land if they pass.")
pr(1322, "cleanup", reason="Failing CSS shorthand test. Draft.", next_step="Make it an issue, not a red PR.")
pr(1140, "cleanup", reason="Scrub-to-zero. Split unrelated pointer-event changes.", next_step="Split, then review.")
pr(1875, "cleanup", reason="Prefer minified CDN ESM. Docs. Eoghan requested changes on Justin.", next_step="Justin: address or close.", tags=("changes-requested",))
pr(1841, "cleanup", reason="Changelog backfill. DIRTY.", next_step="Rebase or close.")
pr(1811, "cleanup", reason="CI / changeset / fork-comment plumbing.", next_step="Squash with 1810/1809/1792/1789 into one hygiene PR.", related=(1810, 1809, 1792, 1789))
pr(1810, "cleanup", reason="CI / changeset plumbing.", next_step="Squash into one hygiene PR with 1811/1809/1792/1789.", related=(1811, 1809, 1792, 1789))
pr(1809, "cleanup", reason="Fork-comment plumbing.", next_step="Squash into one hygiene PR with 1811/1810/1792/1789.", related=(1811, 1810, 1792, 1789))
pr(1792, "cleanup", reason="Turbo outputs. Tiny, behind.", next_step="Squash into one hygiene PR.", related=(1811, 1810, 1809, 1789))
pr(1789, "cleanup", reason="tsconfig bundler. Tiny, behind.", next_step="Squash into one hygiene PR.", related=(1811, 1810, 1809, 1792))
pr(1790, "cleanup", reason="Privacy recipe docs. Author notes they were not verified.", next_step="Rewrite against the privacy-at-capture policy, then merge.", tags=("strengthens-privacy", "privacy-overlap"))

# --- Reject -----------------------------------------------------------------
pr(1610, "reject", reason="Exact older duplicate of 1745.", next_step="Close in favor of 1745. The hidden-input bug remains.", tags=("strengthens-privacy",), related=(1745, 1609), notes="Keep 1745.")
pr(1798, "reject", reason="Weaker duplicate of 1688.", next_step="Close in favor of 1688 + Eoghan 1673. Mixpanel already shipped this weaker variant.", related=(1688, 1673), downstream="Mixpanel rrweb 10 cites this PR as the upstream they shipped.")
pr(1735, "reject", reason="Crash already handled by merged 1580 / 1600. Keep regression-only 1906.", next_step="Close. Point at 1906 and split-point 1920.", related=(1906, 1920, 1734, 1692))
pr(1679, "reject", reason="Sender-origin is not validated; narrower than 1800.", next_step="Close in favor of the 1800 allowlist if that is the chosen model.", tags=("strengthens-privacy",), related=(1800, 1256, 1680))
pr(1256, "reject", reason="Earlier safeCrossOrigin sketch. Superseded by 1800.", next_step="Close in favor of 1800.", related=(1800, 1679))
pr(1413, "reject", reason="Superseded by 1428.", next_step="Close in favor of 1428.", tags=("posthog-in-fork",), downstream="In PostHog fork — do not adopt from that fact.", related=(1428, 1235))
pr(1235, "reject", reason="Superseded by 1428. Also mixes unrelated player changes.", next_step="Close in favor of 1428.", related=(1428, 1413))
pr(1259, "reject", reason="Dependabot against an ancient lockfile.", next_step="Close. Refresh in a new PR if the advisory still applies.")
pr(1255, "reject", reason="Dependabot against an ancient lockfile.", next_step="Close. Refresh in a new PR if the advisory still applies.")
pr(1238, "reject", reason="Dependabot against an ancient lockfile.", next_step="Close. Refresh in a new PR if the advisory still applies.")
pr(1416, "reject", reason="waiting-for-more-info, no author follow-up.", next_step="Close.")
pr(549, "reject", reason="No info since 2021.", next_step="Close as abandoned.")
pr(1477, "reject", reason="Stale pre-commit prettier. Close; re-file repo-wide if wanted.", next_step="Eoghan: close.", tags=("maintainer-close",))
pr(724, "reject", reason="__sn / iframe id; unreproducible, mirror replaced it.", next_step="Eoghan: close.", tags=("maintainer-close", "posthog-in-fork"), downstream="In PostHog fork — do not adopt from that fact. We already reject.")
pr(558, "reject", reason="Timestamp ordering; no reliable tests, later pipelines ate it.", next_step="Eoghan: close.", tags=("maintainer-close",), downstream="On PostHog planned batch-2; do not adopt. We already reject.")
pr(389, "reject", reason="Destructor against the old snapshot repo. Redesign if still needed.", next_step="Eoghan: close.", tags=("maintainer-close",))
pr(294, "reject", reason="window.top / window.top.document. Cross-frame privilege grab. Six years stale.", next_step="Eoghan: close.", tags=("maintainer-close", "impacts-privacy"))
pr(1462, "reject", reason="Media-target bug; superseded by Eoghan 1673 + community 1688.", next_step="Justin: close.", tags=("maintainer-close", "posthog-in-fork"), downstream="In PostHog fork — do not adopt from that fact.", related=(1673, 1688))
pr(1239, "reject", reason="Asset events v1. Eoghan already pointed review at 1475.", next_step="Justin: close in favor of Eoghan 1475.", tags=("maintainer-close", "impacts-privacy", "commercial", "changes-requested"), related=(1475,))


ISSUE: dict[int, dict] = {}


def issue(
    number: int,
    triage: str,
    *,
    reason: str,
    next_step: str,
    notes: str = "",
    tags: tuple[str, ...] = (),
    downstream: str = "",
    related: tuple[int, ...] = (),
    message: str = "",
) -> None:
    ISSUE[number] = {
        "triage": triage,
        "reason": reason,
        "notes": notes,
        "next": next_step,
        "tags": list(tags),
        "downstream": downstream,
        "related": list(related),
        "message": message,
    }


issue(1916, "adopt", reason="Fixed by PR 1921.", next_step="Merge PR 1921, then close.", related=(1921,))
issue(1772, "adopt", reason="Fixed by PR 1904.", next_step="Merge PR 1904, then close.", related=(1904,))
issue(1738, "adopt", reason="Fixed by PR 1903.", next_step="Merge PR 1903, then close.", related=(1903,))
issue(1736, "adopt", reason="Fixed by PR 1905.", next_step="Merge PR 1905, then close.", tags=("strengthens-privacy",), related=(1905,))
issue(1666, "adopt", reason="Fixed by PR 1769.", next_step="Merge PR 1769, then close.", related=(1769,))
issue(1609, "adopt", reason="Hidden-input leak. Merge 1745, not 1610.", next_step="Merge PR 1745 (not 1610), then close.", tags=("strengthens-privacy",), related=(1745, 1610))
issue(1315, "adopt", reason="Fixed by PR 1771.", next_step="Merge PR 1771, then close.", tags=("strengthens-privacy",), related=(1771,))
issue(1680, "adopt", reason="Cross-origin iframe origins. Land 1800, not 1679.", next_step="Land 1800’s allowlist after the security discussion, then close.", tags=("strengthens-privacy",), related=(1800, 1679))
issue(1675, "adopt", reason=":hover regex overflow. PR 1681.", next_step="Merge PR 1681 after changeset, then close.", related=(1681,))
issue(1734, "adopt", reason="CSS crash already handled by merged 1580/1600.", next_step="Close against merged 1580/1600; keep tests 1906 and split-point PR 1920.", related=(1692, 1906, 1920, 1735))
issue(1692, "adopt", reason="CSS crash already handled by merged 1580/1600.", next_step="Close against merged 1580/1600; keep tests 1906 and split-point PR 1920.", related=(1734, 1906, 1920, 1735))
issue(874, "adopt", reason="Has PR 1097. Same masking hole as 1385/1488.", next_step="Do not close until the masking discussion lands.", tags=("strengthens-privacy",), related=(1097, 1385, 1488))

issue(1919, "review", reason="Blocked <img> still pays the full inlineImages encode. Block is a privacy control; encoding the bytes anyway is a leak plus a perf bug.", next_step="Assign an owner. Privacy + commercial.", tags=("strengthens-privacy", "commercial"))
issue(1881, "review", reason="Canvas mutations in same-origin iframes.", next_step="Assign an owner.", tags=("impacts-privacy", "commercial"))
issue(1816, "review", reason="<select> wrong during forward play, right on seek.", next_step="Assign an owner. Repro-able replay bug.")
issue(1786, "review", reason="UMD global inconsistency.", next_step="Assign an owner.", tags=("commercial",))
issue(1785, "review", reason="Record bundle size.", next_step="Assign an owner.", tags=("commercial",), related=(1742,))
issue(1742, "review", reason="Record bundle size.", next_step="Assign an owner.", tags=("commercial",), related=(1785,))
issue(1724, "review", reason="Web-extension broken.", next_step="Assign an owner.", tags=("commercial",))
issue(1720, "review", reason="Cross-origin iframe blanks after parent fullSnapshot.", next_step="Assign an owner.")
issue(1707, "review", reason="Memory/CPU on rel=preload links.", next_step="Assign an owner. PostHog and Sprig already shipped a production fix for the endless preload-as-style poll.", downstream="PostHog posthog-js 3667 shipped. Sprig/UserLeap rrweb 2 cites this issue and that port.")
issue(1701, "review", reason="Popover API. Modern UI fidelity.", next_step="Assign an owner.", tags=("commercial",))
issue(1690, "review", reason="Mobile DOM order.", next_step="Assign an owner.")
issue(1667, "review", reason="background shorthand expands empty. Related CSSOM bugs.", next_step="Assign an owner.")
issue(1628, "review", reason="Stop-recording / iframe leaks. Pair with PR 1791/1770.", next_step="Pair with PR 1791/1770.", related=(1585, 1791, 1770))
issue(1585, "review", reason="Iframe leaks. Pair with PR 1791/1770.", next_step="Pair with PR 1791/1770.", related=(1628, 1791, 1770))
issue(1626, "review", reason="Adopted stylesheets missing from first full snapshot.", next_step="Assign an owner. Amplitude already ships the full-snapshot inline.", related=(1567,), downstream="Amplitude rrweb 101.")
issue(1567, "review", reason="Adopted stylesheets missing from first full snapshot.", next_step="Assign an owner. Amplitude already ships the full-snapshot inline.", related=(1626,), downstream="Amplitude rrweb 101.")
issue(1577, "review", reason="Duplicate cross-origin message listeners.", next_step="Assign an owner.", tags=("impacts-privacy",), related=(1590,))
issue(1590, "review", reason="Duplicate cross-origin message listeners.", next_step="Assign an owner.", tags=("impacts-privacy",), related=(1577,))
issue(1564, "review", reason="Table alignment in replay.", next_step="Assign an owner.")
issue(1505, "review", reason="all: unset expansion.", next_step="Assign an owner.")
issue(1488, "review", reason="maskInputFn skipped.", next_step="Same hole as 1097 / 1385.", tags=("strengthens-privacy",), related=(1097, 1385, 874))
issue(1385, "review", reason="maskInputFn skipped.", next_step="Same hole as 1097 / 1488.", tags=("strengthens-privacy",), related=(1097, 1488, 874))
issue(1395, "review", reason="Grid template areas. PR 1586.", next_step="Review PR 1586. Amplitude independently wrote a grid-template-areas serializer.", related=(1586,), downstream="Amplitude rrweb 126.")
issue(816, "review", reason="Strict CSP vs style mutation. 34 comments, still open.", next_step="Keep open. Security of the recorded app.", tags=("strengthens-privacy",))
issue(423, "review", reason="Inline/blob workers vs CSP.", next_step="Keep open with 1699.", tags=("strengthens-privacy",), related=(1699,))
issue(1699, "review", reason="Inline/blob workers vs CSP.", next_step="Keep open with 423.", tags=("strengthens-privacy",), related=(423,))
issue(88, "review", reason="removeChild DOMException. Ancient, 17 comments; may already be PR 1907.", next_step="Check whether PR 1907 covers it before closing.", related=(1907,))

issue(1918, "discuss", reason="inlineImages encodes full natural resolution with no cap. Retention cost and high-res PII.", next_step="Team meeting.", tags=("impacts-privacy", "commercial"))
issue(1913, "discuss", reason="UNSAFE_replayCanvas adds allow-scripts. Documented unsafe, still a footgun.", next_step="Answer with the sandbox ADR, then close or turn into implement-the-ADR.", tags=("impacts-privacy",), related=(1817,))
issue(1899, "discuss", reason="Replay pre-process plugins.", next_step="Team meeting.", tags=("commercial",))
issue(1896, "discuss", reason="More pseudo-classes. PR 1897.", next_step="Decide with PR 1897.", tags=("commercial",), related=(1897,))
issue(1880, "discuss", reason="Record a subtree only. Can strengthen privacy (less capture) and is commercially useful for widgets.", next_step="Team meeting with 1659 / 111.", tags=("impacts-privacy", "commercial"), related=(1659, 111))
issue(1659, "discuss", reason="Record a subtree only.", next_step="Team meeting with 1880 / 111.", tags=("impacts-privacy", "commercial"), related=(1880, 111))
issue(111, "discuss", reason="Record a subtree only.", next_step="Team meeting with 1880 / 1659.", tags=("impacts-privacy", "commercial"), related=(1880, 1659))
issue(1817, "discuss", reason="Rebuild may execute scripts. This repo already has the sandboxed-rebuild ADR.", next_step="Answer with the sandbox ADR.", tags=("impacts-privacy",), related=(1913,))
issue(1773, "discuss", reason="Remote control / MITM. Recommend reject, but confirm the product line.", next_step="Confirm out of scope, then close with 987.", tags=("commercial", "impacts-privacy"), related=(987,))
issue(987, "discuss", reason="Remote control / MITM. Recommend reject.", next_step="Confirm out of scope, then close with 1773.", tags=("commercial", "impacts-privacy"), related=(1773,))
issue(1671, "discuss", reason="When is 2.0? Trust and adoption.", next_step="Write one public status, then close 1664/1778/1420 as answered here.", tags=("commercial",), related=(1664, 1778, 1420))
issue(1664, "discuss", reason="2.0 schedule duplicate.", next_step="Close as answered in 1671.", tags=("commercial",), related=(1671,))
issue(1778, "discuss", reason="2.0 schedule duplicate.", next_step="Close as answered in 1671.", tags=("commercial",), related=(1671,))
issue(1420, "discuss", reason="2.0 schedule duplicate.", next_step="Close as answered in 1671.", tags=("commercial",), related=(1671,))
issue(1644, "discuss", reason="Fine-grained blocking. PR 1642.", next_step="Discuss with PR 1642 against the policy API.", tags=("strengthens-privacy", "commercial"), related=(1642,))
issue(1581, "discuss", reason="Mask attributes. PR 1257.", next_step="Discuss with PR 1257. Do not land a second API.", tags=("strengthens-privacy", "commercial"), related=(1257,))
issue(1563, "discuss", reason="maskAllText flag.", next_step="Fold into the privacy-at-capture discussion.", tags=("strengthens-privacy",))
issue(1560, "discuss", reason="Cut / merge / clip sessions.", next_step="Team meeting with Yun 1149 / 398 / 160.", tags=("commercial",), related=(1149, 398, 160))
issue(398, "discuss", reason="Session cutter / clip.", next_step="Team meeting with 1149 / 1560 / 160.", tags=("commercial",), related=(1149, 1560, 160))
issue(160, "discuss", reason="Session cutter / clip.", next_step="Team meeting with 1149 / 1560 / 398.", tags=("commercial",), related=(1149, 1560, 398))
issue(1528, "discuss", reason="Sanitization vs sandbox. Same debate as the ADR.", next_step="Answer with the sandbox ADR.", tags=("impacts-privacy",))
issue(1491, "discuss", reason="CSS animation currentTime.", next_step="Team meeting.", tags=("commercial",))
issue(1337, "discuss", reason="Full snapshot perf.", next_step="Team meeting. Related to 1694 / 1547.", tags=("commercial",), related=(1694, 1547))
issue(1547, "discuss", reason="Snapshot / mutation perf. Related to PR 1694.", next_step="Review with PR 1694.", tags=("commercial",), related=(1694, 1337))
issue(1143, "discuss", reason="Web Animations API.", next_step="Team meeting.", tags=("commercial",))
issue(419, "discuss", reason="rrdom as an analytics engine. Strategic, not a bug.", next_step="Keep until the matching discussion happens.", tags=("commercial",))
issue(860, "discuss", reason="Deferred / asset events. The assets PRs.", next_step="Discuss with 1475 / 1848.", tags=("impacts-privacy", "commercial"), related=(1475, 1848))

CLEANUP_ISSUES = {
    1824, 1727, 1713, 1650, 1608, 1595, 1558, 1514, 1473, 1232, 1192, 1075, 951, 377, 1658, 1622, 1723,
}
for n in CLEANUP_ISSUES:
    extra = {
        1658: "Extension “obfuscated code” complaint — ask for the exact file/build.",
        1622: "Turbo on M1.",
        1723: "pauseAnimation docs question.",
    }.get(n, "Need a reproduction, English summary, or a reduced test case.")
    issue(n, "cleanup", reason=extra, next_step="Use the issue template; close after 14 days of silence. Label reproduction needed.")

issue(1878, "reject", reason="Captcha/stealth evasion is out of scope and hostile to end users.", next_step="Close. Do not help hide recording from the page or from the user.", tags=("impacts-privacy",))
issue(1801, "reject", reason="WeChat mini programs / React Native are not DOM.", next_step="Close as out of scope.")
issue(1606, "reject", reason="Recording JS execution is a profiler, not rrweb.", next_step="Close as out of scope.")
issue(1048, "reject", reason="IE11.", next_step="Close.")


TAG_LABEL = {
    "approved": "Approved",
    "waiting-on-review": "Waiting on review",
    "changes-requested": "Changes requested",
    "strengthens-privacy": "Strengthens privacy",
    "impacts-privacy": "Impacts privacy",
    "commercial": "Commercial",
    "posthog-backed": "PostHog-backed",
    "posthog-shipped": "PostHog shipped",
    "posthog-declined": "PostHog declined",
    "posthog-in-fork": "In PostHog fork — do not adopt",
    "posthog-nudge": "PostHog nudge",
    "sentry-backed": "Sentry-backed",
    "datadog-diverged": "Datadog diverged",
    "newrelic-backed": "New Relic-backed",
    "amplitude-backed": "Amplitude-backed",
    "mixpanel-backed": "Mixpanel-backed",
    "grafana-backed": "Grafana-backed",
    "sprig-backed": "Sprig-backed",
    "launchdarkly-backed": "LaunchDarkly-backed",
    "highlight-backed": "Highlight-backed",
    "privacy-overlap": "Privacy-at-capture overlap",
    "maintainer-close": "Maintainer close",
    "draft": "Draft",
    "maintainer": "Maintainer",
    "community": "Community",
    "bulk-updated": "Bulk-updated 2026-06-08",
}

TAG_RANK = {
    "approved": 0,
    "posthog-backed": 1,
    "posthog-shipped": 2,
    "strengthens-privacy": 3,
    "impacts-privacy": 4,
    "privacy-overlap": 5,
    "waiting-on-review": 6,
    "changes-requested": 7,
    "maintainer-close": 8,
    "commercial": 9,
    "posthog-declined": 10,
    "posthog-in-fork": 11,
    "posthog-nudge": 12,
    "mixpanel-backed": 12.1,
    "amplitude-backed": 12.2,
    "newrelic-backed": 12.3,
    "grafana-backed": 12.4,
    "sprig-backed": 12.5,
    "launchdarkly-backed": 12.6,
    "highlight-backed": 12.7,
    "sentry-backed": 12.8,
    "datadog-diverged": 12.9,
    "draft": 13,
    "maintainer": 14,
    "community": 15,
    "bulk-updated": 16,
}


def ev(label: str, url: str, note: str = "") -> dict:
    return {"label": label, "url": url, "note": note}


PH = "https://github.com/PostHog/posthog-js"
MX = "https://github.com/mixpanel/rrweb"
AMP = "https://github.com/amplitude/rrweb"
NR = "https://github.com/newrelic-forks/rrweb"
DD = "https://github.com/DataDog/browser-sdk"
GF = "https://github.com/grafana/rrweb"
LD = "https://github.com/launchdarkly/rrweb"
UL = "https://github.com/UserLeap/rrweb"
HL = "https://github.com/highlight/rrweb"

PH_TRACKER = ev(
    "PostHog/posthog-js#3765",
    f"{PH}/issues/3765",
    "Their public pull-in tracker. Evidence is the row for this upstream PR.",
)
PH_ALREADY = ev(
    "PostHog/posthog-js#3765",
    f"{PH}/issues/3765",
    "Listed as already in their vendored rrweb (verified by them, not re-verified here).",
)
PH_ADOPT = ev(
    "PostHog/posthog-js#3765",
    f"{PH}/issues/3765",
    "On their adopt / adopt-high list. Not treated as shipped unless a port PR is linked.",
)
PH_DECLINE = ev(
    "PostHog/posthog-js#3765",
    f"{PH}/issues/3765",
    "They explicitly declined to adopt this from that review.",
)
PH_NUDGE = ev(
    "PostHog/posthog-js#3765",
    f"{PH}/issues/3765",
    "On their own-open / nudge list — needs tests or a cluster decision.",
)

# Links to the vendor PR/issue that provides the evidence. Only rows we
# actually opened. Datadog is an in-tree fork that has diverged.
EVIDENCE: dict[int, list[dict]] = {
    1712: [ev("PostHog/posthog-js#3765", f"{PH}/issues/3765", "Their own two-line warn fix; listed as already in the fork / APPROVED upstream.")],
    1771: [PH_ADOPT],
    1769: [PH_ADOPT],
    1737: [PH_ADOPT],
    1802: [PH_ALREADY],
    1688: [
        PH_ALREADY,
        ev("mixpanel/rrweb#10", f"{MX}/pull/10", "Shipped the MediaInteraction isSupportedMediaElement guard. Their write-up cites the weaker duplicate 1798, not this PR."),
    ],
    1691: [
        PH_ALREADY,
        ev("grafana/rrweb#31", f"{GF}/pull/31", "Independent re-implementation of skip-unchanged setAttribute in rrdom diffProps (plus SVG NS + iframe src coverage). Open on their fork."),
    ],
    1711: [PH_ALREADY],
    1770: [PH_ALREADY],
    1812: [PH_ADOPT],
    1633: [
        PH_ALREADY,
        ev("amplitude/rrweb#61", f"{AMP}/pull/61", "Shipped better Angular zone / unpatched-prototype detection."),
        ev("newrelic-forks/rrweb#8", f"{NR}/pull/8", "Shipped a Safari-only port of this PR (Chrome froze their Angular app when they took the full patch)."),
    ],
    1814: [PH_ADOPT],
    1697: [ev("PostHog/posthog-js#4131", f"{PH}/pull/4131", "Shipped adopt of this PR (plus a Set hoist). Checkout timers can still unfreeze.")],
    1873: [ev("PostHog/posthog-js#4129", f"{PH}/pull/4129", "Shipped adopt. At port time: shadow roots were not filtered; empty [] observed no attributes.")],
    1302: [
        ev("PostHog/posthog-js#4130", f"{PH}/pull/4130", "Shipped adopt. They kept has→delete→add."),
        ev("PostHog/posthog-js#4697", f"{PH}/pull/4697", "Empty-payload early return skips addedSet reset — still missing in this tree."),
    ],
    1673: [PH_ADOPT],
    1745: [
        PH_ADOPT,
        ev("mixpanel/rrweb#4", f"{MX}/pull/4", "Re-implemented hidden-input masking (maskInputOptions.hidden)."),
    ],
    1610: [
        PH_TRACKER,
        ev("mixpanel/rrweb#4", f"{MX}/pull/4", "They shipped a hidden-input fix. Close this duplicate; keep 1745."),
    ],
    1912: [
        ev("mixpanel/rrweb#18", f"{MX}/pull/18", "Shipped placeholder masking when input masking is on."),
        ev("newrelic-forks/rrweb#19", f"{NR}/pull/19", "Same product: mask placeholder via maskInputValue. Closed unmerged on their fork."),
        ev("DataDog/browser-sdk#1660", f"{DD}/pull/1660", "Datadog hides placeholders under mask privacy in their own recorder — not a port of this PR."),
    ],
    1798: [
        ev("mixpanel/rrweb#10", f"{MX}/pull/10", "They shipped this weaker duplicate and cited it as the upstream. Prefer 1688 + 1673."),
    ],
    1791: [
        PH_ALREADY,
        ev("mixpanel/rrweb#8", f"{MX}/pull/8", "Explicit port of this PR. Shipped iframe teardown + removeNodeFromMapPermanently."),
        ev("mixpanel/rrweb#12", f"{MX}/pull/12", "Follow-up: recurse iframe contentDocument children so the mirror does not pin GC."),
        ev("grafana/rrweb#41", f"{GF}/pull/41", "Same leak class: IframeManager.reset() on stop. Independent, still open on their fork."),
    ],
    1755: [
        PH_NUDGE,
        ev("grafana/rrweb#32", f"{GF}/pull/32", "Same stop-path: reset all MutationBuffer collections and empty the mutationBuffers registry. Open on their fork."),
    ],
    1739: [
        ev("amplitude/rrweb#102", f"{AMP}/pull/102", "Closed-mode shadow mutation capture (patchAttachShadow used element.shadowRoot which is null for closed roots). Open, not merged."),
        ev("highlight/rrweb#118", f"{HL}/pull/118", "Salesforce LWC / closed shadow recording. Same product need, not a port of this PR."),
    ],
    1586: [
        ev("amplitude/rrweb#126", f"{AMP}/pull/126", "Serialize grid-template-areas faithfully (mobile replay overlap). Same Chrome grid-template hole. Open, not merged."),
    ],
    1641: [
        PH_NUDGE,
        ev("amplitude/rrweb#101", f"{AMP}/pull/101", "Shipped inline adoptedStyleSheets in the full snapshot so dropped incremental style events cannot leave shadow CSS empty."),
        ev("amplitude/rrweb#133", f"{AMP}/pull/133", "Follow-up: inline adoptedStyleSheets on mutation add as well. Open."),
    ],
    1766: [
        ev("launchdarkly/rrweb#36", f"{LD}/pull/36", "Shipped optional replayer CSP (cspContent → meta http-equiv). Same product need, different API than this PR’s iframe CSP."),
    ],
    1707: [
        ev("PostHog/posthog-js#3667", f"{PH}/pull/3667", "Shipped: stop polling preload-as-style <link> forever (Next.js chunked CSS)."),
        ev("UserLeap/rrweb#2", f"{UL}/pull/2", "Sprig/UserLeap shipped the same preload event-listener leak fix; their write-up cites this issue and PostHog 3667."),
    ],
    1395: [
        ev("amplitude/rrweb#126", f"{AMP}/pull/126", "Amplitude’s grid-template-areas serializer. Review with PR 1586."),
    ],
    1626: [
        ev("amplitude/rrweb#101", f"{AMP}/pull/101", "Shipped inline adoptedStyleSheets in the full snapshot."),
    ],
    1567: [
        ev("amplitude/rrweb#101", f"{AMP}/pull/101", "Shipped inline adoptedStyleSheets in the full snapshot."),
    ],
    1800: [ev("mixpanel/rrweb#9", f"{MX}/pull/9", "Their public fork has allowedIframeOrigins (own cross-origin port).")],
    1609: [
        ev("mixpanel/rrweb#4", f"{MX}/pull/4", "Re-implemented hidden-input masking."),
        ev("PostHog/posthog-js#3765", f"{PH}/issues/3765", "They list upstream 1745, not 1610."),
    ],
    1680: [ev("mixpanel/rrweb#9", f"{MX}/pull/9", "Mixpanel already ships an iframe-origin allowlist in their fork.")],
    1469: [PH_ADOPT],
    1635: [PH_NUDGE],
    1642: [PH_ADOPT],
    1686: [PH_NUDGE],
    1164: [PH_ADOPT],
    1097: [PH_ADOPT],
    1257: [PH_ADOPT],
    1356: [PH_DECLINE],
    1373: [PH_DECLINE],
    1694: [PH_DECLINE],
    1313: [PH_ADOPT],
    1463: [PH_ADOPT],
    1428: [PH_ADOPT],
    1413: [PH_ALREADY],
    1462: [PH_ALREADY],
    724: [PH_ALREADY],
    558: [PH_ADOPT],
    1320: [PH_ADOPT],
    1854: [
        ev("PostHog/posthog-js#4128", f"{PH}/pull/4128", "Shipped adopt. Already on upstream main."),
        ev("PostHog/posthog-js#4325", f"{PH}/pull/4325", "Later widened Safari keepalive to WebKit."),
    ],
}

EVIDENCE_TAGS: dict[int, tuple[str, ...]] = {
    1912: ("mixpanel-backed", "newrelic-backed"),
    1745: ("mixpanel-backed",),
    1610: ("mixpanel-backed",),
    1800: ("mixpanel-backed",),
    1609: ("mixpanel-backed",),
    1680: ("mixpanel-backed",),
    1688: ("mixpanel-backed",),
    1798: ("mixpanel-backed",),
    1791: ("mixpanel-backed", "grafana-backed"),
    1633: ("amplitude-backed", "newrelic-backed"),
    1691: ("grafana-backed",),
    1755: ("grafana-backed",),
    1739: ("amplitude-backed", "highlight-backed"),
    1586: ("amplitude-backed",),
    1395: ("amplitude-backed",),
    1641: ("amplitude-backed",),
    1626: ("amplitude-backed",),
    1567: ("amplitude-backed",),
    1766: ("launchdarkly-backed",),
    1707: ("sprig-backed", "posthog-shipped"),
}


def load_json(path: Path):
    return json.loads(path.read_text())


def who_of(login: str) -> tuple[str, str]:
    if login in MAINTAINERS:
        return "maintainer", MAINTAINERS[login]
    return "community", "Community"


def _sentence(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return text if text.endswith((".", "!", "?")) else text + "."


def _keep_ref(related: list) -> str | None:
    return f"#{related[0]}" if related else None


def _close_footer(kind: str) -> str:
    if kind == "pr":
        return (
            "If this is still relevant, please open a new PR against current `main` "
            "with a rebase, a changeset, and a regression test. We’re closing stale "
            "work so intake can restart."
        )
    return (
        "If this is still relevant, please open a new issue with a reduced "
        "reproduction on a current release. We’re closing stale work so intake "
        "can restart."
    )


def compose_message(kind: str, overlay: dict, who: str) -> str:
    if overlay.get("message"):
        return overlay["message"]
    triage = overlay["triage"]
    reason = _sentence(overlay.get("reason") or "")
    next_step = _sentence(overlay.get("next") or "")
    related = overlay.get("related") or []
    tags = overlay.get("tags") or []
    keep = _keep_ref(related)
    noun = "pull request" if kind == "pr" else "issue"

    if triage == "reject":
        if keep:
            return (
                f"Closing in favor of {keep}, which covers the same ground. "
                "Please move any extra test cases there.\n\n"
                f"{reason}\n\n{_close_footer(kind)}"
            )
        lowered = reason.lower()
        if any(
            token in lowered
            for token in (
                "out of scope",
                "stealth",
                "captcha",
                "mitm",
                "remote control",
                "wechat",
                "profiler",
            )
        ):
            return (
                "rrweb records and replays the DOM. Remote control, captcha evasion, "
                "and host-app MITM are out of scope for this repo. Please don’t "
                f"re-open that class of request.\n\n{reason}"
            )
        if who == "maintainer":
            return (
                f"Closing this stale {noun} as part of intake cleanup.\n\n"
                f"{reason}\n\n{_close_footer(kind)}"
            )
        return (
            f"Closing this {noun} as part of intake cleanup.\n\n"
            f"{reason}\n\n{_close_footer(kind)}"
        )

    if triage == "cleanup":
        if kind == "issue":
            return (
                "Thanks for filing this. We need a reduced reproduction, an English "
                "summary, or a failing fixture before we can spend review time on it. "
                "If that doesn’t happen in two weeks we’ll close it; open a new issue "
                f"if this is still relevant.\n\n{reason}"
            )
        if who == "maintainer":
            return (
                "This still needs a rebase / tests / split before review is worth "
                "the time. If it stays stale we should close it and open a new PR "
                f"against current `main` if it is still relevant.\n\n{reason}\n\n{next_step}"
            ).strip()
        return (
            "Thanks for this — the direction looks useful. Before we can review it on "
            "current `main`, please rebase, add a changeset, and add a regression test "
            "for the reported case. If that doesn’t happen in two weeks we’ll close "
            "it; open a new PR if this is still relevant.\n\n"
            f"{reason}"
        )

    if triage == "review":
        if "changes-requested" in tags:
            return (
                "A maintainer already reviewed this. Please address the requested "
                "changes and we’ll pick it back up — no need to re-review from "
                f"scratch.\n\n{reason}"
            )
        if kind == "issue":
            return (
                "This looks like a real bug or a small, well-scoped feature. "
                f"Putting it in the individual-review queue.\n\n{reason}\n\n{next_step}"
            ).strip()
        return (
            "Could someone from core take a look at this? It’s a focused change, "
            f"not a product-strategy fork.\n\n{reason}\n\n{next_step}"
        ).strip()

    if triage == "discuss":
        return (
            "Holding this for a team discussion rather than merging or closing from "
            f"the thread.\n\n{reason}"
        )

    if triage == "merge-now":
        return f"Review is already done. Merging this onto current `main`.\n\n{reason}"

    if triage == "adopt":
        extra = f" Related: {', '.join(f'#{n}' for n in related)}." if related else ""
        if kind == "issue":
            return (
                f"This has a known fix in the adopt queue.{extra}\n\n{reason}\n\n{next_step}"
            ).strip()
        return (
            "This looks small and correct enough to adopt after rebase + green CI. "
            f"Approving.\n\n{reason}{extra}"
        )

    return (
        "Closing as part of intake cleanup. This was not individually reviewed "
        "in the first pass: questions go to the guide, 2.0 duplicates to 1671, "
        "privacy duplicates to the policy comment, and reports without a reduced "
        f"fixture need a reproduction.\n\n{reason}\n\n{_close_footer(kind)}"
    )


def assemble() -> list[dict]:
    snapshot = load_json(ROOT / "snapshot-2026-09-03.json")
    prs = snapshot["pr"]
    issues = snapshot["issue"]
    items: list[dict] = []
    missing_prs = []

    for raw in prs:
        n = raw["number"]
        overlay = PR.get(n)
        if overlay is None:
            missing_prs.append(n)
            overlay = {
                "triage": "review",
                "reason": "Open at snapshot; not given a dedicated row in the first-pass tables.",
                "notes": "",
                "next": "Skim title and files; then bucket.",
                "tags": [],
                "downstream": "",
                "related": [],
                "message": "",
            }
        login = (raw.get("author") or {}).get("login") or "unknown"
        who_kind, who_label = who_of(login)
        tags = list(overlay["tags"])
        if who_kind == "maintainer":
            tags.append("maintainer")
        else:
            tags.append("community")
        if raw.get("isDraft"):
            tags.append("draft")
        decision = raw.get("reviewDecision") or ""
        if decision == "APPROVED":
            tags.append("approved")
        elif decision == "CHANGES_REQUESTED":
            tags.append("changes-requested")
        elif not raw.get("isDraft") and decision in ("REVIEW_REQUIRED", ""):
            tags.append("waiting-on-review")
        if (raw.get("updatedAt") or "").startswith("2026-06-08"):
            tags.append("bulk-updated")
        for lab in raw.get("labels") or []:
            name = lab if isinstance(lab, str) else lab.get("name")
            if name and name not in tags:
                tags.append(name)
        for t in EVIDENCE_TAGS.get(n, ()):
            tags.append(t)
        # de-dupe preserving order
        seen = set()
        uniq = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                uniq.append(t)
        items.append(
            {
                "id": n,
                "kind": "pr",
                "title": raw["title"],
                "url": raw.get("url") or f"https://github.com/rrweb-io/rrweb/pull/{n}",
                "author": login,
                "authorName": (raw.get("author") or {}).get("name") or login,
                "createdAt": raw["createdAt"],
                "updatedAt": raw["updatedAt"],
                "draft": bool(raw.get("isDraft")),
                "reviewDecision": decision or "NONE",
                "who": who_kind,
                "whoLabel": who_label,
                "triage": overlay["triage"],
                "tags": uniq,
                "next": overlay["next"],
                "reason": overlay["reason"],
                "notes": overlay["notes"],
                "downstream": overlay["downstream"],
                "downstreamLinks": EVIDENCE.get(n, []),
                "related": overlay["related"],
                "message": compose_message("pr", overlay, who_kind),
                "additions": raw.get("additions"),
                "deletions": raw.get("deletions"),
                "changedFiles": raw.get("changedFiles"),
                "mergeable": raw.get("mergeable"),
            }
        )

    if missing_prs:
        raise SystemExit(f"Missing PR overlay for: {missing_prs}")

    for raw in issues:
        n = raw["number"]
        overlay = ISSUE.get(n)
        if overlay is None:
            overlay = {
                "triage": "bulk",
                "reason": "Not individually reviewed in the first pass (~180 issues).",
                "notes": "Bulk rule: questions → guide; 2.0 dupes → 1671; privacy dupes → policy comment; Chinese-only with no fixture → ask for a reduced case.",
                "next": "Apply bulk hygiene. Do not spend a review slot unless a repro appears.",
                "tags": [],
                "downstream": "",
                "related": [],
                "message": "",
            }
        login = (raw.get("author") or {}).get("login") or "unknown"
        who_kind, who_label = who_of(login)
        tags = list(overlay["tags"])
        tags.append("maintainer" if who_kind == "maintainer" else "community")
        if (raw.get("updatedAt") or "").startswith("2026-06-08"):
            tags.append("bulk-updated")
        for lab in raw.get("labels") or []:
            name = lab if isinstance(lab, str) else lab.get("name")
            if name and name not in tags:
                tags.append(name)
        for t in EVIDENCE_TAGS.get(n, ()):
            tags.append(t)
        seen = set()
        uniq = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                uniq.append(t)
        items.append(
            {
                "id": n,
                "kind": "issue",
                "title": raw["title"],
                "url": raw.get("url") or f"https://github.com/rrweb-io/rrweb/issues/{n}",
                "author": login,
                "authorName": (raw.get("author") or {}).get("name") or login,
                "createdAt": raw["createdAt"],
                "updatedAt": raw["updatedAt"],
                "draft": False,
                "reviewDecision": "",
                "who": who_kind,
                "whoLabel": who_label,
                "triage": overlay["triage"],
                "tags": uniq,
                "next": overlay["next"],
                "reason": overlay["reason"],
                "notes": overlay["notes"],
                "downstream": overlay["downstream"],
                "downstreamLinks": EVIDENCE.get(n, []),
                "related": overlay["related"],
                "message": compose_message("issue", overlay, who_kind),
                "additions": None,
                "deletions": None,
                "changedFiles": None,
                "mergeable": None,
            }
        )

    items.sort(key=lambda x: (0 if x["kind"] == "pr" else 1, -x["id"]))
    return items


def apply_refresh(items: list[dict]) -> list[dict]:
    refresh = load_json(ROOT / "refresh-2026-10-23.json")
    current = {p["number"]: p for p in refresh["open"]}
    resolved = {p["number"]: p for p in refresh["resolved"]}
    original_ids = {p["id"] for p in items if p["kind"] == "pr"}
    new_ids = {p["id"] for p in refresh["new"]}
    if original_ids - current.keys() != resolved.keys():
        raise ValueError("Every original PR must be open or explicitly resolved")
    if current.keys() - original_ids != new_ids or new_ids & original_ids:
        raise ValueError("New PRs must exactly match additions to the open queue")
    for item in items:
        item["historical"] = True
        if item["kind"] != "pr":
            item["upstreamState"] = "Issue status not refreshed"
            continue
        n = item["id"]
        if n in current:
            raw = current[n]
            item.update(title=raw["title"], draft=raw["draft"], updatedAt=raw["updated_at"], upstreamState="Open")
        else:
            raw = resolved[n]
            item["upstreamState"] = "Merged" if raw["merged"] else "Closed unmerged"
            item["resolvedAt"] = raw["merged_at"] or raw["closed_at"]
    for raw in refresh["new"]:
        who, label = who_of(raw["author"])
        tags = ["new", "maintainer" if who == "maintainer" else "community"]
        if raw["draft"]:
            tags.append("draft")
        if raw["id"] in (1964, 1965):
            tags.append("strengthens-privacy")
        item = dict(
            id=raw["id"], kind="pr", title=raw["title"], url=raw["url"],
            author=raw["author"], authorName=raw["author"], who=who, whoLabel=label,
            createdAt=raw["created"], updatedAt=raw["updated"], draft=raw["draft"],
            reviewDecision="Not a merge approval", triage="review", tags=tags,
            reason=raw["reason"], next="Obtain maintainer review and verify current head checks.",
            notes="Provisional review priority: " + raw["bucket"], downstream="",
            downstreamLinks=[], related=[], message="", historical=False,
            upstreamState="Open", refresh=raw,
        )
        if raw["id"] in (1933, 1934):
            item["downstream"] = "Requested by PostHog; adoption is not verified."
            item["downstreamLinks"] = [ev("PostHog requested-work tracker", "https://github.com/PostHog/posthog-js/issues/3766")]
        items.append(item)
    items.sort(key=lambda x: (0 if x["kind"] == "pr" else 1, -x["id"]))
    return items


HTML_HEAD = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>rrweb intake triage · 2026-10-23 refresh</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
  :root {
    --bg: #12140f;
    --bg-2: #1b1e16;
    --bg-3: #23281c;
    --ink: #f3efe2;
    --muted: #9a937c;
    --line: #3a3f2f;
    --accent: #d4a017;
    --accent-2: #7eb8a0;
    --merge: #d4a017;
    --adopt: #7eb8a0;
    --review: #8aa4d4;
    --discuss: #c48bdb;
    --cleanup: #d4b07a;
    --reject: #d37a6a;
    --bulk: #7a7668;
    --chip: #2a2e22;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--ink);
    font: 14px/1.45 "IBM Plex Sans", "Source Sans 3", "Segoe UI", sans-serif; }
  a { color: #e8c56a; }
  a:hover { color: #ffe08a; }
  header.page {
    padding: 22px 28px 10px;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, #191c13 0%, var(--bg) 100%);
    position: sticky; top: 0; z-index: 20;
  }
  h1 { font-size: 22px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 6px; }
  .lede { color: var(--muted); margin: 0 0 10px; }
  .prefilters { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 12px; }
  .prefilters button {
    appearance: none; border: 1px solid var(--line); background: var(--bg-2);
    color: var(--ink); padding: 7px 12px; border-radius: 999px; cursor: pointer;
    font: inherit; display: inline-flex; align-items: center; gap: 8px;
  }
  .prefilters button .n { background: var(--chip); color: var(--muted); padding: 1px 7px;
    border-radius: 999px; font-size: 12px; }
  .prefilters button.active { border-color: var(--accent); background: #2a2410; color: #ffe08a; }
  .prefilters button[data-filter="merge-now"].active { box-shadow: inset 0 0 0 1px var(--merge); }
  .toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 8px; }
  .toolbar label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }
  select, input[type="search"] {
    background: var(--bg-2); color: var(--ink); border: 1px solid var(--line);
    border-radius: 8px; padding: 6px 10px; font: inherit;
  }
  input[type="search"] { min-width: 220px; }
  .sorts { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
  .sorts button {
    appearance: none; border: 1px solid var(--line); background: var(--bg-3);
    color: var(--ink); padding: 5px 10px; border-radius: 6px; cursor: pointer; font: inherit;
  }
  .sorts button.active { border-color: var(--accent-2); color: var(--accent-2); }
  .meta { color: var(--muted); font-size: 12px; margin: 4px 0 0; display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; }
  .meta-actions { display: inline-flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .meta-actions label { text-transform: none; letter-spacing: 0; font-size: 12px; color: var(--muted); display: inline-flex; gap: 6px; align-items: center; cursor: pointer; }
  .ghost {
    appearance: none; border: 1px solid var(--line); background: var(--bg-3);
    color: var(--ink); padding: 3px 9px; border-radius: 6px; cursor: pointer;
    font: inherit; font-size: 12px; white-space: nowrap;
  }
  .ghost:hover, .ghost:focus-visible { border-color: var(--accent); color: #ffe08a; }
  .ghost.copied { border-color: var(--adopt); color: var(--adopt); background: #1c2a22; }
  main { padding: 16px 28px 80px; }
  .row {
    background: var(--bg-2); border: 1px solid var(--line); border-radius: 10px;
    padding: 12px 14px 10px; margin: 0 0 8px;
  }
  details.refresh-context, details.refresh-notes { margin: 10px 0; color: var(--muted); }
  summary { cursor: pointer; }
  .row.done { opacity: 0.55; }
  .row.done .title { text-decoration: line-through; }
  .row-top { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; }
  .id a { font-weight: 650; text-decoration: none; font-variant-numeric: tabular-nums; }
  .kind { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
  .title { flex: 1 1 280px; font-weight: 550; }
  .triage {
    font-size: 12px; font-weight: 650; padding: 2px 8px; border-radius: 999px;
    border: 1px solid var(--line); white-space: nowrap;
  }
  .triage.merge-now { color: #1b1404; background: var(--merge); border-color: var(--merge); }
  .triage.adopt { color: #10241c; background: var(--adopt); border-color: var(--adopt); }
  .triage.review { color: #0e1728; background: var(--review); border-color: var(--review); }
  .triage.discuss { color: #1d1024; background: var(--discuss); border-color: var(--discuss); }
  .triage.cleanup { color: #241a0c; background: var(--cleanup); border-color: var(--cleanup); }
  .triage.reject { color: #2a100c; background: var(--reject); border-color: var(--reject); }
  .triage.bulk { color: var(--ink); background: #3a382e; }
  .tags { display: flex; flex-wrap: wrap; gap: 4px; margin: 8px 0 6px; }
  .tag {
    font-size: 11px; padding: 2px 7px; border-radius: 4px; background: var(--chip);
    color: #d9d2b8; border: 1px solid #3d4233;
  }
  .tag.strengthens-privacy { color: #b8f0d4; border-color: #3d6b55; }
  .tag.impacts-privacy { color: #ffc9b8; border-color: #6b3d33; }
  .tag.posthog-backed, .tag.posthog-shipped { color: #b8e0ff; border-color: #33556b; }
  .tag.approved { color: #1b1404; background: var(--merge); border-color: var(--merge); }
  .sub { color: var(--muted); font-size: 12px; }
  .grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; margin-top: 8px;
  }
  @media (max-width: 1100px) { .grid { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 700px) { .grid { grid-template-columns: 1fr; } header.page, main { padding-left: 14px; padding-right: 14px; } }
  .cell h3 {
    margin: 0 0 4px; font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--muted); font-weight: 650;
  }
  .cell p { margin: 0; color: #e6e0cf; }
  .cell.empty p { color: #6d6858; font-style: italic; }
  .related a { margin-right: 8px; }
  .ev-links { margin: 6px 0 0; padding-left: 18px; }
  .ev-links li { margin: 0 0 4px; }
  .ev-links a { font-weight: 550; }
  .empty-board { color: var(--muted); padding: 40px 8px; }
  .msg { position: relative; display: inline-flex; }
  .copy-msg {
    appearance: none; border: 1px solid var(--line); background: var(--bg-3);
    color: var(--ink); padding: 3px 9px; border-radius: 6px; cursor: pointer;
    font: inherit; font-size: 12px; white-space: nowrap;
  }
  .copy-msg:hover, .copy-msg:focus-visible,
  .mark-done:hover, .mark-done:focus-visible {
    border-color: var(--accent); color: #ffe08a;
  }
  .copy-msg.copied { border-color: var(--adopt); color: var(--adopt); background: #1c2a22; }
  .mark-done.done-on { border-color: var(--reject); color: #ffc9b8; }
  .row-actions { margin-left: auto; display: inline-flex; gap: 6px; align-items: center; }
  .msg:has(.copy-msg.copied) .msg-tip { display: none; }
  .msg-tip {
    display: none; position: absolute; right: 0; top: calc(100% + 6px);
    z-index: 40; width: min(440px, 78vw); background: #2a2718;
    border: 1px solid var(--accent); color: var(--ink); padding: 10px 12px;
    border-radius: 8px; white-space: pre-wrap; font-size: 12px; line-height: 1.45;
    box-shadow: 0 10px 28px rgba(0,0,0,0.45);
  }
  .msg:hover .msg-tip, .msg:focus-within .msg-tip { display: block; }
</style>
</head>
<body>
<header class="page">
  <h1>rrweb-io/rrweb intake triage</h1>
  <p class="lede">
    PR refresh 2026-10-23: 140 open · 19 new · 11 merged · 6 closed unmerged.
    Original recommendations and issue metadata remain dated 2026-09-03.
  </p>
  <details class="refresh-context"><summary>Refresh scope and evidence</summary>
    <p>121 original PRs remain open. Resolved PRs are kept under Merged / closed and excluded from active filters.
    All original recommendations, evidence and review tags are historical, not current approval or meeting decisions.
    The 289 issue states were not refreshed. Browser-local Done marks are preserved separately from upstream status.</p>
    <p>New priorities are provisional, based on public PR metadata, descriptions, reviews and observed head checks,
    not a fresh code audit. Green checks do not imply approval; action_required is not a failed test.
    PostHog requested/planned work is not proof of adoption. Data is a static snapshot, not live.</p>
  </details>
  <p class="lede">Numbers link upstream; vendor links provide historical evidence.
  </p>
  <div class="prefilters" id="prefilters"></div>
  <div class="toolbar">
    <label>Kind
      <select id="kind">
        <option value="all">PRs + issues</option>
        <option value="pr">PRs only</option>
        <option value="issue">Issues only</option>
      </select>
    </label>
    <label>Who
      <select id="who">
        <option value="all">Everyone</option>
        <option value="maintainer">Maintainers</option>
        <option value="community">Community</option>
      </select>
    </label>
    <input type="search" id="q" placeholder="Filter title, author, tags, notes…" />
    <div class="sorts" id="sorts"></div>
  </div>
  <p class="meta">
    <span id="meta-count"></span>
    <span class="meta-actions">
      <label><input type="checkbox" id="show-done" /> Show done</label>
      <button type="button" class="ghost" id="copy-done">Copy done IDs</button>
    </span>
  </p>
</header>
<main id="board"></main>
<script>
"""

HTML_TAIL = r"""
const TRIAGE_LABEL = {
  "merge-now": "Merge now",
  "adopt": "Adopt",
  "review": "Review individually",
  "discuss": "Discuss in team",
  "cleanup": "Request clean-up",
  "reject": "Reject",
  "bulk": "Bulk hygiene",
};
const TRIAGE_RANK = { "merge-now": 0, adopt: 1, review: 2, discuss: 3, cleanup: 4, reject: 5, bulk: 6 };
const TAG_LABEL = {
  "approved": "Approved",
  "waiting-on-review": "Waiting on review",
  "changes-requested": "Changes requested",
  "strengthens-privacy": "Strengthens privacy",
  "impacts-privacy": "Impacts privacy",
  "commercial": "Commercial",
  "posthog-backed": "PostHog-backed",
  "posthog-shipped": "PostHog shipped",
  "posthog-declined": "PostHog declined",
  "posthog-in-fork": "In PostHog fork — do not adopt",
  "posthog-nudge": "PostHog nudge",
  "sentry-backed": "Sentry-backed",
  "datadog-diverged": "Datadog diverged",
  "newrelic-backed": "New Relic-backed",
  "amplitude-backed": "Amplitude-backed",
  "mixpanel-backed": "Mixpanel-backed",
  "grafana-backed": "Grafana-backed",
  "sprig-backed": "Sprig-backed",
  "launchdarkly-backed": "LaunchDarkly-backed",
  "highlight-backed": "Highlight-backed",
  "privacy-overlap": "Privacy-at-capture overlap",
  "maintainer-close": "Maintainer close",
  "draft": "Draft",
  "maintainer": "Maintainer",
  "community": "Community",
  "bulk-updated": "Bulk-updated 2026-06-08",
};
const TAG_RANK = {
  "approved": 0, "posthog-backed": 1, "posthog-shipped": 2,
  "strengthens-privacy": 3, "impacts-privacy": 4, "privacy-overlap": 5,
  "waiting-on-review": 6, "changes-requested": 7, "maintainer-close": 8,
  "commercial": 9, "posthog-declined": 10, "posthog-in-fork": 11,
  "posthog-nudge": 12, "mixpanel-backed": 12.1, "amplitude-backed": 12.2,
  "newrelic-backed": 12.3, "grafana-backed": 12.4, "sprig-backed": 12.5,
  "launchdarkly-backed": 12.6, "highlight-backed": 12.7,
  "sentry-backed": 12.8, "datadog-diverged": 12.9,
  "draft": 13, "maintainer": 14, "community": 15, "bulk-updated": 16,
};

const PREFILTERS = [
  { id: "new", label: "New PRs" },
  { id: "resolved", label: "Merged / closed" },
  { id: "merge-now", label: "Merge now" },
  { id: "adopt", label: "Adopt" },
  { id: "posthog", label: "PostHog-backed" },
  { id: "vendor", label: "Other vendors" },
  { id: "privacy", label: "Strengthens privacy" },
  { id: "waiting", label: "Waiting on review" },
  { id: "maintainer-close", label: "Maintainer close" },
  { id: "discuss", label: "Discuss" },
  { id: "reject", label: "Reject" },
  { id: "done", label: "Done here" },
  { id: "all", label: "All" },
];

const SORTS = [
  { id: "recency", label: "Recency" },
  { id: "number", label: "Number" },
  { id: "triage", label: "Triage status" },
  { id: "tags", label: "Tags" },
];

const state = { pre: "new", kind: "all", who: "all", q: "", sort: "recency", showDone: false };

const DONE_KEY = "rrweb-triage-done:2026-09-03";

function itemKey(item) {
  return item.kind + ":" + item.id;
}

function loadDone() {
  try {
    const raw = JSON.parse(localStorage.getItem(DONE_KEY) || "{}");
    return raw && typeof raw === "object" ? raw : {};
  } catch {
    return {};
  }
}

let doneMap = loadDone();

function saveDone() {
  localStorage.setItem(DONE_KEY, JSON.stringify(doneMap));
}

function isDone(item) {
  return Boolean(doneMap[itemKey(item)]);
}

function setDone(item, on) {
  if (on) doneMap[itemKey(item)] = true;
  else delete doneMap[itemKey(item)];
  saveDone();
}

function doneItems() {
  return ITEMS.filter(isDone);
}

function doneCount() {
  return doneItems().length;
}

function matchesPre(item, pre) {
  const resolved = item.upstreamState === "Merged" || item.upstreamState === "Closed unmerged";
  if (pre === "resolved") return resolved;
  if (pre !== "done" && resolved) return false;
  if (pre === "new") return !item.historical;
  if (pre === "all") return true;
  if (pre === "merge-now") return item.triage === "merge-now";
  if (pre === "adopt") return item.triage === "adopt";
  if (pre === "posthog") return item.tags.includes("posthog-backed") || item.tags.includes("posthog-shipped");
  if (pre === "vendor") return [
    "mixpanel-backed", "amplitude-backed", "newrelic-backed", "grafana-backed",
    "sprig-backed", "launchdarkly-backed", "highlight-backed",
  ].some((t) => item.tags.includes(t));
  if (pre === "privacy") return item.tags.includes("strengthens-privacy");
  if (pre === "waiting") return item.kind === "pr" && item.tags.includes("waiting-on-review");
  if (pre === "maintainer-close") return item.tags.includes("maintainer-close") || (item.who === "maintainer" && item.triage === "reject");
  if (pre === "discuss") return item.triage === "discuss";
  if (pre === "reject") return item.triage === "reject";
  if (pre === "done") return isDone(item);
  return true;
}

function filtered() {
  const q = state.q.trim().toLowerCase();
  return ITEMS.filter((item) => {
    if (!matchesPre(item, state.pre)) return false;
    if (state.pre !== "done" && !state.showDone && isDone(item)) return false;
    if (state.kind !== "all" && item.kind !== state.kind) return false;
    if (state.who !== "all" && item.who !== state.who) return false;
    if (!q) return true;
    const hay = [
      item.id, item.title, item.author, item.authorName, item.triage,
      TRIAGE_LABEL[item.triage], item.next, item.reason, item.notes,
      item.downstream, item.message, ...(item.tags || []), ...(item.related || []),
      ...((item.downstreamLinks || []).map((l) => [l.label, l.note, l.url].join(" "))),
    ].join(" ").toLowerCase();
    return hay.includes(q);
  });
}

function tagKey(item) {
  const ranked = (item.tags || []).map((t) => TAG_RANK[t] ?? 50);
  const min = ranked.length ? Math.min(...ranked) : 99;
  const names = (item.tags || []).map((t) => TAG_LABEL[t] || t).sort().join(",");
  return [min, names];
}

function sorted(list) {
  const out = list.slice();
  out.sort((a, b) => {
    if (state.sort === "recency") {
      if (a.updatedAt !== b.updatedAt) return a.updatedAt < b.updatedAt ? 1 : -1;
      return b.id - a.id;
    }
    if (state.sort === "number") return b.id - a.id;
    if (state.sort === "triage") {
      const d = (TRIAGE_RANK[a.triage] ?? 9) - (TRIAGE_RANK[b.triage] ?? 9);
      if (d) return d;
      return b.id - a.id;
    }
    if (state.sort === "tags") {
      const [ar, an] = tagKey(a);
      const [br, bn] = tagKey(b);
      if (ar !== br) return ar - br;
      if (an !== bn) return an < bn ? -1 : 1;
      return b.id - a.id;
    }
    return 0;
  });
  return out;
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function fmtDate(iso) {
  if (!iso) return "—";
  return iso.slice(0, 10);
}

function relatedUrl(id) {
  const hit = ITEMS.find((x) => x.id === id);
  if (hit) return hit.url;
  return "https://github.com/rrweb-io/rrweb/issues/" + id;
}

function cell(title, text) {
  const empty = !text;
  return `<div class="cell${empty ? " empty" : ""}"><h3>${esc(title)}</h3><p>${empty ? "None recorded." : esc(text)}</p></div>`;
}

function downstreamCell(item) {
  const links = item.downstreamLinks || [];
  const empty = !item.downstream && !links.length;
  const list = links.length
    ? `<ul class="ev-links">${links.map((l) =>
        `<li><a href="${esc(l.url)}" target="_blank" rel="noreferrer">${esc(l.label)}</a>${l.note ? " — " + esc(l.note) : ""}</li>`
      ).join("")}</ul>`
    : "";
  const body = item.downstream
    ? `<p>${esc(item.downstream)}</p>${list}`
    : (list || `<p>None recorded.</p>`);
  return `<div class="cell${empty ? " empty" : ""}"><h3>Downstream evidence</h3>${body}</div>`;
}

function messageToCopy(item) {
  const warning = "Historical draft from 2026-09-03. Recheck the current item, diff, CI and reviews before using this text.\n\n";
  return (item.historical ? warning : "") + item.message;
}

function refreshNotes(item) {
  if (!item.refresh) return "";
  const r = item.refresh;
  const checks = [...r.runs, ...r.statuses].map((x) =>
    `<li>${x.url ? `<a href="${esc(x.url)}" target="_blank" rel="noreferrer">${esc(x.name)}</a>` : esc(x.name)}: ${esc(x.result)}</li>`
  ).join("");
  const reviews = r.reviews.map((x) => `${x.author}: ${x.state}`).join("; ") || "No submitted reviews returned";
  return `<details class="refresh-notes"><summary>Observed checks and review gates · 2026-10-23</summary>
    <ul>${checks}</ul><p>${esc(reviews)}. Mergeability: ${r.mergeable === true ? "mergeable" : r.mergeable === false ? "conflicts" : "unknown"}; ${esc(r.mergeableState)}.</p>
    <p>Head ${esc(r.sha)}. ${r.files} files, +${r.plus} / −${r.minus}. No merge approval inferred.</p>
  </details>`;
}

function renderRow(item) {
  const tags = (item.tags || []).map((t) =>
    `<span class="tag ${esc(t)}">${esc(TAG_LABEL[t] || t)}</span>`
  ).join("");
  const rel = (item.related || []).map((id) =>
    `<a href="${esc(relatedUrl(id))}" target="_blank" rel="noreferrer">#${id}</a>`
  ).join("");
  const review = item.kind === "pr"
    ? ` · ${esc(item.reviewDecision)}${item.draft ? " · draft" : ""}`
    : "";
  const msg = !["Merged", "Closed unmerged"].includes(item.upstreamState) && item.message
    ? `<button type="button" class="copy-msg" data-id="${item.id}" data-kind="${item.kind}">${item.historical ? "Copy historical draft" : "Copy message"}</button>
        <span class="msg-tip">Historical draft from 2026-09-03. Recheck current state and review before use. ${esc(item.message)}</span>`
    : "";
  const marked = isDone(item);
  return `<article class="row${marked ? " done" : ""}" data-id="${item.id}" data-kind="${item.kind}">
    <div class="row-top">
      <span class="kind">${item.kind === "pr" ? "PR" : "Issue"}</span>
      <span class="id"><a href="${esc(item.url)}" target="_blank" rel="noreferrer">#${item.id}</a></span>
      <span class="kind">${esc(item.upstreamState)}${item.resolvedAt ? " · " + fmtDate(item.resolvedAt) : ""}</span>
      <span class="title">${esc(item.title)}</span>
      <span class="triage ${esc(item.triage)}">${esc(TRIAGE_LABEL[item.triage] || item.triage)}</span>
      <span class="row-actions">
        <button type="button" class="mark-done ghost${marked ? " done-on" : ""}" data-id="${item.id}" data-kind="${item.kind}">${marked ? "Undo" : "Done"}</button>
        ${msg ? `<span class="msg">${msg}</span>` : ""}
      </span>
    </div>
    <div class="sub">${esc(item.authorName || item.author)} (@${esc(item.author)}) · ${esc(item.whoLabel)} · updated ${fmtDate(item.updatedAt)} · opened ${fmtDate(item.createdAt)}${review}</div>
    <div class="sub">${item.historical ? "Historical recommendation, tags and review evidence: 2026-09-03" : "New provisional recommendation: 2026-10-23"}</div>
    <div class="tags">${tags || '<span class="tag">No extra tags</span>'}</div>
    ${refreshNotes(item)}
    <div class="grid">
      ${downstreamCell(item)}
      ${cell("Reason", item.reason)}
      ${cell("Notes", item.notes)}
      ${cell("Suggested next step", item.next)}
    </div>
    ${rel ? `<div class="sub related" style="margin-top:8px">Related: ${rel}</div>` : ""}
  </article>`;
}

function countPre(id) {
  return ITEMS.filter((item) => {
    if (!matchesPre(item, id)) return false;
    if (id !== "done" && !state.showDone && isDone(item)) return false;
    if (state.kind !== "all" && item.kind !== state.kind) return false;
    if (state.who !== "all" && item.who !== state.who) return false;
    return true;
  }).length;
}

function render() {
  const list = sorted(filtered());
  document.getElementById("prefilters").innerHTML = PREFILTERS.map((p) =>
    `<button type="button" data-filter="${p.id}" class="${state.pre === p.id ? "active" : ""}">${esc(p.label)}<span class="n">${countPre(p.id)}</span></button>`
  ).join("");
  document.getElementById("sorts").innerHTML =
    `<label>Sort</label>` +
    SORTS.map((s) =>
      `<button type="button" data-sort="${s.id}" class="${state.sort === s.id ? "active" : ""}">${esc(s.label)}</button>`
    ).join("");
  document.getElementById("meta-count").textContent =
    `${list.length} shown · ${doneCount()} done in this browser · PR status 2026-10-23 · recommendations dated per row`;
  document.getElementById("board").innerHTML = list.length
    ? list.map(renderRow).join("")
    : `<p class="empty-board">No rows match these filters.</p>`;
}

document.getElementById("prefilters").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-filter]");
  if (!btn) return;
  state.pre = btn.dataset.filter;
  render();
});
document.getElementById("sorts").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-sort]");
  if (!btn) return;
  state.sort = btn.dataset.sort;
  render();
});
document.getElementById("kind").addEventListener("change", (e) => { state.kind = e.target.value; render(); });
document.getElementById("who").addEventListener("change", (e) => { state.who = e.target.value; render(); });
document.getElementById("q").addEventListener("input", (e) => { state.q = e.target.value; render(); });
document.getElementById("show-done").addEventListener("change", (e) => {
  state.showDone = e.target.checked;
  render();
});
document.getElementById("copy-done").addEventListener("click", async (e) => {
  const btn = e.currentTarget;
  const lines = doneItems().map((item) =>
    `${item.kind === "pr" ? "PR" : "Issue"} ${item.id}  ${item.title}`
  );
  const text = lines.length ? lines.join("\n") : "None marked done.";
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  }
  btn.classList.add("copied");
  btn.textContent = "Copied";
  setTimeout(() => {
    btn.classList.remove("copied");
    btn.textContent = "Copy done IDs";
  }, 1400);
});
document.getElementById("board").addEventListener("click", async (e) => {
  const doneBtn = e.target.closest("button.mark-done");
  if (doneBtn) {
    const id = Number(doneBtn.dataset.id);
    const kind = doneBtn.dataset.kind;
    const item = ITEMS.find((x) => x.id === id && x.kind === kind);
    if (!item) return;
    setDone(item, !isDone(item));
    render();
    return;
  }
  const btn = e.target.closest("button.copy-msg");
  if (!btn) return;
  const id = Number(btn.dataset.id);
  const kind = btn.dataset.kind;
  const item = ITEMS.find((x) => x.id === id && x.kind === kind);
  if (!item || !item.message) return;
  try {
    await navigator.clipboard.writeText(messageToCopy(item));
  } catch {
    const ta = document.createElement("textarea");
    ta.value = messageToCopy(item);
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  }
  btn.classList.add("copied");
  btn.textContent = "Copied";
  setTimeout(() => {
    btn.classList.remove("copied");
    btn.textContent = item.historical ? "Copy historical draft" : "Copy message";
  }, 1400);
});

render();
</script>
</body>
</html>
"""


def main() -> None:
    items = apply_refresh(assemble())
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    html = HTML_HEAD + f"const ITEMS = {payload};\n" + HTML_TAIL
    OUT_HTML.write_text(html)
    prs = [i for i in items if i["kind"] == "pr"]
    issues = [i for i in items if i["kind"] == "issue"]
    print(f"Wrote {OUT_HTML} ({len(html)} bytes)")
    print(f"PRs {len(prs)}  issues {len(issues)}")
    from collections import Counter
    print("PR triage", dict(Counter(i["triage"] for i in prs)))
    print("Issue triage", dict(Counter(i["triage"] for i in issues)))
    print("Merge now", [i["id"] for i in prs if i["triage"] == "merge-now"])
    print("Adopt", sorted(i["id"] for i in prs if i["triage"] == "adopt"))
    print("PostHog-backed", sorted(i["id"] for i in items if "posthog-backed" in i["tags"] or "posthog-shipped" in i["tags"]))
    vendor_tags = (
        "mixpanel-backed", "amplitude-backed", "newrelic-backed", "grafana-backed",
        "sprig-backed", "launchdarkly-backed", "highlight-backed",
    )
    print("Other vendors", sorted(i["id"] for i in items if any(t in i["tags"] for t in vendor_tags)))
    print("Maintainer close", sorted(i["id"] for i in items if "maintainer-close" in i["tags"] or (i["who"] == "maintainer" and i["triage"] == "reject")))


if __name__ == "__main__":
    main()