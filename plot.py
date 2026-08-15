from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE_DIR = Path(__file__).resolve().parent
TASKS = ["cyber_loghub", "earnings_call", "legal_cuad"]

METRICS = [("input_tokens", "#4C78A8"),
           ("output_tokens", "#F58518"),
           ("reasoning_tokens", "#54A24B")]


def plot_tokens(task: str) -> None:
    df = pd.read_csv(CODE_DIR / task / "results" / "analysis" / "summary_stats.csv")
    df["variant"] = df["prompt_type"].astype(str) + "/" + df["thinking_level"].astype(str)

    # lay out bars: a block of variants per question, with a gap between questions
    xs, bar_labels, rows = [], [], []
    grp_centers, grp_labels = [], []
    pos = 0
    for q in df["question_id"].drop_duplicates():
        sub = df[df["question_id"] == q].sort_values(["prompt_type", "thinking_level"])
        start = pos
        for _, r in sub.iterrows():
            xs.append(pos); bar_labels.append(r["variant"]); rows.append(r); pos += 1
        grp_centers.append((start + pos - 1) / 2); grp_labels.append(q)
        pos += 1  # gap before next question

    rows = pd.DataFrame(rows).reset_index(drop=True)
    x = np.array(xs)

    fig, axes = plt.subplots(len(METRICS), 1, figsize=(max(12, len(x) * 0.35), 11),
                             sharex=True)
    for ax, (metric, color) in zip(axes, METRICS):
        ax.bar(x, rows[f"{metric}_mean"], width=0.8, color=color,
               yerr=rows[f"{metric}_std"], capsize=2,            # std = sqrt(variance)
               error_kw={"elinewidth": 0.8, "ecolor": "#222"})
        ax.set_ylabel(metric)
        ax.grid(axis="y", alpha=0.3)

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels(bar_labels, rotation=90, fontsize=6)
    for c, l in zip(grp_centers, grp_labels):
        axes[-1].text(c, -0.28, l, transform=axes[-1].get_xaxis_transform(),
                      ha="center", va="top", fontsize=8, fontweight="bold")

    fig.suptitle(f"{task}: tokens per question/variant (error bars = std across trials)",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    out = CODE_DIR / task / "results" / "analysis" / "tokens_by_metric.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    for t in TASKS:
        plot_tokens(t)