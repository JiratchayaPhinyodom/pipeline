import json
from pathlib import Path
import random

BASE_DIR = Path("laura-baird-icse2026")
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "attack_chains_ranked.json"

# -----------------------------
# STEP 1: Load cascade-style pairs
# -----------------------------
def load_pairs():
    """
    TODO: Replace with real cascade predictions later.
    For now: simulate learned relationships.
    """
    return [
        ("CVE-2023-0001", "CVE-2023-0002", 0.92),
        ("CVE-2023-0002", "CVE-2023-0003", 0.85),
        ("CVE-2023-0003", "CVE-2023-0004", 0.40),
        ("CVE-2022-1111", "CVE-2022-2222", 0.78),
        ("CVE-2022-2222", "CVE-2022-3333", 0.81),
    ]

# -----------------------------
# STEP 2: Build chains
# -----------------------------
def build_chains(pairs):
    graph = {}
    for a, b, score in pairs:
        graph.setdefault(a, []).append((b, score))

    chains = []

    def dfs(node, path, scores):
        if node not in graph:
            chains.append({"chain": path, "scores": scores})
            return
        for next_node, s in graph[node]:
            dfs(next_node, path + [next_node], scores + [s])

    for start in graph:
        dfs(start, [start], [])

    return chains

# -----------------------------
# STEP 3: Risk scoring
# -----------------------------
def compute_risk(chain):
    if not chain["scores"]:
        return 0

    avg_prob = sum(chain["scores"]) / len(chain["scores"])
    length = len(chain["chain"])

    # Placeholder CVSS (later replace with real data)
    avg_cvss = random.uniform(7, 10)

    return avg_prob * length * avg_cvss

# -----------------------------
# STEP 4: Rank chains
# -----------------------------
def rank_chains(chains):
    ranked = []
    for c in chains:
        score = compute_risk(c)
        ranked.append({
            "chain": c["chain"],
            "length": len(c["chain"]),
            "risk_score": round(score, 4)
        })

    ranked.sort(key=lambda x: x["risk_score"], reverse=True)
    return ranked

# -----------------------------
# MAIN
# -----------------------------
def main():
    print("🔍 Building attack chains...")

    pairs = load_pairs()
    chains = build_chains(pairs)

    print(f"Total chains: {len(chains)}")

    ranked = rank_chains(chains)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(ranked, f, indent=2)

    print("✅ Ranking complete!")
    print("\nTop 5 chains:")
    print(json.dumps(ranked[:5], indent=2))


if __name__ == "__main__":
    main()