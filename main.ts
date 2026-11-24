import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
// Self-check: the copy must be byte-identical to the shipped image.
if (statSync(src).size !== statSync(dst).size) {
  throw new Error(`copy mismatch: ${src} vs ${dst}`);
}
console.log(`wrote ${dst} (${statSync(dst).size} bytes)`);
