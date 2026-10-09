# COSMO comparison runs

Runs [COSMO](https://www.cs.bgu.ac.il/~vaksler/COSMO/) against the same input genes used for the other tools in `toolscomparison/`, so results can be compared head-to-head.

## Files

- `pipeline.py` — `run_cosmo(gene_dir, gene_name, pattern_file_name, codon_usage_file_name)` runs the full pipeline: ensure the COSMO binary is present (extracting `cosmo0.9.zip` on first run), convert the codon usage table to COSMO's `.cu` format, extract the coding region, shell out to `cosmo`, parse the optimized CDS from stdout, reassemble it with the original UTRs, compute CAI on the coding region, and report pattern violations and 5' UTR / 3' UTR substitution counts.
- `SAUR11.py`, `SAUR40.py`, `MYH9.py` — thin callers that supply the inputs for one gene.
- `cosmo0.9.zip` — bundled COSMO binary archive. Extracted automatically into `cosmo0.9/` on first run.
- `cosmo0.9/` — created by the pipeline on first run; contains the `cosmo` binary.
- `results/` — per-gene outputs. Each run writes to `./results/<gene_name>/` with the generated `.cu` file and the CDS-only input written for COSMO.
- `__pycache__/` — ignore.

## How to run

From the repo root:

```bash
python toolscomparison/COSMO/SAUR40.py
```

The pipeline resolves inputs under `files/<gene_dir>/`:

- Sequence: `files/<gene_dir>/<gene_name>.txt` (must contain a `*` marker immediately before the start codon)
- Unwanted patterns: `files/<gene_dir>/<pattern_file_name>.txt` (one pattern per line; joined with `|` and passed via COSMO's `-p` flag)
- Codon usage table: `files/<gene_dir>/<codon_usage_file_name>.txt` (tab-separated `codon\tfrequency`)

Results are written to `./results/<gene_name>/` (the directory is wiped before each run).

## Parameters

| Name | Meaning |
|---|---|
| `gene_dir` | Subdirectory under `files/` holding the inputs |
| `gene_name` | Sequence file stem and output directory name |
| `pattern_file_name` | Unwanted patterns file stem (no `.txt`) |
| `codon_usage_file_name` | Codon usage file stem (no `.txt`) |

Unlike the DNAChisel pipeline, no `species` parameter is needed — COSMO uses the `.cu` file converted from the codon usage table at runtime.

## COSMO binary

The pipeline looks for `cosmo0.9/cosmo` next to `pipeline.py`. If it's missing, it extracts `cosmo0.9.zip` into this directory and sets the executable bit (zip extraction can drop permissions on macOS/Linux). If both the binary and the archive are missing, the run errors out early.

## Output

In addition to COSMO's own stdout, the pipeline prints:

- Path/length of the optimized sequence (CDS stitched back with the original UTRs)
- Optimized sequence and its coding region
- CAI on the coding region
- 5' UTR, 3' UTR, and total non-coding substitution counts — always `0` here, since COSMO only optimizes the CDS and the UTRs are copied through unchanged
- Pattern hit counts for any forbidden pattern that still appears in the optimized sequence
