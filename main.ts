// news-image-20261119 entry: copy the poster beside this program to the
// grader's output directory. Node 22, standard library only. No network,
// no randomness, no arguments: the output bytes are an exact copy of
// entry.png, so two runs produce identical bytes.
//
// The poster itself is drawn by poster.py (Pillow, deterministic) from
// the 37 verified stories of Thursday 19 November 2026; this program
// only ships the finished file. The copy is checked by size so a
// truncated write fails loudly instead of shipping a broken entry.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

// The gate only accepts a whole PNG: refuse anything whose first
// bytes are not the PNG signature (137 80 78 71 13 10 26 10).
const head = readFileSync(dst).subarray(0, 8);
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngSig)) {
  throw new Error("entry.png is not a PNG file");
}

// Fail loudly instead of shipping a truncated copy.
const srcSize = statSync(src).size;
const dstSize = statSync(dst).size;
if (srcSize !== dstSize) {
  throw new Error(`entry.png copy size mismatch: ${srcSize} vs ${dstSize}`);
}
