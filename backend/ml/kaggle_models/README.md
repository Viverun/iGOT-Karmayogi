# Models Used

| Name of Model | Where it is used? | Why it is used? | What it does? |
|---|---|---|---|
| `xgb_competency.ubj` (XGBoost) | `backend/ml_scorers.py` -> `backend/gap_engine.py` -> Dashboard + Admin analytics (`GET /api/dashboard`) | To make skill scores stable when test/quiz data is noisy, blended 50/50 with real scores so it only helps, never decides alone. | Takes 12 evidence features (test, quiz, experience, etc.) and predicts skill level 1-5. |
| `ncf_hybrid.pt` (Hybrid NCF) | `backend/ml_scorers.py` -> `backend/gap_engine.py` -> Roadmap (`GET /api/roadmap`) | To order courses for each learner personally instead of same fixed list, blended 60% rules / 40% model for ordering only. | Takes user + course + 5 context features (gap fit, etc.) and gives 0-1 score for how useful that course is next. |

> Both run with safe fallback: no model/torch = EWMA + rule-based still works. Trained on synthetic data — see `MODEL_CARD.md`.
