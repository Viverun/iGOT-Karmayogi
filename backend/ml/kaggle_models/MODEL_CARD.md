# Model card — iGOT Competency Engine (Kaggle-trained)

## What these are
- `xgb_competency.ubj` — XGBoost regressor (300 trees, depth 6), 12 evidence
  features → 1–5 competency. Plus an XGB classifier head for gap-class
  (Critical / Moderate / No-Low) used only during training evaluation.
- `ncf_hybrid.pt` — Hybrid Neural CF (user/item embeddings 32-d + 5-feature
  content MLP), ranking with 2× hard-negative weighting.

Kaggle runs (Tesla T4, reproducible scripts in `backend/ml/kaggle_nb_*.py`):
- XGB: 220k rows, temporal holdout Aug-2026 — MAE 0.16 (baseline 0.69),
  R² 0.94, gap-class accuracy 90%, MAE 95% CI [0.159, 0.162].
- NCF: 160k examples, 8 epochs — AUC 0.61, HR@10 1.00, NDCG@10 0.87,
  diversity@5 0.73.

## Critical limitation: trained on SYNTHETIC data
Both artifacts were trained on generator-made data whose labels are smooth
functions of the input features. Real-learner metrics WILL be lower —
especially NCF AUC (0.61 even on synthetic is weak signal, not strong).
Treat every number above as a smoke test of the pipeline, not a claim.

## How the backend uses them (and does not)
- XGB output is blended **50/50 with measured EWMA evidence** — it can move a
  score, never set it. Readiness gates (30% cap, +14% per verified completion)
  are unchanged and model-independent.
- NCF blends **60% rules / 40% model** for ordering only; gaps, targets and
  explanations come from measured data.
- If artifacts or `torch` are missing, everything falls back to EWMA +
  rule-based + GPT/deterministic quizzes. No endpoint can 500 because of ML.
- Dashboard and admin analytics run the SAME blend core, so they agree.

## Retrain before any real deployment
Fine-tune on real `competency_evidence` (never on hidden `true_competency`),
recalibrate, and re-validate temporally. Then update this card.
