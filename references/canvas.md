# Canvas setup and display

If the host already has an Excalidraw connector, use it. Otherwise use [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) version 2.0.0 (tested with Node 24+). It runs a local canvas in the browser and has a CLI.

## Start a canvas

Install it in the task's scratch folder, not globally:

```sh
npm install --prefix work/excalidraw-runtime --no-audit --no-fund mcp-excalidraw-server@2.0.0
python3 <skill-dir>/scripts/patch_canvas_2_0_0.py work/excalidraw-runtime/node_modules/mcp-excalidraw-server
PORT=3217 HOST=127.0.0.1 node work/excalidraw-runtime/node_modules/mcp-excalidraw-server/dist/server.js
```

Leave the server running. If the port is taken, the server exits with code 1. Pick another free port. Don't reuse a canvas from an earlier session.

Open `http://127.0.0.1:<port>` with your agent's browser tool (for example Claude in Chrome, or any tool that drives a real browser) and wait for a green **Connected** in the header. Image export needs a connected browser.

Run CLI commands as `node work/excalidraw-runtime/node_modules/mcp-excalidraw-server/dist/bin.js <command>`, with `EXCALIDRAW_NO_AUTOSTART=1` and `EXPRESS_SERVER_URL=http://127.0.0.1:<port>` set.

## Add, load and export

- **New elements.** `add work/elements.json` takes a JSON array. Give each element a stable ID, put labels in `text`, and connect arrows with `startElementId` / `endElementId`.
- **Existing `.excalidraw` files.** Don't use the CLI import, which drops text. Clean the file first, then load it:

  ```sh
  python3 <skill-dir>/scripts/prepare_scene.py source.excalidraw work/prepared.excalidraw
  node <skill-dir>/scripts/load_native.mjs work/prepared.excalidraw http://127.0.0.1:3217 --replace
  ```

  `prepare_scene.py` writes a new file without deleted elements, broken links or order keys, and never overwrites. Always run it on an export before loading it anywhere: the export's order keys are invalid on boards over about 90 elements, and the scene won't open. `load_native.mjs` replaces the canvas, so reload the tab after. An already open tab can write its old drawing back over the load; check `GET /api/elements` reports the expected count, and if it doesn't, load into a new canvas on another port. It needs the patch above. Scenes with embedded images can't use it; the person has to open those by hand.
- **Replacing.** `load_native.mjs` always replaces the whole canvas, and `--replace` is required to confirm that. Only load onto a canvas you created for this task.
- **Export.** Click **Sync to Backend** in the canvas first so text sizes match the browser. Then run `export --out outputs/design.excalidraw` and `screenshot --out outputs/design.png`.

Never click the canvas menu's **Open**. It opens the system file picker, which blocks the browser tools and can strand the session.

## Check

Read the PNG to see it, and zoom into labels and arrows. If a label hides its arrow, shorten the label or widen the gap. Fix the canvas and export again. Then run the export through `prepare_scene.py`, load it back onto the same canvas with `load_native.mjs`, and confirm labels and arrows survived.

## Open the finished board on excalidraw.com

excalidraw.com keeps one drawing in the browser's `localStorage` under the key `excalidraw`. Loading a board replaces it, so these steps back it up first. The board goes in the way a dragged-and-dropped file does: a hidden file input gets the file from disk, then a synthetic `drop` event hands it to the open page. The page loads it into its live drawing and saves it itself, with no reload, so no tab can write an old drawing back over it. Nothing is uploaded to a server, and other excalidraw.com tabs don't need closing.

1. Boards with embedded images need the person to open them by hand; stop here. Otherwise run `python3 <skill-dir>/scripts/prepare_scene.py outputs/design.excalidraw work/excalidraw-com.excalidraw`, using a new file name each time. The file must be in the session's scratch or outputs folder.
2. Open a new tab at `https://excalidraw.com`.
3. Back up the current drawing and add a file input with your browser tool's run-JavaScript action (`javascript_tool` in Claude in Chrome). This returns `{backup}`, which is null if the old drawing was empty. The backup is named after the drawing it holds, taken from its biggest text (its title), so the person can tell backups apart, e.g. `chat-scheduler-for-cal-com-take-home-and-2026-10-28T07:06:15.416Z`. The timestamp at the end is what marks a key as a backup; none of excalidraw.com's own keys end in one:

   ```js
   if (location.origin !== 'https://excalidraw.com') throw new Error('Run this on excalidraw.com');
   const old = localStorage.getItem('excalidraw');
   let backup = null;
   const live = old ? JSON.parse(old).filter(e => !e.isDeleted) : [];
   if (live.length) {
     const title = live.filter(e => e.type === 'text' && !e.containerId).sort((a, b) => b.fontSize - a.fontSize || a.y - b.y)[0];
     const slug = ((title && title.text) || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40).replace(/-$/, '') || 'untitled';
     backup = slug + '-' + new Date().toISOString();
     localStorage.setItem(backup, JSON.stringify({elements: old, state: localStorage.getItem('excalidraw-state')}));
   }
   document.getElementById('agent-scene-input')?.remove();
   const input = Object.assign(document.createElement('input'), {type: 'file', id: 'agent-scene-input', accept: '.excalidraw,application/json'});
   input.setAttribute('aria-label', 'Agent scene file');
   input.style.cssText = 'position:fixed;left:0;bottom:0;opacity:0.01;width:2px;height:2px;';
   document.body.appendChild(input);
   window.__agentFile = new Promise(resolve => input.addEventListener('change', () => resolve(input.files[0])));
   ({backup})
   ```

4. Find the input labelled "Agent scene file" and set the prepared file on it with your browser tool's file-upload action (`find`, then `file_upload` in Claude in Chrome). Don't click the input: that opens the system file picker.
5. Drop the file onto the canvas:

   ```js
   const f = await window.__agentFile;
   const file = new File([await f.text()], 'board.excalidraw', {type: 'application/json'});
   const dt = new DataTransfer(); dt.items.add(file);
   const target = document.querySelector('.excalidraw__canvas.interactive');
   const r = target.getBoundingClientRect();
   const opts = {bubbles: true, cancelable: true, dataTransfer: dt, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2};
   target.dispatchEvent(new DragEvent('dragover', opts));
   target.dispatchEvent(new DragEvent('drop', opts));
   document.getElementById('agent-scene-input').remove();
   ({dropped: file.size})
   ```

6. Press Escape, then Shift+1 to fit the board. Take a screenshot to confirm. Then check that it saved: `JSON.parse(localStorage.getItem('excalidraw')).filter(e => !e.isDeleted).length` should equal the element count `prepare_scene.py` printed.
7. Tell the person the board is open and give the backup key if there is one.

To bring back their old drawing, run this on an excalidraw.com tab. It drops a backup onto the canvas the same way and deletes that key once the drop saves. Set `want` to the key the person names, or leave it null for the newest. The board shown now is lost from the browser but still on disk.

```js
if (location.origin !== 'https://excalidraw.com') throw new Error('Run this on excalidraw.com');
const want = null;
// A backup key ends in an ISO timestamp; sort on it, since the drawing name comes first.
const isBackup = k => /-\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/.test(k);
const key = want || Object.keys(localStorage).filter(isBackup).sort((a, b) => a.slice(-24).localeCompare(b.slice(-24))).at(-1);
if (!key) throw new Error('No backup key in this browser');
const elements = JSON.parse(JSON.parse(localStorage.getItem(key)).elements);
const scene = {type: 'excalidraw', version: 2, source: 'https://excalidraw.com', elements, appState: {}, files: {}};
const dt = new DataTransfer();
dt.items.add(new File([JSON.stringify(scene)], 'restore.excalidraw', {type: 'application/json'}));
const target = document.querySelector('.excalidraw__canvas.interactive');
const r = target.getBoundingClientRect();
const opts = {bubbles: true, cancelable: true, dataTransfer: dt, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2};
target.dispatchEvent(new DragEvent('dragover', opts));
target.dispatchEvent(new DragEvent('drop', opts));
await new Promise(res => setTimeout(res, 3000));
const live = JSON.parse(localStorage.getItem('excalidraw')).filter(e => !e.isDeleted).length;
const expected = elements.filter(e => !e.isDeleted).length;
if (live === expected) localStorage.removeItem(key);
({restored: key, live, expected, keyRemoved: live === expected})
```

Tried and dropped, so don't retry them:

- (28 Oct 2026) Writing the board into `localStorage` and reloading the page. The page saved its old drawing back over the board during the reload, and the board never appeared. The drop above replaced it.

Tried and dropped (5 Oct 2026):

- Fetching the file from a local server. Chrome holds the request at a permission prompt the page can't see.
- Pasting the board into a run-JavaScript call as text. It works, but a 200 KB board is about 19,000 characters that must be copied exactly.
- Writing `localStorage` without reloading. The open page doesn't pick it up.
- The menu's **Open**. It's the system file picker.
