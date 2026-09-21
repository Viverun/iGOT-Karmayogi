# iGOT Competency Engine — XGBoost (temporal validation, calibration, SHAP, CI)
# Kaggle GPU/CPU notebook, fully self-contained: generates leakage-safe synthetic data,
# trains XGBoost regressor + classifier, temporal holdout Aug-2026, baselines, calibration, SHAP.

# pip install
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "xgboost", "shap", "scikit-learn", "pandas", "numpy"])

import numpy as np, pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, classification_report, log_loss, accuracy_score
from sklearn.dummy import DummyRegressor
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

RNG = np.random.default_rng(42)
N = 220000
print("generating synthetic competency evidence...", flush=True)
# latent ability per employee-skill
emp = RNG.integers(0, 8000, N); skill = RNG.integers(0, 40, N)
ability = RNG.normal(3.1, 0.8, N).clip(1, 5)
snap = RNG.choice(["2025-10-01","2025-12-01","2026-02-01","2026-04-01","2026-06-01","2026-08-01"],
                  N, p=[.18,.18,.18,.18,.18,.10])
rel = RNG.beta(8, 1.2, N); comp = RNG.beta(7, 1.5, N); conf = RNG.beta(7, 1.5, N)
rec = RNG.beta(6, 2, N); cnt = RNG.integers(1, 4, N)
noise = RNG.normal(0, .35, N) + (1-rel)*RNG.normal(0, .5, N)
obs = np.clip(ability + noise, 1, 5)
assess = np.clip(obs*20 + RNG.normal(0, 6, N), 0, 100)
quiz = np.clip(obs*20 + RNG.normal(0, 8, N), 0, 100)
prac = np.clip(obs*20 + RNG.normal(0, 7, N), 0, 100)
quiz[RNG.random(N) < .25] = np.nan  # missing evidence like real data
req = RNG.choice([2.0, 3.0, 4.0], N); exp_yrs = RNG.gamma(4, 2, N).clip(0, 35)
gap_cls = np.where(obs >= req+.5, "No/Low Gap", np.where(obs >= req-.5, "Moderate Gap", "Critical Gap"))
qm = np.nanmedian(quiz)
df = pd.DataFrame({"assessment_score": assess, "quiz_score": np.where(np.isnan(quiz), qm, quiz),
  "practical_score": prac, "observed_competency": obs, "gap_class": gap_cls,
  "assessment_reliability": rel, "evidence_completeness": comp, "evidence_count": cnt,
  "evidence_confidence": conf, "recency_weight": rec, "required_level": req,
  "experience_years": exp_yrs, "skill_id": skill, "role_id": emp % 60, "snapshot_date": snap})
FEATS = ["required_level","assessment_score","quiz_score","practical_score","assessment_reliability",
         "evidence_completeness","evidence_count","evidence_confidence","recency_weight",
         "experience_years","skill_id","role_id"]
tr = df[df.snapshot_date != "2026-08-01"]; te = df[df.snapshot_date == "2026-08-01"]
Xtr, Xte = tr[FEATS], te[FEATS]
print(f"train={len(tr)} holdout={len(te)}", flush=True)

reg = xgb.XGBRegressor(n_estimators=500, max_depth=6, learning_rate=0.05,
                       subsample=.8, colsample_bytree=.8, n_jobs=-1, random_state=42,
                       tree_method="hist", device="cuda" if __import__("torch").cuda.is_available() else "cpu")
reg.fit(Xtr, tr.observed_competency)
pr = reg.predict(Xte)
print(f"XGB-reg MAE={mean_absolute_error(te.observed_competency, pr):.4f} "
      f"RMSE={mean_squared_error(te.observed_competency, pr)**.5:.4f} R2={r2_score(te.observed_competency, pr):.4f}")
print(f"Baseline MAE={mean_absolute_error(te.observed_competency, DummyRegressor().fit(Xtr, tr.observed_competency).predict(Xte)):.4f}")
err = np.abs(te.observed_competency.values - pr); boots = [RNG.choice(err, len(err), replace=True).mean() for _ in range(200)]
print(f"MAE 95% CI: [{np.percentile(boots, 2.5):.4f}, {np.percentile(boots, 97.5):.4f}]")

le = LabelEncoder().fit(tr.gap_class)
clf = xgb.XGBClassifier(n_estimators=500, max_depth=6, learning_rate=0.05, subsample=.8,
                        colsample_bytree=.8, n_jobs=-1, random_state=42, tree_method="hist")
clf.fit(Xtr, le.transform(tr.gap_class))
pe = le.transform(te.gap_class); pp = clf.predict(Xte)
print(f"XGB-clf acc={accuracy_score(pe, pp):.4f} logloss={log_loss(pe, clf.predict_proba(Xte)):.4f}")
print(classification_report(pe, pp, target_names=list(le.classes_)))
print(f"Calibrated logloss={log_loss(pe, CalibratedClassifierCV(clf, method='sigmoid', cv=3).fit(Xtr, le.transform(tr.gap_class)).predict_proba(Xte)):.4f}")

import shap
sv = shap.TreeExplainer(reg).shap_values(Xte.iloc[:500])
for f, i in sorted(zip(FEATS, np.abs(sv).mean(0)), key=lambda t: -t[1])[:8]:
    print(f"  SHAP {f}: {i:.4f}")
reg.save_model("/kaggle/working/xgb_competency.ubj")
print("saved /kaggle/working/xgb_competency.ubj")
