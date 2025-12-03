import json
from pathlib import Path

import pandas as pd


# ---------- 1. TruthfulQA → truthfulqa_small.json ----------

def prepare_truthfulqa():
    src = Path("data/hallucination/generation_validation.csv")
    if not src.exists():
        raise FileNotFoundError(f"TruthfulQA CSV not found at {src}")

    df = pd.read_csv(src)

    # Try to guess the right columns
    # Adjust these names if your columns are slightly different
    if "question" not in df.columns:
        raise ValueError(f"'question' column not found. Columns: {df.columns.tolist()}")

    # Pick a reasonable answer column
    answer_col_candidates = [
        "best_answer",
        "best_answer_text",
        "correct_answer",
        "answer",
    ]
    answer_col = None
    for c in answer_col_candidates:
        if c in df.columns:
            answer_col = c
            break

    if answer_col is None:
        raise ValueError(
            f"Could not find an answer column in {df.columns.tolist()}. "
            "Update prepare_truthfulqa() with your actual column name."
        )

    # Sample up to 150 questions
    n = min(150, len(df))
    subset = df.sample(n=n, random_state=42).reset_index(drop=True)

    records = []
    for i, row in subset.iterrows():
        records.append(
            {
                "id": f"tqa_{i}",
                "question": str(row["question"]),
                "true_answer": str(row[answer_col]),
                # dataset doesn’t really have a clean “false answer”; leave empty
                "false_answer": "",
            }
        )

    out_path = Path("data/hallucination/truthfulqa_small.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"[TruthfulQA] Wrote {len(records)} items to {out_path}")


# ---------- 2. CrowS-Pairs → crows_pairs_small.json ----------

def prepare_crows_pairs():
    src = Path("data/bias/crows_pairs_anonymized.csv")
    if not src.exists():
        raise FileNotFoundError(f"CrowS-Pairs CSV not found at {src}")

    df = pd.read_csv(src)

    required_cols = {"bias_type", "sent_more", "sent_less"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns {missing} in CrowS-Pairs CSV")

    n = min(200, len(df))
    subset = df.sample(n=n, random_state=42).reset_index(drop=True)

    records = []
    for i, row in subset.iterrows():
        records.append(
            {
                "id": f"crows_{i}",
                "bias_type": str(row["bias_type"]),
                # In CrowS-Pairs: sent_more = more stereotypical, sent_less = anti/less biased
                "stereotype_sentence": str(row["sent_more"]),
                "anti_stereotype_sentence": str(row["sent_less"]),
            }
        )

    out_path = Path("data/bias/crows_pairs_small.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"[CrowS-Pairs] Wrote {len(records)} items to {out_path}")


# ---------- 3. Jigsaw → jigsaw_toxic_small.csv ----------

def prepare_jigsaw():
    src = Path("data/safety/train.csv")
    if not src.exists():
        raise FileNotFoundError(f"Jigsaw train.csv not found at {src}")

    df = pd.read_csv(src)

    if "comment_text" not in df.columns:
        raise ValueError(f"'comment_text' column not found. Columns: {df.columns.tolist()}")

    toxicity_cols = [
        c
        for c in ["toxic", "severe_toxic", "obscene", "insult", "threat", "identity_hate"]
        if c in df.columns
    ]
    if not toxicity_cols:
        raise ValueError(
            "No standard Jigsaw toxicity columns found. "
            f"Columns are: {df.columns.tolist()}"
        )

    # Mark a comment as toxic if ANY of the toxicity labels is 1
    df["toxic_any"] = (df[toxicity_cols].sum(axis=1) > 0).astype(int)

    # Take a mix of toxic and non-toxic comments
    toxic_df = df[df["toxic_any"] == 1]
    clean_df = df[df["toxic_any"] == 0]

    toxic_n = min(250, len(toxic_df))
    clean_n = min(50, len(clean_df))

    subset = pd.concat(
        [
            toxic_df.sample(n=toxic_n, random_state=42),
            clean_df.sample(n=clean_n, random_state=43),
        ],
        ignore_index=True,
    )

    out_df = subset[["comment_text", "toxic_any"]].rename(columns={"toxic_any": "toxic"})

    out_path = Path("data/safety/jigsaw_toxic_small.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_path, index=False)
    print(f"[Jigsaw] Wrote {len(out_df)} rows to {out_path}")


if __name__ == "__main__":
    prepare_truthfulqa()
    prepare_crows_pairs()
    prepare_jigsaw()
    print("All subsets prepared.")
