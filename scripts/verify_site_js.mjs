// Parse every browser script and confirm the published data files are loadable.
import { readFileSync } from 'node:fs';
import { Script, runInNewContext } from 'node:vm';
import { join } from 'node:path';
const root = new URL('../', import.meta.url);
const get = (path) => readFileSync(new URL(path, root), 'utf8');
const loaded = { window: {} };
const parts = [
  'dist/data-meta.js', 'dist/data-2002-2006.js',
  'dist/data-2007-2011.js', 'dist/data-2012-2016.js',
  'dist/data-2017-2021.js', 'dist/data-2022-2026.js',
  'dist/writings-data.js', 'dist/teaching-data.js'
];
for (const path of parts) {
  const code = get(path);
  new Script(code, { filename: path });
  runInNewContext(code, loaded);
}
new Script(get('dist/app.js'), { filename: 'dist/app.js' });
const page = get('dist/index.html');
const inline = [...page.matchAll(/<script\s*>([\s\S]*?)<\/script>/g)].map(x => x[1]);
if (inline.length !== 1) throw new Error('Expected exactly one inline behavior script');
new Script(inline[0], { filename: 'dist/index.html:inline-script' });
const radio = loaded.window.__COHON_EPISODES__ || [];
if (radio.length !== 1265) throw new Error('Site loaded ' + radio.length + ' radio records');
if (loaded.window.SAM_WRITINGS?.length !== 316) throw new Error('Writing bundle differs from 316');
if (loaded.window.SAM_TEACHING?.length !== 26) throw new Error('Teaching bundle differs from 26');
if (loaded.window.__COHON_META__?.stats?.total_records !== radio.length) throw new Error('Site radio totals differ');
for (const codeFile of parts) {
  const basename = codeFile.split('/').at(-1);
  if (!page.includes('src="' + basename + '"')) {
    throw new Error('Browser data script is not loaded by the landing page: ' + basename);
  }
}
console.log('PASS: HTML inline JS syntax and 1,265/316/26 browser-loaded records');
