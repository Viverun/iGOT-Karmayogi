"""ML integration hardening tests: contracts, determinism, failure injection.

Run:  python3 backend/tests/test_ml_integration.py
Isolation-sensitive cases (missing/corrupt models, no-torch) run in
subprocesses so the ml_scorers lazy-load cache can never leak between them.
DB-backed cases skip gracefully when Supabase is unreachable.
Exit non-zero on any failure.
"""
import os
import subprocess
import sys

BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND)

PASS, FAIL, SKIP = 0, 0, 0


def check(name, fn):
    global PASS, FAIL, SKIP
    try:
        r = fn()
        if r == "skip":
            SKIP += 1
            print(f"SKIP  {name}")
        else:
            PASS += 1
            print(f"PASS  {name}")
    except AssertionError as e:
        FAIL += 1
        print(f"FAIL  {name}: {e}")
    except Exception as e:  # noqa: BLE001 — a crash is also a failure
        FAIL += 1
        print(f"FAIL  {name}: {type(e).__name__}: {e}")


def run_sub(env_extra, code):
    env = dict(os.environ, **env_extra)
    p = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, cwd=BACKEND, timeout=120, env=env)
    return p


SUB_IMPORT = "import sys; sys.path.insert(0, '.'); import ml_scorers as ml; "

# ---------- 1. contracts ----------

def t_xgb_feature_contract():
    import ml_scorers as ml
    assert ml.XGB_FEATS == ["required_level", "assessment_score", "quiz_score",
                            "practical_score", "assessment_reliability",
                            "evidence_completeness", "evidence_count",
                            "evidence_confidence", "recency_weight",
                            "experience_years", "skill_id", "role_id"], "feat order drift"
    b = ml._load_xgb()
    assert b is not None, "artifact missing — primary path would silently fall back"
    assert len(b.feature_names) == 12, f"artifact expects {b.feature_names}"


def t_ncf_arch_match():
    import ml_scorers as ml
    m = ml._ncf_model()
    assert m is not None, "torch or weights missing"
    import torch
    sd = torch.load(os.path.join(BACKEND, "ml/kaggle_models/ncf_hybrid.pt"),
                    map_location="cpu")
    assert set(sd) == set(m.state_dict()), "arch/weights key mismatch"
    assert sd["u.weight"].shape == (8000, 32), sd["u.weight"].shape
    assert sd["c.weight"].shape == (120, 32), sd["c.weight"].shape


def t_no_leakage_in_scorer():
    src = open(os.path.join(BACKEND, "ml_scorers.py")).read()
    for banned in ("true_competency",):
        assert banned not in src, f"leakage: {banned} in scorer"
    import ml_scorers as ml
    import gap_engine as ge  # noqa: F401 — ensures evidence builder has no hidden labels
    gsrc = open(os.path.join(BACKEND, "gap_engine.py")).read()
    assert "true_competency" not in gsrc, "leakage in gap_engine"


# ---------- 2. determinism + ranges ----------

def _ev(high=True):
    v = 85.0 if high else 25.0
    return {"required_level": 3.0, "assessment_score": v, "quiz_score": v,
            "practical_score": v, "assessment_reliability": 0.9,
            "evidence_completeness": 1.0, "evidence_count": 3,
            "evidence_confidence": 0.9, "recency_weight": 0.8,
            "experience_years": 5.0, "skill_id": 3, "role_id": 7}


def t_xgb_determinism_range_monotonic():
    import ml_scorers as ml
    a = ml.predict_competency(_ev(True))
    b = ml.predict_competency(_ev(True))
    lo = ml.predict_competency(_ev(False))
    assert a is not None and b is not None and lo is not None
    assert a == b, "non-deterministic XGB predict"
    assert 1.0 <= a <= 5.0 and 1.0 <= lo <= 5.0, f"out of 1-5 range: {a}, {lo}"
    assert a > lo, f"not monotonic: high={a} low={lo}"


def t_xgb_garbage_never_raises():
    import ml_scorers as ml
    assert ml.predict_competency({}) is not None  # all-defaults still predicts
    assert ml.predict_competency({"assessment_score": "junk"}) is None
    assert ml.predict_competency(None) is None


def t_ncf_determinism_range():
    import ml_scorers as ml
    if not ml.ncf_available():
        return "skip"
    ctx = {k: 0.6 for k in ml.NCF_CTX}
    a = ml.ncf_score(42, "rs-fundamentals", ctx)
    b = ml.ncf_score(42, "rs-fundamentals", ctx)
    assert a is not None and 0.0 <= a <= 1.0, a
    assert a == b, "non-deterministic NCF"
    assert ml.ncf_score(42, "rs-fundamentals", None) is None
    assert ml.stable_idx("x", 120) == ml.stable_idx("x", 120)


# ---------- 3. failure injection (subprocesses) ----------

def t_missing_models_fallback():
    p = run_sub({"ML_MODELS_DIR": "/tmp/empty_models_mltest"},
                SUB_IMPORT + "import json;"
                "assert not ml.xgb_available(); assert not ml.ncf_available();"
                "assert ml.predict_competency({'a':1}) is None;"
                "assert ml.ncf_score(1,'c',{}) is None;"
                "s=ml.status();"
                "assert s['competency_primary']=='ewma' and s['ranking_primary']=='rule-based', s;"
                "print('fallback-ok')")
    assert p.returncode == 0 and "fallback-ok" in p.stdout, p.stderr[-2000:]


def t_corrupt_models_fallback():
    p = run_sub({"ML_MODELS_DIR": "/tmp/corrupt_models_mltest"},
                "import os; os.makedirs('/tmp/corrupt_models_mltest', exist_ok=True);"
                "open('/tmp/corrupt_models_mltest/xgb_competency.ubj','w').write('garbage');"
                "open('/tmp/corrupt_models_mltest/ncf_hybrid.pt','w').write('garbage');"
                + SUB_IMPORT +
                "assert not ml.xgb_available(), 'corrupt xgb must not load';"
                "assert not ml.ncf_available(), 'corrupt ncf must not load';"
                "assert ml.predict_competency({'a':1}) is None;"
                "print('corrupt-ok')")
    assert p.returncode == 0 and "corrupt-ok" in p.stdout, p.stderr[-2000:]


def t_no_torch_ncf_off_xgb_on():
    code = ("\n".join([
        "import sys, importlib.abc",
        "class Blocker(importlib.abc.MetaPathFinder):",
        "    def find_spec(self, n, p=None, t=None):",
        "        if n == 'torch' or n.startswith('torch.'):",
        "            raise ImportError('torch blocked for test')",
        "        return None",
        "sys.meta_path.insert(0, Blocker())",
        "sys.path.insert(0, '.'); import ml_scorers as ml",
        "assert not ml.ncf_available(), 'ncf must be off without torch'",
        "assert ml.xgb_available(), 'xgb must stay on without torch'",
        "print('notorch-ok')",
    ]))
    p = run_sub({}, code)
    assert p.returncode == 0 and "notorch-ok" in p.stdout, p.stderr[-2000:]


# ---------- 4. rerank math (monkeypatch, cache-safe) ----------

def t_ncf_rerank_math():
    import ml_scorers as ml
    import gap_engine as ge
    if not ml.ncf_available():
        return "skip"
    real_avail, real_score = ml.ncf_available, ml.ncf_score
    try:
        ml.ncf_available = lambda: True
        ml.ncf_score = lambda u, k, c: 0.99 if k == "b" else 0.01
        courses = [
            {"identifier": "a", "level": "Basic", "competencyAreas": ["Python"],
             "name": "A", "provider": "P", "durationMinutes": 60},
            {"identifier": "b", "level": "Basic", "competencyAreas": ["Python"],
             "name": "B", "provider": "P", "durationMinutes": 60},
        ]
        gaps = {"top_gaps": [{"area": "Python", "gap": 50}], "vector": []}
        out = ge._ncf_rerank(1, [(50.0, c, []) for c in courses],
                             {"Python": 50})
        out.sort(key=lambda t: t[0], reverse=True)  # caller (build_roadmap) sorts
        assert [c["identifier"] for _, c, _ in out] == ["b", "a"], "blend must reorder"
        assert any("ML-ranked" in r for _, _, rs in out for r in rs)
        # rule fallback untouched when NCF off
        ml.ncf_available = lambda: False
        out2 = ge._ncf_rerank(1, [(50.0, c, []) for c in courses], {"Python": 50})
        assert [c["identifier"] for _, c, _ in out2] == ["a", "b"]
    finally:
        ml.ncf_available, ml.ncf_score = real_avail, real_score


# ---------- 5. DB consistency (optional) ----------

def t_single_vs_bulk_consistency():
    try:
        import main  # noqa: F401 — needs Supabase
        import gap_engine as ge
        import ml_scorers as ml
        if not ml.xgb_available():
            return "skip"
        from db import get_db
        conn = get_db()
        try:
            u = conn.execute(
                "SELECT id, department FROM users ORDER BY id LIMIT 1").fetchone()
        finally:
            conn.close()
        if not u:
            return "skip"
        from assessment import department_key as dk
        dept = dk(u["department"])
        single = ge.competency_vector(u["id"], dept)
        pre = ge.bulk_context([u["id"]])
        bulk = ge.competency_vector(u["id"], dept, prefetch=pre)
        s = {v["area"]: (v["current"], v.get("source")) for v in single}
        b = {v["area"]: (v["current"], v.get("source")) for v in bulk}
        assert s == b, f"dashboard/admin disagree: {[a for a in s if s[a] != b.get(a)][:3]}"
    except Exception as e:
        if "connect" in str(type(e)).lower() or "connection" in str(e).lower():
            return "skip"
        raise


for name, fn in sorted([(k, v) for k, v in list(globals().items())
                        if k.startswith("t_")]):
    check(name, fn)

print(f"\n{PASS} passed, {FAIL} failed, {SKIP} skipped")
sys.exit(1 if FAIL else 0)
