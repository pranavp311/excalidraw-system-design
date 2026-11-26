// Load native shape/text scenes into a dedicated local canvas without lossy conversion.
import {readFile} from 'node:fs/promises';
const [file, address, replace] = process.argv.slice(2);
if (!file || !address || replace !== '--replace') {
  throw new Error('Usage: node load_native.mjs prepared.excalidraw http://127.0.0.1:3217 --replace');
}
const url = new URL(address);
if (url.protocol !== 'http:' || !['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname)) {
  throw new Error('Only a local canvas is supported.');
}
const scene = JSON.parse(await readFile(file, 'utf8'));
if (scene.type !== 'excalidraw' || !Array.isArray(scene.elements)) throw new Error('Expected a native scene.');
if (scene.elements.some(e => e.isDeleted)) throw new Error('Run prepare_scene.py first.');
if (scene.elements.some(e => e.type === 'image')) throw new Error('Images require native browser Open; this loader supports shapes/text only.');
if (scene.elements.some(e => typeof e.versionNonce !== 'number' || typeof e.isDeleted !== 'boolean')) {
  throw new Error('Expected fully expanded native elements, not toolkit shorthand.');
}
const response = await fetch(new URL('/api/elements/sync', url), {
  method: 'POST', headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({elements: scene.elements, timestamp: new Date().toISOString()}),
});
if (!response.ok) throw new Error(`Canvas returned ${response.status}: ${await response.text()}`);
console.log(await response.text());
console.log('Reload the browser canvas. This endpoint replaces its contents.');
