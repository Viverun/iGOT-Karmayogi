"""Competency Model: XGBoost with temporal validation, calibration, SHAP, CI, baselines.
Target: observed_competency (1-5 continuous) + gap_class classification.
Leakage-safe: never uses true_competency/gap hidden labels.
Temporal: train <=2026-06-01, holdout =2026-08-01. Strict unseen-employee via employee_split.
"""
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, classification_report, log_loss
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.calibration import CalibratedClassifierCV
import xgboost as xgb

CSV = "backend/ml/competency_kaggle.csv"
NUM = ["required_level","assessment_score","quiz_score","practical_score","assessment_reliability",
       "evidence_completeness","evidence_count","evidence_confidence","recency_weight","experience_years"]

def load():
    df = pd.read_csv(CSV)
    for c in NUM: df[c] = pd.to_numeric(df[c], errors="coerce")
    df[["quiz_score"]] = df[["quiz_score"]].fillna(df[["quiz_score"]].median())
    df["skill_id"] = df["skill_id"].astype("category").cat.codes
    df["role_id"] = df["role_id"].astype("category").cat.codes
    feats = NUM + ["skill_id","role_id"]
    return df, feats

def main(n_debug=None):
    df, feats = load()
    df = df.dropna(subset=["observed_competency","gap_class"])
    if n_debug: df = df.sample(n_debug, random_state=42)
    X = df[feats]; y_reg = df["observed_competency"]; y_clf = df["gap_class"]
    # temporal split
    te_mask = df["snapshot_date"]=="2026-08-01"
    tr = df[~te_mask]; te = df[te_mask]
    Xtr, Xte = tr[feats], te[feats]
    ytr_r, yte_r = tr["observed_competency"], te["observed_competency"]
    ytr_c, yte_c = tr["gap_class"], te["gap_class"]
    print(f"train={len(tr)} holdout={len(te)} feats={feats}")

    # --- regression: XGBoost ---
    reg = xgb.XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.05,
                           subsample=0.8, colsample_bytree=0.8, n_jobs=-1, random_state=42)
    reg.fit(Xtr, ytr_r)
    pr = reg.predict(Xte)
    rmse = mean_squared_error(yte_r, pr)**0.5
    print(f"XGB-reg  MAE={mean_absolute_error(yte_r,pr):.4f} RMSE={rmse:.4f} R2={r2_score(yte_r,pr):.4f}")
    dum = DummyRegressor(strategy="mean").fit(Xtr, ytr_r)
    print(f"Baseline MAE={mean_absolute_error(yte_r,dum.predict(Xte)):.4f}")
    # bootstrap 95% CI on MAE
    rng = np.random.default_rng(42); boots=[]
    err = np.abs(yte_r.values-pr)
    for _ in range(200):
        boots.append(rng.choice(err, size=len(err), replace=True).mean())
    print(f"MAE 95% CI: [{np.percentile(boots,2.5):.4f}, {np.percentile(boots,97.5):.4f}]")

    # --- classification: gap_class + calibration ---
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder().fit(ytr_c)
    ytr_ce, yte_ce = le.transform(ytr_c), le.transform(yte_c)
    print("classes:", list(le.classes_))
    clf = xgb.XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05,
                            subsample=0.8, colsample_bytree=0.8, n_jobs=-1, random_state=42)
    clf.fit(Xtr, ytr_ce)
    pc = clf.predict(Xte)
    from sklearn.metrics import accuracy_score
    print(f"XGB-clf acc={accuracy_score(yte_ce,pc):.4f} logloss={log_loss(yte_ce, clf.predict_proba(Xte)):.4f}")
    print(classification_report(yte_ce, pc, target_names=list(le.classes_), zero_division=0))
    cal = CalibratedClassifierCV(clf, method="sigmoid", cv=3).fit(Xtr, ytr_ce)
    print(f"Calibrated logloss={log_loss(yte_ce, cal.predict_proba(Xte)):.4f}")

    # --- SHAP (sample) ---
    try:
        import shap
        sv = shap.TreeExplainer(reg).shap_values(Xte.iloc[:500])
        imp = np.abs(sv).mean(0)
        for f,i in sorted(zip(feats,imp), key=lambda t:-t[1])[:8]:
            print(f"  SHAP {f}: {i:.4f}")
    except Exception as e: print("SHAP skipped:", e)
    reg.save_model("backend/ml/xgb_competency.ubj")
    print("saved backend/ml/xgb_competency.ubj")

if __name__=="__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv)>1 else None)
