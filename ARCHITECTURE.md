# BioSynth — Architecture & Pipeline

This document describes the internal design of BioSynth: the algorithmic
core, the agent-based pipeline, the GUI/CLI entry points, and how state
flows from a raw input file to a rendered HTML report. For installation
and usage instructions see [README.md](README.md).

---

## Table of contents

1. [Overview](#1-overview)
2. [The pipeline at a glance](#2-the-pipeline-at-a-glance)
3. [Package layout](#3-package-layout)
4. [Algorithmic core](#4-algorithmic-core)
   - [FSM construction](#41-fsm-construction-biosynthalgorithmfsmpy)
   - [DP elimination](#42-dp-elimination-biosynthalgorithmelimination_controllerpy)
   - [Cost model](#43-cost-model-biosynthutilscost_utilspy)
5. [Agent architecture](#5-agent-architecture)
   - [Base class & errors](#51-base-class-and-errors-biosynthagentsbasepy)
   - [Typed messages](#52-typed-messages-biosynthagentsmessagespy)
   - [The five agents](#53-the-five-agents)
   - [Pipeline orchestrator](#54-pipeline-orchestrator-biosynthagentspipelinepy)
6. [Entry points](#6-entry-points)
   - [CLI](#61-cli)
   - [GUI](#62-gui)
   - [Debug runner](#63-debug-runner)
7. [GUI architecture](#7-gui-architecture)
8. [Application-wide state](#8-application-wide-state)
9. [End-to-end run trace](#9-end-to-end-run-trace)
10. [Testing strategy](#10-testing-strategy)
11. [Extending the pipeline](#11-extending-the-pipeline)
12. [Glossary](#12-glossary)

---

## 1. Overview

BioSynth designs synthetic DNA sequences that **avoid a user-supplied
list of unwanted patterns** (e.g. restriction sites, immunogenic motifs)
while **respecting the codon-usage bias** of a target organism. The
optimization is exact: a finite-state machine over the pattern set is
combined with dynamic programming to find the minimum-cost edited
sequence under a configurable substitution-cost model.

The codebase has three execution surfaces — a CLI, a PyQt5 GUI, and a
debug runner — all of which drive the same internal pipeline of five
cooperating agents.

---

## 2. The pipeline at a glance

```
                ┌──────────────────────────────────────┐
                │  Inputs (sequence, patterns, codon   │
                │  usage table, α/β/w, optimized_codon)│
                └──────────────────┬───────────────────┘
                                   │
                       ┌───────────▼──────────┐
                       │   PreflightAgent     │  non-empty sequence check
                       └───────────┬──────────┘
                                   │
                       ┌───────────▼──────────┐
                       │  CodingRegionAgent   │  start-codon discovery
                       └───────────┬──────────┘  + per-position phase tagging
                                   │
                       ┌───────────▼──────────┐
                       │  EliminationAgent    │  FSM + DP optimization
                       └───────────┬──────────┘  (the deterministic core)
                                   │
                       ┌───────────▼──────────┐
                       │     ReportAgent      │  render HTML via Jinja2,
                       └───────────┬──────────┘  copy to output dir
                                   │
                       ┌───────────▼──────────┐
                       │  SaveArtifactsAgent  │  optimized seq +
                       └───────────┬──────────┘  cost-contribution +
                                   │             cost-substitution
                                   ▼
                         PipelineResult dataclass
```

Each arrow is a typed dataclass message; each box is an
[`Agent[InputT, OutputT]`](biosynth/agents/base.py) subclass.

The orchestrator that chains them (`Pipeline`) is in
[`biosynth/agents/pipeline.py`](biosynth/agents/pipeline.py). The CLI's
`CommandController` invokes the agents directly (rather than via
`Pipeline.run`) so it can interleave terminal output between stages
and wrap **only** the heavy `EliminationAgent` in a busy spinner.

---

## 3. Package layout

```
biosynth/
├── __main__.py                      # python -m biosynth → app.main
├── app.py                           # entry: dispatches CLI vs GUI
├── app-debug.py                     # debug script (runs both modes)
│
├── algorithm/                       # deterministic algorithmic core
│   ├── fsm.py                       # KMP-based FSM over pattern set
│   └── elimination_controller.py    # FSM + DP minimum-cost edit
│
├── agents/                          # multi-agent pipeline layer
│   ├── base.py                      # Agent ABC + AgentError
│   ├── messages.py                  # typed Request/Result dataclasses
│   ├── preflight_agent.py
│   ├── coding_region_agent.py
│   ├── elimination_agent.py
│   ├── report_agent.py
│   ├── save_artifacts_agent.py
│   └── pipeline.py                  # linear orchestrator
│
├── data/
│   └── app_data.py                  # module-globals: InputData / CostData /
│                                    # UploadData / EliminationData / OutputData
│
├── executions/
│   ├── execution_utils.py           # is_valid_* validators + helpers
│   └── controllers/
│       ├── cli_controller.py        # CLI entry: parses argv, populates
│       │                            #   InputData/CostData, dispatches
│       │                            #   CommandController
│       ├── command_controller.py    # CLI orchestrator (runs the agents)
│       ├── debug_controller.py      # debug entry: hard-coded inputs
│       ├── gui_controller.py        # GUI entry: launches PyQt5 wizard
│       └── ui/                      # PyQt5 widgets, windows, theme — see §7
│
├── report/
│   ├── report_controller.py         # Jinja2-based HTML report builder
│   └── report.html                  # Jinja2 template
│
├── settings/                        # sample inputs for the debug runner
│   ├── codon_usage_settings.py
│   ├── pattern_settings.py
│   └── sequence_settings.py
│
├── utils/                           # small, focused helpers
│   ├── amino_acid_utils.py          # codon → amino-acid table + helpers
│   ├── argument_parser.py           # argparse wrapper (was input_utils)
│   ├── cost_utils.py                # substitution cost computations +
│   │                                #   CAI normalisation
│   ├── date_utils.py                # human-readable date formatter
│   ├── dna_utils.py                 # start-codon discovery, coding phase
│   ├── file_utils.py                # readers for the 3 input files,
│   │                                #   save_file helper
│   ├── info_utils.py                # help/info text blocks
│   ├── logger.py                    # ANSI-coloured Logger (was output_utils)
│   ├── sequence_display.py          # SequenceUtils — highlight / diff render
│   │                                #   (was display_utils)
│   ├── spinner.py                   # terminal busy indicator (Braille)
│   ├── table_test_runner.py         # tabulated unittest runner
│   │                                #   (was test_utils)
│   └── text_utils.py                # OutputFormat enum + critical-error
│                                    #   handler
│
└── tests/                           # pytest suite, mirrors source layout
    ├── test_<source-module>.py …
```

---

## 4. Algorithmic core

### 4.1 FSM construction ([biosynth/algorithm/fsm.py](biosynth/algorithm/fsm.py))

`kmp_based_fsm_bigram(unwanted_patterns, sigma)` builds an Aho-Corasick-
style finite-state machine whose states are **bigrams of the DNA
alphabet** (`{AA, AC, AG, AT, CA, …, TT}`) plus longer prefixes of
unwanted patterns.

- `f(state, symbol)` returns the next state, or `None` if extending
  with this symbol would form a complete unwanted pattern (the
  "forbidden transition").
- `g(state)` is the standard KMP failure function used during BFS
  construction.
- After construction, all single-character states and `epsilon` are
  pruned and every bigram is added so the DP table is well-formed.

`FSM(unwanted_patterns, alphabet)` is the thin class wrapper used by
`EliminationController`.

### 4.2 DP elimination ([biosynth/algorithm/elimination_controller.py](biosynth/algorithm/elimination_controller.py))

`EliminationController.eliminate(...)` runs the dynamic program:

```
A[(i, v)] = minimum total cost of any optimized prefix of length i
            that ends in FSM state v
A_star[(i, v)] = backpointer (best prev state and chosen symbol σ)
```

The recurrence:

```
A[(i, v)] = min over (u, σ) with f(u, σ) = v of:
            A[(i-1, u)] + cost(σ at position i)
```

`cost(...)` is computed by `EliminationScorerConfig.cost_function`
(see §4.3). After the table is filled the minimum-cost final state is
chosen and the sequence is reconstructed by walking `A_star` backwards.

The function accepts cost parameters either as keyword args (used by
`EliminationAgent`) or, when omitted, reads them from `CostData`
globals (used by the legacy CLI/GUI paths). The signature was
intentionally widened to enable the agent design without breaking any
existing call site.

### 4.3 Cost model ([biosynth/utils/cost_utils.py](biosynth/utils/cost_utils.py))

For a proposed nucleotide `σ` at position `i`:

| Region                | Cost                                                |
| --------------------- | --------------------------------------------------- |
| Non-coding, no change | `0`                                                 |
| Non-coding, A↔G / C↔T | `α` (transition)                                    |
| Non-coding, other     | `β` (transversion)                                  |
| Coding, codon pos 1/2 | `0` (handled when position 3 of the codon arrives)  |
| Coding, codon pos 3, same codon                                   | `0` (when `optimized_codon=False`) |
| Coding, codon pos 3, synonymous swap                              | `−log(relative_adaptiveness)` from `normalize_codon_usage` |
| Coding, position 3, start codon (`-3`) or stop-codon formation    | `∞` (forbidden) |
| Coding, position 3, non-synonymous swap                           | `w + edit_distance(target_codon, proposed_codon)` |

`normalize_codon_usage(codon_freqs)` converts raw frequencies to a CAI
(Codon Adaptation Index) cost: each codon's frequency is divided by the
maximum frequency among its synonyms, and the result is mapped to cost
space via `−log(adaptiveness)`. Rare codons → high cost.

The cost-model defaults are:

| Symbol             | Default | Meaning                                  |
| ------------------ | ------- | ---------------------------------------- |
| `α` (alpha)        | `1.0`   | Transition substitution in non-coding    |
| `β` (beta)         | `2.0`   | Transversion substitution in non-coding  |
| `w`                | `100.0` | Non-synonymous substitution in coding    |
| `optimized_codon`  | `True`  | Allow drift to higher-CAI synonymous codons even if input codon matches |

`is_valid_cost` in `execution_utils.py` enforces `α < β` and
`β·10 < w` as biological sanity checks.

---

## 5. Agent architecture

The pipeline that drives a single BioSynth run is decomposed into
**five typed, cooperating agents**. Each agent is a deterministic
pipeline stage with an explicit message contract — no LLMs, no
autonomy. The decomposition makes each stage independently testable,
swappable, and instrumentable.

### 5.1 Base class and errors ([biosynth/agents/base.py](biosynth/agents/base.py))

```python
class Agent(ABC, Generic[InputT, OutputT]):
    name: str = "agent"

    @abstractmethod
    def handle(self, request: InputT) -> OutputT: ...


class AgentError(Exception):
    def __init__(self, code: int, message: str): ...
```

- `Agent` is a generic, stateless ABC. The `name` attribute identifies
  the stage for progress callbacks.
- `AgentError.code` carries the process exit code the orchestrator
  passes to `sys.exit` so legacy CLI contract is preserved
  (`exit(3)` for empty / malformed sequence, etc.).

### 5.2 Typed messages ([biosynth/agents/messages.py](biosynth/agents/messages.py))

All inter-agent messages are **frozen dataclasses**. For every stage
there is a `*Request` (input) and a `*Result` (output), plus a
top-level `PipelineRequest` / `PipelineResult` envelope.

This ensures:

- Inputs to each stage are explicit (no hidden global reads inside
  the agent).
- Messages can be passed across threads/processes safely.
- Static analysers and IDEs autocomplete the available fields.

### 5.3 The five agents

| Agent                  | File                                                                                                        | Wraps                                                                                                                  | On failure              |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| **PreflightAgent**     | [`agents/preflight_agent.py`](biosynth/agents/preflight_agent.py)                                            | non-empty sequence check                                                                                              | `AgentError(code=3)`    |
| **CodingRegionAgent**  | [`agents/coding_region_agent.py`](biosynth/agents/coding_region_agent.py)                                    | `DNAUtils.find_start_codon` + `get_coding_and_non_coding_regions_positions`                                          | `AgentError(code=3)` on malformed `*ATG` marker |
| **EliminationAgent**   | [`agents/elimination_agent.py`](biosynth/agents/elimination_agent.py)                                        | `EliminationController.eliminate` (with explicit cost params, no global reads)                                       | propagates as-is        |
| **ReportAgent**        | [`agents/report_agent.py`](biosynth/agents/report_agent.py)                                                  | `ReportController` (with explicit data kwargs); calls `create_report` then `download_report`                          | propagates as-is        |
| **SaveArtifactsAgent** | [`agents/save_artifacts_agent.py`](biosynth/agents/save_artifacts_agent.py)                                  | `save_file` for a batch of `filename → text` artifacts                                                                | returns saved paths     |

Each agent is **pure** with respect to its inputs — it does not read
from or write to the `app_data` globals. The boundary that bridges
the typed-message world back to globals lives in `CommandController`
(see §6.1 and §8).

### 5.4 Pipeline orchestrator ([biosynth/agents/pipeline.py](biosynth/agents/pipeline.py))

```python
class Pipeline:
    def __init__(self, *, preflight=None, coding_region=None,
                 elimination=None, report=None, save=None): ...

    def run(self, request: PipelineRequest, *,
            on_step: Callable[[str, object], None] = None) -> PipelineResult: ...
```

- Default constructor wires the production agents. Pass your own
  instances for tests or alternative implementations.
- `run` chains the agents linearly, threading each stage's result into
  the next.
- An optional `on_step(stage_name, payload)` callback fires after every
  stage — useful for progress UIs or logging.
- `Pipeline.run` is suitable for one-shot end-to-end use (the GUI
  worker thread, tests, scripts). The CLI prefers to call the agents
  directly so it can interleave Logger output between stages.

---

## 6. Entry points

### 6.1 CLI

```
$ biosynth -s seq.txt -p patterns.txt -c codon_usage.txt
           [-a α] [-b β] [-w W] [-oc true|false] [-o output_dir]
```

Flow:

1. **`biosynth/__main__.py:main`** receives `sys.argv` and forwards to
   `BioSynthApp.execute` in [`biosynth/app.py`](biosynth/app.py).
2. **`BioSynthApp.execute`** wipes the local `output/` cache, parses
   the args, picks CLI vs GUI mode (`-g` flag), and dispatches.
3. **`CLIController.execute`** ([`controllers/cli_controller.py`](biosynth/executions/controllers/cli_controller.py))
   reads the three input files via `SequenceReader`/`PatternReader`/
   `CodonUsageReader`, validates them via `is_valid_input`/`is_valid_cost`,
   normalizes the codon table via `normalize_codon_usage`, populates
   `InputData` / `CostData` / `OutputData`, then constructs and runs a
   **`CommandController`**.
4. **`CommandController.run`** ([`controllers/command_controller.py`](biosynth/executions/controllers/command_controller.py))
   is the CLI's orchestrator. It owns one instance of each agent and
   invokes them directly (not via `Pipeline.run`) so it can:
   - print the banner, target-sequence highlight, and patterns list
     *before* the elimination spinner starts;
   - wrap *only* `EliminationAgent.handle` in `run_with_spinner`;
   - mirror each agent's result back into `app_data` globals for any
     downstream reader (notably the GUI worker thread, which still
     reads `EliminationData` / `OutputData` directly).

### 6.2 GUI

```
$ biosynth -g
```

Flow:

1. `BioSynthApp.execute` sets `OutputFormat.GUI` and constructs
   `GUIController().execute()`.
2. **`GUIController.execute`** ([`controllers/gui_controller.py`](biosynth/executions/controllers/gui_controller.py))
   creates a `QApplication`, instantiates a `BaseWindow` (the wizard
   shell), applies the global QSS, and enters the Qt event loop.
3. **`BaseWindow`** ([`controllers/ui/windows/base_window.py`](biosynth/executions/controllers/ui/windows/base_window.py))
   manages a `QStackedWidget` and four wizard pages:
   `UploadWindow → SettingsWindow → EliminationWindow → ResultsWindow`.
4. On `Next` from `SettingsWindow`, `BaseWindow` shows a modal
   `BusyDialog` and spins up an `EliminationWorker` on a background
   `QThread`. The worker calls `eliminate_unwanted_patterns` (which
   internally uses the same `EliminationController` as the agent
   pipeline). On `finished` the dialog closes and `EliminationWindow`
   is shown with the results.

The wizard pages, custom widgets, theme tokens, and QSS factories all
live under `executions/controllers/ui/`. See §7.

### 6.3 Debug runner

`DebugController.execute()` ([`controllers/debug_controller.py`](biosynth/executions/controllers/debug_controller.py))
uses the example fixtures in `biosynth/settings/` (`S`, `P`, `C`),
sets canonical cost parameters (`α=1.02`, `β=1.98`, `w=99.96`), and
runs `CommandController` **twice** — once with `optimized_codon=False`,
once with `True`. It's a developer tool for sanity-checking the
pipeline against the bundled samples; not exposed via a CLI flag.

---

## 7. GUI architecture

```
executions/controllers/ui/
├── windows/              # the 4 wizard pages + WizardPage base + BaseWindow
│   ├── base_window.py        # wizard shell (QMainWindow + QStackedWidget)
│   ├── wizard_page.py        # WizardPage(QWidget) base class — Back / Next
│   │                         #   layout scaffolding shared by step pages
│   ├── upload_window.py      # step 1: file drop + cost spinboxes
│   ├── settings_window.py    # step 2: confirm parsed sequence + patterns
│   ├── elimination_window.py # step 3: shows elimination log
│   └── results_window.py     # step 4: diff view + save / preview buttons
│
├── widgets/              # reusable Qt widgets
│   ├── custom_widgets.py     # ToggleSwitch, CircularButton, DropTextEdit,
│   │                         #   DropTableWidget, FloatingScrollIndicator
│   ├── busy_dialog.py        # modal indeterminate progress dialog
│   └── info_dialog.py        # tabbed help dialog (used by Upload + Results)
│
├── theme/                # design tokens + QSS factories
│   ├── tokens.py             # Colors / Fonts / Sizes / Margins / Labels /
│   │                         #   Titles dataclasses — single source of truth
│   └── styles.py             # QSS strings built from tokens
│
├── utils/                # layout helpers + Qt-side glue
│   ├── factories.py          # add_button, add_spinbox, create_scroll_area,
│   │                         #   create_table_from_data, add_drop_text_edit,
│   │                         #   add_drop_table, add_text_edit_html, …
│   ├── file_actions.py       # download / save-as / copy callbacks
│   ├── validation.py         # GuiValidator wrapping is_valid_*
│   │                         #   with QMessageBox feedback
│   └── elimination_worker.py # QObject worker that runs the elimination
│                             #   off the UI thread (signals: finished/failed)
│
└── window_utils.py       # backward-compat re-export shim — older imports
                          #   like `from ui.window_utils import add_button`
                          #   still work via this module
```

**Threading.** The elimination algorithm runs on a `QThread` to keep
the UI responsive. `BaseWindow.switch_to_elimination_window`:

1. Opens a modal `BusyDialog`.
2. Creates an `EliminationWorker` (a `QObject` that calls
   `eliminate_unwanted_patterns`), moves it to a new `QThread`.
3. Connects `worker.finished` → close dialog, show
   `EliminationWindow`.
4. Connects `worker.failed` → close dialog, show
   `QMessageBox.critical`.

---

## 8. Application-wide state

`biosynth/data/app_data.py` defines five module-level singletons that
act as the **runtime state bus** for legacy callers (CLI/GUI helpers
and Logger output). Each is a class with class-level attributes and a
`reset()` classmethod:

| Class              | Holds                                                                                |
| ------------------ | ------------------------------------------------------------------------------------ |
| `InputData`        | raw + cleaned DNA sequence, unwanted patterns set, start codon index, coding phases |
| `UploadData`       | unvalidated file content during GUI upload, before promotion to `InputData`         |
| `CostData`         | α, β, w, optimized_codon, codon usage table, codon usage filename                   |
| `EliminationData`  | elimination info log, cost contribution list, cost substitution list, min cost      |
| `OutputData`       | optimized sequence, output directory (`Path.home() / "Downloads"` by default)       |

**Why globals?** They predate the agent decomposition. Wholesale
removal would touch the GUI extensively. The agent design avoids
*reading* globals (each agent's request carries everything it needs),
and `CommandController.run` is the boundary that **writes** the
agents' results back to `EliminationData` / `OutputData` /
`InputData` so downstream readers (especially the GUI) keep working
unchanged.

`EliminationController.eliminate` and `ReportController.__init__`
**accept explicit kwargs** for all required state and **fall back to
the globals** when omitted. The agents always pass explicit values.

---

## 9. End-to-end run trace

For `biosynth -s seq.txt -p patterns.txt -c codon_usage.txt`:

```
__main__.main()
└─ app.BioSynthApp.execute(argv)
   ├─ delete_dir('output')            (clear local cache)
   ├─ ArgumentParser.parse_args(argv)
   ├─ set_output_format(TERMINAL)
   └─ CLIController(argv).execute()
      ├─ SequenceReader / PatternReader / CodonUsageReader  → raw inputs
      ├─ is_valid_input(seq, patterns, codon_usage)
      ├─ is_valid_cost(α, β, w)
      ├─ normalize_codon_usage(raw_codon_table)             → CAI costs
      ├─ InputData.* = …  CostData.* = …  OutputData.* = …
      └─ CommandController().run()
         ├─ Logger.notice(banner)
         ├─ PreflightAgent.handle(PreflightRequest)
         │      └─ (sequence non-empty?)                    ─┐ AgentError → sys.exit(3)
         ├─ CodingRegionAgent.handle(CodingRegionRequest)    │
         │      ├─ DNAUtils.find_start_codon                 │
         │      └─ DNAUtils.get_coding_and_non_coding_regions_positions
         │           sync coding_* → InputData
         ├─ Logger: target sequence (highlighted) + unwanted patterns
         ├─ run_with_spinner(
         │      "Computation in progress …",
         │      EliminationAgent.handle, EliminationRequest)
         │      └─ EliminationController.eliminate
         │            ├─ FSM(unwanted_patterns, alphabet)
         │            ├─ DP table fill (O(n·|V|²·|Σ|))
         │            └─ backtrack
         │           sync elim_* → EliminationData / OutputData
         ├─ Logger: elimination info + optimized sequence + tabulated
         │          cost contribution + cost substitution
         ├─ ReportAgent.handle(ReportRequest)
         │      └─ ReportController(…).create_report(date) + download_report(output_path)
         └─ SaveArtifactsAgent.handle(SaveArtifactsRequest)
                └─ save_file(...)  for optimized seq + 2 cost tables
            Logger: paths
```

Outputs land under `OutputData.output_path / BioSynth-Outputs/`:

```
BioSynth-Report_<date>.html
Optimized-Sequence_<date>.txt
Cost-Contribution_<date>.txt
Cost-Substitution_<date>.txt
```

---

## 10. Testing strategy

- **`biosynth/tests/`** is a pytest suite mirroring the source layout
  one-test-file-per-module.
- The agent layer (`biosynth/agents/*` + `command_controller.py`) is at
  **100 % statement coverage**.
- Tests use `unittest.TestCase` + `unittest.mock.patch` for isolation.
- The `Pipeline` tests demonstrate the agent-injection pattern:
  passing fake agents to `Pipeline(preflight=Fake…, …)` lets a test
  drive the orchestrator without touching the algorithm.
- CI (`tox`) installs via `poetry install --with dev` and runs the
  suite plus `coverage`.

Run locally:

```bash
pytest biosynth/tests
# or with coverage:
tox -e coverage
```

---

## 11. Extending the pipeline

**Adding a new stage** (e.g. a `LintAgent` between coding region and
elimination):

1. Define `LintRequest` / `LintResult` dataclasses in
   [`biosynth/agents/messages.py`](biosynth/agents/messages.py).
2. Implement `LintAgent(Agent[LintRequest, LintResult])` in a new
   file under `biosynth/agents/`.
3. Re-export from [`biosynth/agents/__init__.py`](biosynth/agents/__init__.py).
4. Plug into `Pipeline.run` (or extend `CommandController.run` if the
   CLI presentation needs interleaving).

**Swapping an implementation**:

```python
class StrictPreflightAgent(Agent):
    name = "preflight"
    def handle(self, request):
        # tighter rules here
        ...

pipeline = Pipeline(preflight=StrictPreflightAgent())
```

**Adding a new cost-model parameter**: thread it through
`PipelineRequest`, `EliminationRequest`, the widened
`EliminationController.eliminate(...)` kwargs, the `CostData` dataclass,
and the CLI flag in `argument_parser.py`. Existing callers that don't
pass it will fall back to the `CostData` default.

**Adding a new GUI page**: subclass `WizardPage` in
`biosynth/executions/controllers/ui/windows/`, implement
`build_body(layout)`, register navigation methods on `BaseWindow`.

---

## 12. Glossary

| Term                          | Meaning                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **FSM**                       | Finite-state machine over DNA bigrams; rejects transitions that would complete an unwanted pattern.           |
| **DP table** `A[(i, v)]`      | Minimum total cost of an optimized prefix of length `i` ending in FSM state `v`.                              |
| **CAI**                       | Codon Adaptation Index. Per-codon adaptiveness = `freq / max_freq_among_synonyms`. Cost = `−log(adaptiveness)`. |
| **Transition** vs **transversion** | Transitions = A↔G, C↔T (cost α). Transversions = anything else (cost β).                              |
| **Coding phase**              | 0 = non-coding, 1/2/3 = codon position (3rd base is where codon-level decisions are made). `−3` marks the start codon. |
| **`*ATG`**                    | Marker in the input sequence indicating the start codon of the coding region.                                 |
| **`optimized_codon`**         | When `True`, the DP may swap a coding-region codon for a higher-CAI synonym even if no unwanted pattern would otherwise be formed. |
| **Agent**                     | Here: a typed, stateless pipeline stage implementing the `Agent` ABC. Not an LLM.                             |
| **app_data globals**          | Module-level state classes (`InputData`, `CostData`, …) used by legacy callers as a runtime data bus.         |

---

*For installation and usage instructions, see [README.md](README.md).*
