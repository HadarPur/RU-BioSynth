# BioSynth comparison runs

Runs BioSynth (`biosynth.BioSynth.BioSynthApp`) against the same input genes used for the other tools in `toolscomparison/`, so results can be compared head-to-head.

## Files

- `pipeline.py` — `run_biosynth(gene_dir, gene_name, pattern_file_name, codon_usage_file_name)` runs the full pipeline: invoke the BioSynth CLI, locate the coding region, read the optimized output, compute CAI on the coding region, and report 5' UTR / 3' UTR substitution counts.
- `SAUR11.py`, `SAUR40.py`, `MYH9.py` — thin callers that supply the inputs for one gene.
- `results/` — BioSynth outputs. Each run writes to `./results/<gene_name>/BioSynth-Outputs/`.
- `__pycache__/` — ignore.

## How to run

From the repo root:

```bash
python toolscomparison/BioSynth/SAUR40.py
```

The pipeline resolves inputs under `files/<gene_dir>/`:

- Sequence: `files/<gene_dir>/<gene_name>.txt` (must contain a `*` marker immediately before the start codon)
- Unwanted patterns: `files/<gene_dir>/<pattern_file_name>.txt` (one pattern per line)
- Codon usage table: `files/<gene_dir>/<codon_usage_file_name>.txt` (tab-separated `codon\tfrequency`)

Results are written to `./results/<gene_name>/` (the directory is wiped before each run). The pipeline reads the optimized sequence from `./results/<gene_name>/BioSynth-Outputs/Optimized-Sequence*.txt`.

## Parameters

| Name | Meaning |
|---|---|
| `gene_dir` | Subdirectory under `files/` holding the inputs |
| `gene_name` | Sequence file stem and output directory name |
| `pattern_file_name` | Unwanted patterns file stem (no `.txt`) |
| `codon_usage_file_name` | Codon usage file stem (no `.txt`) |

Unlike the DNAChisel pipeline, no `species` parameter is needed — BioSynth reads the codon usage table directly from the file passed via `-c`.

## Output

In addition to BioSynth's own logs, the pipeline prints:

- Path and length of the optimized sequence
- Optimized sequence and its coding region
- CAI on the coding region
- 5' UTR, 3' UTR, and total non-coding substitution counts (positions where the optimized base differs from the original outside the coding region)