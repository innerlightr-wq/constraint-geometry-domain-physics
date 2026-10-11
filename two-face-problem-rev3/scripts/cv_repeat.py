import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load import load
df=load(); f=df[(~df.deprecated)&(df.ecc<0.01)&(df.Erad>0.001)&(df.Erad<0.2)]; n=f[f.nonspin]
rng=np.random.default_rng(7)
coords={"eta":n.eta,"h":n.h,"chi":n.chi,"theta":n.theta,"xi":n.xi,"R":n.R}
def cv(x,y,deg,reps=200,k=5):
    out=[]
    for _ in range(reps):
        idx=rng.permutation(len(y)); folds=np.array_split(idx,k); e=[]
        for i in range(k):
            te=folds[i]; tr=np.concatenate([folds[j] for j in range(k) if j!=i]); p=np.polyfit(x[tr],y[tr],deg); e.append(np.mean((np.polyval(p,x[te])-y[te])**2))
        out.append(np.sqrt(np.mean(e)))
    return np.mean(out), np.std(out)
print(f"nonspinning N={len(n)}, equal-mass (chi<0.01): {(n.chi<0.01).sum()}")
for name,y,sc in [("E_rad/M",n.Erad.values,1e4),("a_f",n.af.values,1e4)]:
    print(f"== {name}: repeated 5-fold CV (200 repeats), RMSE x1e-4 mean (sd over repeats)")
    for deg in (1,2,3):
        res=sorted(((cv(np.asarray(c,float),y,deg)),k) for k,c in coords.items())
        print(f"  deg {deg}: "+"  ".join(f"{k}={m*sc:.2f}({s*sc:.2f})" for (m,s),k in res))
