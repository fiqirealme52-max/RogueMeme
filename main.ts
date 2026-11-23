import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Meme Sprint 3 entry: the program writes the meme image to /output/entry.png.
// The meme itself ships in this repo as meme.png (1024x1024, under 1 MiB);
// the program copies it verbatim and checks the gate before writing.
const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "meme.png");
const OUT = "/output/entry.png";

const bytes = readFileSync(SRC);
if (bytes.length > 1_048_576) throw new Error("meme over 1 MiB");
if (bytes.subarray(1, 4).toString("ascii") !== "PNG") {
  throw new Error("not a PNG");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error("meme over 1024x1024");
}

mkdirSync("/output", { recursive: true });
writeFileSync(OUT, bytes);

// Read back what was written: a corrupted or partial output must fail
// loudly here instead of shipping silently to the judge.
const written = readFileSync(OUT);
if (!written.equals(bytes)) {
  throw new Error("read-back mismatch: /output/entry.png is not the meme");
}
console.log(`wrote ${bytes.length}-byte ${width}x${height} meme to ${OUT}`);
