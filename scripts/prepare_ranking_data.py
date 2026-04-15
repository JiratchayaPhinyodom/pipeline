import json
import numpy as np
from pathlib import Path

BASE = Path("../laura-baird-icse2026")

def extract_features(chain):
    cves = chain.get("cves", [])
    if not cves:
        return [0, 0, 0, 0]

    cvss = [c.get("cvss", 0) for c in cves]
    conf = [c.get("confidence", 0.5) for c in cves]

    return [
        np.mean(cvss),
        np.max(cvss),
        len(cves),
        np.mean(conf)
    ]

def heuristic_score(chain):
    cves = chain.get("cves", [])
    if not cves:
        return 0

    scores = [
        c.get("cvss", 0) * (0.7 + 0.3 * c.get("confidence", 0.5))
        for c in cves
    ]

    return np.mean(scores) + max(scores) + len(cves) * 0.5


with open(BASE / "outputs/attack_chains.json") as f:
    chains = json.load(f)

X, y = [], []

for chain in chains:
    X.append(extract_features(chain))
    y.append(heuristic_score(chain))

np.save(BASE / "outputs/X.npy", np.array(X))
np.save(BASE / "outputs/y.npy", np.array(y))

print("✅ Prepared ranking dataset")