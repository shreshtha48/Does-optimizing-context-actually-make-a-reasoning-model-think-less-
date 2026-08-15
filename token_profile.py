"""
First cross-domain token profile: input / output / (summarized) thinking tokens
for ONE model across the five domains.

Provider: Anthropic (Claude). NOTE on "reasoning tokens":
  Claude's usage.output_tokens is thinking+answer COMBINED. The raw chain of
  thought is never returned. With thinking display="summarized" we additionally
  record the token count of the *summary* and of the final answer separately so
  you can see roughly how the output splits — but the summary is NOT the true
  reasoning-token count. For an isolated reasoning-token figure, run an
  OpenAI o-series / Gemini / DeepSeek model instead (see note in chat).

Run:
  cd research
  .venv/Scripts/python.exe -m pip install anthropic      # one-time
  ANTHROPIC_API_KEY=...  (or ANTHROPIC_AUTH_TOKEN=...)    # must be set
  .venv/Scripts/python.exe code/token_profile.py
"""

from __future__ import annotations
import csv, glob, os, sys, pathlib
import anthropic

MODEL = os.environ.get("PROFILE_MODEL", "claude-opus-4-8")
DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
EC = pathlib.Path(__file__).resolve().parent / "earnings_call"

client = anthropic.Anthropic()  # resolves ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / base_url from env


def read(path, n=None, enc="utf-8"):
    with open(path, "r", encoding=enc, errors="replace") as f:
        return f.read() if n is None else f.read(n)


def count(text: str) -> int:
    return client.messages.count_tokens(
        model=MODEL, messages=[{"role": "user", "content": text or " "}]
    ).input_tokens


# --- Build one probe per domain (plus the 3 earnings conditions already on disk) ---
def build_probes():
    probes = []  # each: dict(domain, condition, system, user)

    SYS = ("You are an expert analyst. Answer the user's question based STRICTLY on the "
           "provided context. If the answer is not in the context, say so explicitly. Be concise.")

    # 1) EARNINGS — reuse the three prompt files verbatim (full / oracle / full+distractor)
    for cond, fn in [("full", "prompt.md"), ("oracle", "prompt_context.md"),
                     ("full+distractor", "prompt_garbage.md")]:
        p = EC / fn
        if p.exists():
            probes.append(dict(domain="earnings", condition=cond, system=None, user=read(p)))

    # 2) LEGAL (CUAD) — one full contract + a clause question
    txts = sorted(glob.glob(str(DATA / "legal_cuad/CUAD_v1/full_contract_txt/*.txt")))
    if txts:
        doc = read(txts[0])
        q = "What is the governing law / jurisdiction clause of this agreement? Quote it."
        probes.append(dict(domain="legal", condition="full",
                           system=SYS, user=f"<context>\n{doc}\n</context>\n\n<question>{q}</question>"))

    # 3) MEDICINE (LongHealth) — one patient's notes + one of its questions
    bj = DATA / "medicine_longhealth/repo/data/benchmark_v5.json"
    if bj.exists():
        import json
        d = json.load(open(bj, encoding="utf-8"))
        pid = list(d.keys())[0]
        pat = d[pid]
        notes = "\n\n".join(v for k, v in pat["texts"].items())
        qrow = pat["questions"][0]
        opts = "\n".join(f"{k}) {qrow[k]}" for k in ["answer_a", "answer_b", "answer_c", "answer_d", "answer_e"] if qrow.get(k))
        q = f"{qrow['question']}\n{opts}\nAnswer with the single correct option letter and a one-line justification."
        probes.append(dict(domain="medicine", condition="full",
                           system=SYS, user=f"<context>\n{notes}\n</context>\n\n<question>{q}</question>"))

    # 4) CYBER (LogHub HDFS sample) — a log slice + an anomaly question
    hd = DATA / "cyber_loghub/repo/HDFS/HDFS_2k.log"
    if hd.exists():
        log = read(hd)
        q = ("Scan this HDFS log. Are there any error, exception, or block-corruption events? "
             "If so, list each with its block id; if none, say 'no errors found'.")
        probes.append(dict(domain="cyber", condition="full",
                           system=SYS, user=f"<context>\n{log}\n</context>\n\n<question>{q}</question>"))

    # 5) BANK (Berka) — one account's transaction history + a balance question
    trans = DATA / "bank_berka/repo/trans.asc"
    if trans.exists():
        # pull all rows for the first account_id we see with >40 rows
        from collections import defaultdict
        rows = defaultdict(list)
        with open(trans, "r", encoding="latin-2", errors="replace") as f:
            header = f.readline().strip().split(";")
            for line in f:
                parts = line.rstrip("\n").split(";")
                if len(parts) < 7:
                    continue
                acc = parts[1]
                rows[acc].append(parts)
                if len(rows[acc]) > 120:  # cap one account, enough to be "long"
                    target = acc
                    break
        target = max(rows, key=lambda a: len(rows[a]))
        lines = [";".join(header)] + [";".join(r) for r in rows[target]]
        ledger = "\n".join(lines)
        q = (f"This is the transaction ledger for account {target} "
             "(columns: trans_id;account_id;date;type;operation;amount;balance;...). "
             "Did the running balance ever fall below 0? Give the lowest balance and its date.")
        probes.append(dict(domain="bank", condition="full",
                           system=SYS, user=f"<context>\n{ledger}\n</context>\n\n<question>{q}</question>"))

    return probes


def run_probe(pr):
    kwargs = dict(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive", "display": "summarized"},
        messages=[{"role": "user", "content": pr["user"]}],
    )
    if pr["system"]:
        kwargs["system"] = pr["system"]
    resp = client.messages.create(**kwargs)
    think = "".join(b.thinking for b in resp.content if b.type == "thinking")
    answer = "".join(b.text for b in resp.content if b.type == "text")
    u = resp.usage
    return dict(
        domain=pr["domain"], condition=pr["condition"],
        input_tokens=u.input_tokens,
        output_tokens=u.output_tokens,          # thinking + answer COMBINED
        think_summary_tokens=count(think),       # tokens of the SUMMARY (not true reasoning)
        answer_tokens=count(answer),
        stop=resp.stop_reason,
    )


def main():
    probes = build_probes()
    print(f"Model: {MODEL}  |  probes: {len(probes)}\n")
    out = []
    hdr = ["domain", "condition", "input_tokens", "output_tokens", "think_summary_tokens", "answer_tokens", "stop"]
    print("  ".join(f"{h:>20}" if h not in ('domain','condition') else f"{h:<16}" for h in hdr))
    for pr in probes:
        try:
            r = run_probe(pr)
        except Exception as e:
            print(f"{pr['domain']:<16}{pr['condition']:<16}  ERROR: {e}", file=sys.stderr)
            continue
        out.append(r)
        print(f"{r['domain']:<16}{r['condition']:<16}"
              f"{r['input_tokens']:>20}{r['output_tokens']:>20}"
              f"{r['think_summary_tokens']:>20}{r['answer_tokens']:>20}  {r['stop']}")
    csv_path = DATA / "token_profile.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr)
        w.writeheader()
        w.writerows(out)
    print(f"\nWrote {csv_path}")


if __name__ == "__main__":
    main()
