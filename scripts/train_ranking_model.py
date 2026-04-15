import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path

BASE = Path("../laura-baird-icse2026")

X = np.load(BASE / "outputs/X.npy")
y = np.load(BASE / "outputs/y.npy")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X, y)

(Path(BASE / "outputs/models")).mkdir(parents=True, exist_ok=True)

joblib.dump(model, BASE / "outputs/models/ranking_model.pkl")

print("✅ Ranking model trained")