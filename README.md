# VanillaBPE-Byte

GitHub: [shubhjang2004/VanillaBPE](https://github.com/shubhjang2004/VanillaBPE) · pip/import name: `vanillabpe_byte` · sibling repos: [AksharaG2P](https://github.com/shubhjang2004/AksharaG2P), [VanillaCharBPE](https://github.com/shubhjang2004/VanillaCharBPE)

Byte-level vanilla BPE baseline for Indic scripts (GPT/tiktoken-style, same pipeline as AksharaG2P).

Part of a three-way controlled comparison for the AksharaG2P paper:

| repo | base units | cross-script sharing |
|---|---|---|
| **AksharaG2P** | one unit per Indic character, shared across scripts by Unicode block offset (क = ক = ક = க = ಕ) + script markers | yes |
| **VanillaBPE-Char** | one unit per Indic character, separate per script | no |
| **VanillaBPE-Byte** | UTF-8 bytes (GPT/tiktoken style) | no |

**Base units:** raw UTF-8 bytes only, exactly like GPT-2/tiktoken byte-level
BPE. Every Devanagari/Bengali/Tamil/... character is 3 bytes, and BPE has to
learn merges that rebuild characters before it can build words. There is no
cross-script sharing and there are no script markers.

Compared with AksharaG2P this changes two things at once (bytes vs characters
*and* no phoneme sharing); compare with VanillaBPE-Char to separate the two.

## Same pipeline as AksharaG2P

All three repos share the same Rust BPE core and trainer, the same
pre-tokenizer regex (GPT-4 style, keeping matras/virama/ZWNJ inside words),
the same script-boundary splitting, special tokens, training procedure and
Python API. **The only source difference is the `VARIANT` section of
`src/script.rs`** (plus variant-specific tests). Verify with:

```bash
diff -r AksharaG2P/src VanillaBPE-Byte/src
diff -r AksharaG2P/python/aksharag2p VanillaBPE-Byte/python/vanillabpe_byte
diff AksharaG2P/tests/test_encoding.py VanillaBPE-Byte/tests/test_encoding.py
```

## Usage

```python
import vanillabpe_byte as tok

enc = tok.train({"hi": "hindi.txt", "bn": "bengali.txt"}, vocab_size=32_000, lines_per_file=500_000)
enc.save("vanillabpe_byte_32k.json")

enc = tok.get_encoding("vanillabpe_byte_32k.json")
ids = enc.encode("भारत सरकार नई दिल्ली में है।")
assert enc.decode(ids) == "भारत सरकार नई दिल्ली में है।"
```

Training script (same lines as the other two tokenizers):
`python scripts/train_corpus.py --base /content/drive/MyDrive`.

Decoding is lossless: `decode(encode(text)) == text` for any string.

## Install

```bash
pip install git+https://github.com/shubhjang2004/VanillaBPE   # builds from source; needs Rust (https://rustup.rs)
```

## Development

```bash
pip install maturin pytest
maturin develop --release
cargo test && pytest tests
```
