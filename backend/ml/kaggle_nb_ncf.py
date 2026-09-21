# iGOT Hybrid NCF Recommender — content + collaborative filtering, ranking, hard negatives, diversity
# Self-contained Kaggle GPU notebook.
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pandas", "numpy", "scikit-learn"])

import numpy as np, pandas as pd, torch, torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

RNG = np.random.default_rng(7)
N_U, N_C, PER = 8000, 120, 20
N = N_U * PER
print(f"generating {N} synthetic rec examples...", flush=True)
uid = np.repeat(np.arange(N_U), PER); cid = RNG.integers(0, N_C, N)
gap = RNG.beta(3, 3, N); pre = RNG.beta(4, 2, N); gain = RNG.beta(2, 5, N)
comp = RNG.beta(3, 2, N); nov = RNG.beta(2, 3, N)
logit = 2.2*gap + 1.5*pre + 1.2*gain + .8*comp - .6*nov + RNG.normal(0, .8, N) - 2.2
pos = (RNG.random(N) < 1/(1+np.exp(-logit))).astype(int)
hard = ((pos == 0) & (gap > .55) & (pre > .5)).astype(int)  # topical but weakly aligned
df = pd.DataFrame({"uid": uid, "cid": cid, "gap_alignment_score": gap, "prerequisite_fit": pre,
  "expected_gain": gain, "completion_probability": comp, "novelty": nov,
  "positive_label": pos, "hard_negative": hard})
print(f"pos_rate={pos.mean():.3f} hard_neg_rate={hard.mean():.3f}", flush=True)
CTX = ["gap_alignment_score","prerequisite_fit","expected_gain","completion_probability","novelty"]

class HybridNCF(nn.Module):
    def __init__(self, n_u, n_c, d=32):
        super().__init__()
        self.u = nn.Embedding(n_u, d); self.c = nn.Embedding(n_c, d)
        self.mlp = nn.Sequential(nn.Linear(d*2+5, 64), nn.ReLU(), nn.Dropout(.2),
                                 nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1))
    def forward(self, u, c, x):
        return self.mlp(torch.cat([self.u(u), self.c(c), x], 1)).squeeze(1)

tr, te = train_test_split(df, test_size=.2, random_state=42, stratify=df.positive_label)
dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device:", dev, flush=True)
m = HybridNCF(N_U, N_C).to(dev); opt = torch.optim.Adam(m.parameters(), 1e-3); bce = nn.BCEWithLogitsLoss()
for ep in range(8):
    m.train(); tot = 0
    idx = RNG.permutation(len(tr)); B = 4096
    for s in range(0, len(tr), B):
        b = tr.iloc[idx[s:s+B]]
        u = torch.tensor(b.uid.values, dtype=torch.long).to(dev); c = torch.tensor(b.cid.values, dtype=torch.long).to(dev)
        x = torch.tensor(b[CTX].values, dtype=torch.float32).to(dev); y = torch.tensor(b.positive_label.values, dtype=torch.float32).to(dev)
        w = torch.where(torch.tensor(b.hard_negative.values) == 1, 2.0, 1.0).to(dev)
        loss = (bce(m(u, c, x), y) * w).mean()
        opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(b)
    print(f"ep{ep+1} loss={tot/len(tr):.4f}", flush=True)
m.eval()
with torch.no_grad():
    s = torch.sigmoid(m(torch.tensor(te.uid.values, dtype=torch.long).to(dev),
                        torch.tensor(te.cid.values, dtype=torch.long).to(dev),
                        torch.tensor(te[CTX].values, dtype=torch.float32).to(dev))).cpu().numpy()
print(f"AUC={roc_auc_score(te.positive_label, s):.4f}")
te2 = te.copy(); te2["s"] = s; hs = []; nds = []
for _, g in te2.groupby("uid"):
    if g.positive_label.sum() == 0 or len(g) < 3: continue
    o = np.argsort(-g.s.values); rel = g.positive_label.values[o][:10]
    dcg = sum(r/np.log2(i+2) for i, r in enumerate(rel))
    idcg = sum(1/np.log2(i+2) for i in range(min(int(g.positive_label.sum()), 10)))
    hs.append(int(rel.sum() > 0)); nds.append(dcg/idcg if idcg else 0)
print(f"HR@10={np.mean(hs):.4f} NDCG@10={np.mean(nds):.4f} over {len(hs)} users")
# diversity: 1 - mean pairwise course overlap in top-5 per user
divs = []
for _, g in te2.groupby("uid"):
    top = g.nlargest(5, "s").cid.values
    divs.append(len(set(top))/5)
print(f"diversity@5={np.mean(divs):.4f}")
torch.save(m.state_dict(), "/kaggle/working/ncf_hybrid.pt")
print("saved /kaggle/working/ncf_hybrid.pt")
