# DNAChisel comparison runs

Runs [DNAChisel](https://edinburgh-genome-foundry.github.io/DnaChisel/) against the same input genes used for the other tools in `toolscomparison/`, so results can be compared head-to-head.

## Files

- `pipeline.py` — `run_dnachisel(gene_dir, gene_name, pattern_file_name, codon_usage_file_name, species)` runs the full pipeline: resolve constraints, optimize for CAI, print the optimized sequence, compute CAI on the coding region, and report 5' UTR / 3' UTR substitution counts.
- `SAUR11.py`, `SAUR40.py`, `MYH9.py` — thin callers that supply the inputs for one gene.
- `__pycache__/` — ignore.

## How to run

From the repo root:

```bash
python toolscomparison/DNAChisel/SAUR40.py
```

The pipeline resolves inputs under `files/<gene_dir>/`:

- Sequence: `files/<gene_dir>/<gene_name>.txt` (must contain a `*` marker immediately before the start codon)
- Unwanted patterns: `files/<gene_dir>/<pattern_file_name>.txt` (one pattern per line)
- Codon usage table: `files/<gene_dir>/<codon_usage_file_name>.txt` (tab-separated `codon\tfrequency`)

Results are written to `./results/<gene_name>/` (the directory is wiped before each run).

## Parameters

| Name | Meaning |
|---|---|
| `gene_dir` | Subdirectory under `files/` holding the inputs |
| `gene_name` | Sequence file stem and output directory name |
| `pattern_file_name` | Unwanted patterns file stem (no `.txt`) |
| `codon_usage_file_name` | Codon usage file stem (no `.txt`) |
| `species` | Species key passed to `MaximizeCAI` (e.g. `s_cerevisiae`, `e_coli`) |

## Output

In addition to DNAChisel's own constraint/objective summaries, the pipeline prints:

- Optimized sequence and its coding region
- CAI on the coding region
- 5' UTR, 3' UTR, and total non-coding substitution counts (positions where the optimized base differs from the original outside the coding region)