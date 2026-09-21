"""ML scorers: Kaggle-trained XGBoost competency + Hybrid NCF ranker.

Primary path: use the trained artifacts when present.
Fallback path: existing infra — EWMA competency store + rule-based ranking,
and GPT (llm.py) for quizzes/chat. NOTHING here may raise: every public
helper returns None / falls back on any failure (missing files, missing
optional deps like torch, corrupt weights).

Artifacts (committed under backend/ml/kaggle_models/):
  xgb_competency.ubj  — XGBRegressor, 12 features (see XGB_FEATS), target 1-5
  ncf_hybrid.pt       — HybridNCF state_dict (n_u=8000, n_c=120, d=32)

Environment override (tests / Render Disk):
  ML_MODELS_DIR  — directory holding the two artifact files.
"""
import os
import zlib
from pathlib import Path

MODELS_DIR = Path(os.environ.get(
    "ML_MODELS_DIR",
    Path(__file__).parent / "ml" / "kaggle_models",
))

XGB_FEATS = [
    "required_level", "assessment_score", "quiz_score", "practical_score",
    "assessment_reliability", "evidence_completeness", "evidence_count",
    "evidence_confidence", "recency_weight", "experience_years",
    "skill_id", "role_id",
]

NCF_CTX = ["gap_alignment_score", "prerequisite_fit", "expected_gain",
           "completion_probability", "novelty"]
NCF_N_U, NCF_N_C, NCF_D = 8000, 120, 32

_XGB = {"booster": None, "tried": False}
_NCF = {"model": None, "tried": False}


def _load_xgb():
    if _XGB["tried"]:
        return _XGB["booster"]
    _XGB["tried"] = True
    try:
        import xgboost as xgb
        path = MODELS_DIR / "xgb_competency.ubj"
        if not path.exists():
            return None
        booster = xgb.Booster()
        booster.load_model(str(path))
        _XGB["booster"] = booster
    except Exception as e:
        print("ml_scorers: xgb unavailable, EWMA fallback:", e)
    return _XGB["booster"]


def xgb_available() -> bool:
    return _load_xgb() is not None


def predict_competency(evidence: dict) -> float | None:
    """Predict 1-5 competency from a 12-feature evidence dict. None on failure."""
    booster = _load_xgb()
    if booster is None:
        return None
    try:
        import xgboost as xgb
        row = [float(evidence.get(f, 0)) for f in XGB_FEATS]
        dm = xgb.DMatrix([row], feature_names=XGB_FEATS)
        return float(booster.predict(dm)[0])
    except Exception as e:
        print("ml_scorers: xgb predict failed, fallback:", e)
        return None


def reset_cache():
    """Test hook: forget loaded models so a new ML_MODELS_DIR takes effect."""
    _XGB.update(booster=None, tried=False)
    _NCF.update(model=None, tried=False)
    global MODELS_DIR
    MODELS_DIR = Path(os.environ.get(
        "ML_MODELS_DIR",
        Path(__file__).parent / "ml" / "kaggle_models",
    ))


# ---------- NCF (torch optional) ----------

def _ncf_model():
    if _NCF["tried"]:
        return _NCF["model"]
    _NCF["tried"] = True
    try:
        import torch
        import torch.nn as nn

        class HybridNCF(nn.Module):
            def __init__(self, n_u=NCF_N_U, n_c=NCF_N_C, d=NCF_D):
                super().__init__()
                self.u = nn.Embedding(n_u, d)
                self.c = nn.Embedding(n_c, d)
                self.mlp = nn.Sequential(
                    nn.Linear(d * 2 + 5, 64), nn.ReLU(), nn.Dropout(.2),
                    nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1))

            def forward(self, u, c, x):
                return self.mlp(torch.cat([self.u(u), self.c(c), x], 1)).squeeze(1)

        path = MODELS_DIR / "ncf_hybrid.pt"
        if not path.exists():
            return None
        model = HybridNCF()
        model.load_state_dict(torch.load(str(path), map_location="cpu"))
        model.eval()
        _NCF["model"] = model
    except Exception as e:
        print("ml_scorers: ncf unavailable, rule-based fallback:", e)
    return _NCF["model"]


def ncf_available() -> bool:
    return _ncf_model() is not None


def stable_idx(key: str, mod: int) -> int:
    return zlib.crc32(str(key).encode()) % mod


def _stable_idx(key: str, mod: int) -> int:
    return stable_idx(key, mod)


def ncf_score(user_id: int, course_key: str, ctx: dict) -> float | None:
    """0-1 recommendation score for (user, course). None on any failure."""
    model = _ncf_model()
    if model is None:
        return None
    try:
        import torch
        with torch.no_grad():
            u = torch.tensor([int(user_id) % NCF_N_U], dtype=torch.long)
            c = torch.tensor([stable_idx(course_key, NCF_N_C)], dtype=torch.long)
            x = torch.tensor([[float(ctx.get(k, 0.5)) for k in NCF_CTX]],
                             dtype=torch.float32)
            return float(torch.sigmoid(model(u, c, x)).item())
    except Exception as e:
        print("ml_scorers: ncf score failed, fallback:", e)
        return None


def status() -> dict:
    """Which engine serves each surface — and what the fallback is."""
    try:
        import llm
        llm_on = llm.llm_available()
    except Exception:
        llm_on = False
    xgb_on = xgb_available()
    ncf_on = ncf_available()
    return {
        "competency_primary": "xgboost" if xgb_on else "ewma",
        "competency_fallback": "ewma",
        "ranking_primary": "hybrid-ncf" if ncf_on else "rule-based",
        "ranking_fallback": "rule-based",
        "quiz_chat_primary": "llm(gpt)" if llm_on else "deterministic-fallback",
        "quiz_chat_fallback": "deterministic-fallback",
        # Honesty: both artifacts trained on SYNTHETIC data (see
        # backend/ml/kaggle_models/MODEL_CARD.md). Treat scores as
        # decision support blended with measured evidence — never sole truth.
        "training_data": "synthetic",
        "blend": "ml 50/50 with measured evidence; readiness gates unchanged",
        "models": {
            "xgb": {"available": xgb_on,
                    "path": str(MODELS_DIR / "xgb_competency.ubj")},
            "ncf": {"available": ncf_on,
                    "path": str(MODELS_DIR / "ncf_hybrid.pt")},
            "llm": {"available": llm_on},
        },
    }
