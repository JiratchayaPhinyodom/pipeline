import json
import numpy as np
import joblib
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

model = joblib.load(BASE / "outputs/models/ranking_model.pkl")

with open(BASE / "outputs/attack_chains.json") as f:
    chains = json.load(f)

for chain in chains:
    feat = np.array(extract_features(chain)).reshape(1, -1)
    chain["ml_risk_score"] = float(model.predict(feat)[0])

ranked = sorted(chains, key=lambda x: x["ml_risk_score"], reverse=True)

with open(BASE / "outputs/ranked_attack_chains_ml.json", "w") as f:
    json.dump(ranked, f, indent=2)

print("✅ ML ranking complete")