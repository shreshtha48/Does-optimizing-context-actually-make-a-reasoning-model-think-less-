# Does optimizing context make a reasoning model think less?

An empirical look at how **Gemini 3.1 Pro** spends its reasoning tokens when the same question is asked with three different qualities of context — across three very different document domains.

The short version: **it depends on the task.** Trimming the context to only what's needed makes the model reason *less* on retrieval-style tasks (finding a root cause in logs) but can make it reason *more* on interpretation-style tasks (reading an earnings call or a contract), where a fuller document actually helps. 
## The experiment

For each document we wrote questions that can't be answered by copying a single line — they need some reasoning or digging. Every question was then run under **three versions of the context**:

| Condition | What it is |
|---|---|
| **Tight** (`context`) | Only the context needed to answer the question. |
| **Bloated** (`full`) | The needed context buried in a lot of extra, irrelevant material. |
| **Adversarial** (`garbage`) | The needed context plus deliberately confusing, near-duplicate distractors. |

Everything ran on **Gemini 3.1 Pro** (`gemini-3.1-pro-preview`, Vertex AI) at two thinking settings (`low` / `high`), with multiple trials per combination averaged together. For every run we recorded input tokens, reasoning ("thinking") tokens, output tokens, cost, and latency. We did **not** grade answer correctness — this study is about *effort and cost*, not accuracy.

### Domains

| Domain | Folder | Sources |
|---|---|---|
| Company earnings calls | `code/earnings_call/` | AAON, AAPL, ACMR, AIRS, BMI |
| Cyber security logs | `code/cyber_loghub/` | Android, Hadoop, Windows |
| Legal / IP agreements | `code/legal_cuad/` | Adaptimmune, Armstrong, Buffalo Wild Wings |

## Repository layout

```
.
├── code/
│   ├── summary.py                 # runs.csv -> summary.csv + analysis/summary_stats.csv
│   ├── plot.py                    # per-question token plots (tokens_by_metric, token_stack)
│   ├── token_profile.py           # side exploration: cross-domain token profile (Anthropic)
│   ├── plots/                     # exported figures used in the article
│   │
│   ├── cyber_loghub/              # one folder per domain, same layout:
│   │   ├── prompts/<system>/qN_slug__{context,full,garbage}.md
│   │   └── results/
│   │       ├── runs.csv           #   one row per individual model run (raw)
│   │       ├── responses.jsonl    #   full model responses
│   │       ├── summary.csv        #   means per (question x condition x thinking level)
│   │       └── analysis/          #   summary_stats.csv + per-domain plots
│   ├── earnings_call/             # (prompts/<company>/..., same results/ layout)
│   └── legal_cuad/                # (prompts/<contract>/..., same results/ layout)

```

Each prompt file is named `qN_slug__<condition>.md`, where the condition is `context` (Tight), `full` (Bloated), or `garbage` (Adversarial). The prompt file holds the entire text sent to the model — there is no separate system prompt and no tools/retrieval.

## Reproducing the analysis and plots

The `results/` folders already contain the recorded runs, so you can regenerate every summary and figure without calling any model.

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate     |    macOS/Linux:  source .venv/bin/activate
pip install pandas numpy matplotlib

python code/summary.py           # rebuild summary.csv + analysis/summary_stats.csv
python code/plot.py              # per-question token figures
```

> **Note:** the runner that actually calls Gemini and writes `runs.csv` is not included in this repo; `results/runs.csv` and `results/responses.jsonl` are its recorded output. To re-run against the live model you'd point a Vertex AI client at each `prompts/**/**.md` file across the two thinking levels and log the `usage_metadata` token counts.

## Key results

- **The effect of bad context flips by domain.** For security logs, bloating or poisoning the context roughly *doubles* reasoning at the high thinking setting. For earnings and legal, more context often makes the model reason *less*.
- **The thinking budget is the biggest lever.** Going from `low` to `high` multiplies reasoning tokens by ~1.6–1.7× everywhere — more consistently than any context change.
- **Cost is driven by input tokens.** Bloating the context is expensive no matter what, because you pay for every input token; in the security logs it raises cost ~10× while doing nothing good for the model.


One model (Gemini 3.1 Pro), two thinking settings, a handful of questions per document — enough to see the big trends, not to make fine-grained claims. Reasoning-token counts are the model's own reported numbers, used as a proxy for effort, and no answer was graded for correctness. See the Limitations section of the article for the full list.
