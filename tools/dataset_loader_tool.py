import json
from pathlib import Path
import pandas as pd
from tools.logging_tool import log_event

def load_truthfulqa_small(path: str = "data/hallucination/truthfulqa_small.json") -> list[dict]:
    p = Path(path)
    if not p.exists():
        log_event("dataset_loader", "TruthfulQA subset not found", {"path": path})
        return []
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    log_event("dataset_loader", "Loaded TruthfulQA subset", {"count": len(data)})
    return data

def load_crows_pairs_small(path: str = "data/bias/crows_pairs_small.json") -> list[dict]:
    p = Path(path)
    if not p.exists():
        log_event("dataset_loader", "CrowS-Pairs subset not found", {"path": path})
        return []
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    log_event("dataset_loader", "Loaded CrowS-Pairs subset", {"count": len(data)})
    return data

def load_jigsaw_toxic_small(path: str = "data/safety/jigsaw_toxic_small.csv") -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        log_event("dataset_loader", "Jigsaw toxic subset not found", {"path": path})
        return pd.DataFrame()
    df = pd.read_csv(p)
    log_event("dataset_loader", "Loaded Jigsaw toxic subset", {"rows": len(df)})
    return df
