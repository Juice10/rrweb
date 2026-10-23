// Offline UI logic checks. Run after build_board.py with Node.js.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];
const elements = {};
const stored = {};
const context = {
  document: {
    getElementById(id) {
      return elements[id] ||= { addEventListener() {} };
    },
  },
  localStorage: {
    getItem(key) { return stored[key] || null; },
    setItem(key, value) { stored[key] = value; },
  },
};
vm.createContext(context);
vm.runInContext(script, context);
const run = (code) => vm.runInContext(code, context);
const count = () => (elements.board.innerHTML.match(/<article /g) || []).length;
assert.equal(count(), 19);
assert.equal(run('ITEMS.length'), 446);
assert.equal((elements.board.innerHTML.match(/<details /g) || []).length, 19);
assert.ok(!elements.board.innerHTML.includes('<details open'));
run('state.pre = "resolved"; render()');
assert.equal(count(), 17);
assert.ok(!elements.board.innerHTML.includes('class="copy-msg"'));
run('state.pre = "all"; state.kind = "pr"; render()');
assert.equal(count(), 140);
run('state.q = "release observers, buffers and listeners"; render()');
assert.equal(count(), 1);
run('state.q = "";');
for (const sort of ['number', 'triage', 'tags', 'recency']) {
  run(`state.sort = "${sort}"; render()`);
  assert.equal(count(), 140);
}
run('state.pre = "new"; setDone(ITEMS.find(p => p.id === 1971), true); render()');
assert.equal(count(), 18);
run('doneMap = loadDone(); state.pre = "done"; render()');
assert.equal(count(), 1);
run('setDone(ITEMS.find(p => p.id === 1971), false); render()');
assert.equal(count(), 0);
run('state.pre = "all"; state.kind = "issue"; render()');
assert.equal(count(), 289);
assert.ok(elements.board.innerHTML.includes('class="copy-msg"'));
assert.ok(run('messageToCopy(ITEMS.find(p => p.historical && p.message))').startsWith('Historical draft from 2026-09-03.'));
assert.equal(run('DONE_KEY'), 'rrweb-triage-done:2026-09-03');
console.log('PASS: queue counts, search, sorting, closed disclosures, resolved copy guard, issue actions, Done/Undo and storage compatibility');
