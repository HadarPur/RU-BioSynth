import csv
import os
import sys
from contextlib import contextmanager
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from toolscomparison.BioSynth.pipeline import run_biosynth
from toolscomparison.COSMO.pipeline import run_cosmo
from toolscomparison.DNAChisel.pipeline import run_dnachisel

GENES = [
    {
        "gene_dir": "cloning_example",
        "gene_name": "OQ689691.1",
        "pattern_file_name": "mcs_unwanted_patterns",
        "codon_usage_file_name": "codon_usage_ecoli",
        "species": "e_coli",
    },
    {
        "gene_dir": "maize_yeast_example",
        "gene_name": "SAUR11",
        "pattern_file_name": "ACE2_binding_patterns",
        "codon_usage_file_name": "codon_usage_s_cerevisiae",
        "species": "s_cerevisiae",
    },
    {
        "gene_dir": "maize_yeast_example",
        "gene_name": "SAUR40",
        "pattern_file_name": "ACE2_binding_patterns",
        "codon_usage_file_name": "codon_usage_s_cerevisiae",
        "species": "s_cerevisiae",
    },
]


@contextmanager
def chdir_to(path):
    original = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original)


def run_tool(tool_name, gene):
    tool_dir = REPO_ROOT / "toolscomparison" / tool_name
    with chdir_to(tool_dir):
        if tool_name == "BioSynth":
            return run_biosynth(
                gene["gene_dir"],
                gene["gene_name"],
                gene["pattern_file_name"],
                gene["codon_usage_file_name"],
            )
        if tool_name == "DNAChisel":
            return run_dnachisel(
                gene["gene_dir"],
                gene["gene_name"],
                gene["pattern_file_name"],
                gene["codon_usage_file_name"],
                gene["species"],
            )
        if tool_name == "COSMO":
            return run_cosmo(
                gene["gene_dir"],
                gene["gene_name"],
                gene["pattern_file_name"],
                gene["codon_usage_file_name"],
            )
        raise ValueError(f"Unknown tool: {tool_name}")


def main():
    tools = ["BioSynth", "DNAChisel", "COSMO"]
    rows = []

    for gene in GENES:
        for tool_name in tools:
            print(f"\n{'=' * 60}\nRunning {tool_name} on {gene['gene_name']}\n{'=' * 60}")
            try:
                result = run_tool(tool_name, gene)
            except Exception as e:
                print(f"{tool_name} failed on {gene['gene_name']}: {e}")
                rows.append({
                    "gene": gene["gene_name"],
                    "tool": tool_name,
                    "cai": "",
                    "non_coding_substitutions": "",
                    "all_patterns_removed": "",
                    "status": f"error: {e}",
                })
                continue

            if result is None:
                rows.append({
                    "gene": gene["gene_name"],
                    "tool": tool_name,
                    "cai": "",
                    "non_coding_substitutions": "",
                    "all_patterns_removed": "",
                    "status": "no result",
                })
                continue

            rows.append({
                "gene": gene["gene_name"],
                "tool": tool_name,
                "cai": f"{result['cai']:.4f}" if result.get("cai") is not None else "",
                "non_coding_substitutions": result["non_coding_substitutions"],
                "all_patterns_removed": result["all_patterns_removed"],
                "status": "ok",
            })

    out_file = REPO_ROOT / "toolscomparison" / "comparison_results.csv"
    fieldnames = ["gene", "tool", "cai", "non_coding_substitutions", "all_patterns_removed", "status"]
    with out_file.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote comparison results to {out_file}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
