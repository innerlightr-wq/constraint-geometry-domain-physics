import numpy as np, pandas as pd
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import load
rng=np.random.default_rng(1)
df=load()
f=df[(~df.deprecated)&(df.ecc<0.01)&(df.Erad>0.001)&(df.Erad<0.2)].copy()
print(f"filtered N={len(f)}; nonspinning N={f.nonspin.sum()}")
def ols_r2(X,y):
    X=np.column_stack([np.ones(len(y))]+list(X)); b,*_=np.linalg.lstsq(X,y,rcond=None); r=y-X@b; return 1-r.var()/y.var()
B=lambda d:{"product":(d.eta,d.eta**2),"altitude":(d.h,d.h**2),"asym":(d.chi,d.chi**2),"rapidity":(d.xi,d.xi**2),"response":(d.R,d.R**2),"logR":(np.log(d.R),np.log(d.R)**2)}
def T1(edges,label):
    print(f"\n== T1 {label}")
    mids=[];best=[];vchi=[]
    for lo,hi in zip(edges[:-1],edges[1:]):
        d=f[(f.chi>=lo)&(f.chi<hi)]
        if len(d)<30: print(f"  [{lo:.2f},{hi:.2f}) N={len(d)} skipped"); continue
        ctx=[d.chieff,d.bbind,1/d.D]; base=ols_r2(ctx,d.Erad)
        sc=sorted(((ols_r2(ctx+list(v),d.Erad)-base),k) for k,v in B(d).items())[::-1]
        mids.append((lo+hi)/2); best.append(sc[0][0]); vchi.append(d.chi.var())
        print(f"  [{lo:.2f},{hi:.2f}) N={len(d):4d} Var(chi)={d.chi.var():.2e} best partial R2={sc[0][0]:.3e} ({sc[0][1]})")
    mids,best,vchi=map(np.array,(mids,best,vchi))
    print(f"  ratio last/first={best[-1]/best[0]:.1f}  Pearson(chi_mid,best)={np.corrcoef(mids,best)[0,1]:+.2f}  Pearson(log Var(chi), log best)={np.corrcoef(np.log(vchi),np.log(best))[0,1]:+.2f}")
T1([0,0.1,0.2,0.3,0.4,0.5,0.65,0.95],"paper's bins")
T1(list(np.linspace(0,0.91,8)),"equal-width bins")
# T2 native coordinate
n=f[f.nonspin].copy()
coords={"eta (h^2)":n.eta,"h":n.h,"chi":n.chi,"xi (rapidity)":n.xi,"R":n.R,"theta (Fisher)":n.theta}
def cv_rmse(x,y,deg,k=5):
    idx=rng.permutation(len(y)); folds=np.array_split(idx,k); err=[]
    for i in range(k):
        te=folds[i]; tr=np.concatenate([folds[j] for j in range(k) if j!=i])
        p=np.polyfit(x[tr],y[tr],deg); err.append(np.mean((np.polyval(p,x[te])-y[te])**2))
    return np.sqrt(np.mean(err))
for tname,y in [("E_rad/M",n.Erad.values),("final spin a_f",n.af.values)]:
    print(f"\n== T2 native coordinate for {tname} (nonspinning N={len(n)}); 5-fold CV RMSE x1e4")
    for deg in (1,2,3):
        res=sorted((cv_rmse(np.asarray(c,float),y,deg),k) for k,c in coords.items())
        print(f"  degree {deg}: "+"  ".join(f"{k}={v*1e4:.2f}" for v,k in res))
# T3 small-eta leakage slope
print("\n== T3 leakage law E_rad ~ (1-sqrt(8/9)) eta as eta->0 (nonspinning)")
for cut in (0.12,0.09,0.07):
    s=n[n.eta<cut]
    if len(s)>=4:
        p=np.polyfit(s.eta,s.Erad/s.eta,1); print(f"  eta<{cut}: N={len(s)}, extrapolated E_rad/eta at eta=0: {p[1]:.4f}  (test-particle 1-sqrt(8/9)={1-np.sqrt(8/9):.4f})")
print(f"  global quadratic fit E_rad = c1 eta + c2 eta^2: {np.linalg.lstsq(np.column_stack([n.eta,n.eta**2]),n.Erad,rcond=None)[0].round(4)}")
# T4 kick
print("\n== T4 recoil (nonspinning): single-coordinate polys vs mixed Fitchett/Gonzalez form")
y=n.vkick.values
for deg in (2,3):
    res=sorted((cv_rmse(np.asarray(c,float),y,deg),k) for k,c in coords.items())
    print(f"  degree {deg}: "+"  ".join(f"{k}={v*1e5:.2f}" for v,k in res)+"  (x1e-5)")
X=np.column_stack([n.eta**2*np.sqrt(np.clip(1-4*n.eta,0,None)), n.eta**3*np.sqrt(np.clip(1-4*n.eta,0,None))])
idx=rng.permutation(len(y)); folds=np.array_split(idx,5); err=[]
for i in range(5):
    te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i]); b,*_=np.linalg.lstsq(X[tr],y[tr],rcond=None); err.append(np.mean((X[te]@b-y[te])**2))
b,*_=np.linalg.lstsq(X,y,rcond=None)
print(f"  mixed h^4*chi*(A + B h^2) (2 params, no intercept): CV RMSE={np.sqrt(np.mean(err))*1e5:.2f} x1e-5; A={b[0]:.4f}, B/A={b[1]/b[0]:.3f}")
print(f"  peak of eta^2 sqrt(1-4eta)(1+B/A eta) on grid: eta*={max(np.linspace(0.01,0.25,2401),key=lambda e:e**2*np.sqrt(1-4*e)*(1+b[1]/b[0]*e)):.4f}")
