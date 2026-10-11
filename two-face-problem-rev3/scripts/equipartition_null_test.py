"""Null test for the 'equipartition differential': observable depends on the partition state
through a fixed smooth function with CONSTANT strength everywhere (no special role for asymmetry).
Use the paper's own bin edges. Does partial R^2 still grow with chi?"""
import numpy as np
rng=np.random.default_rng(0)
edges=[0,0.05,0.10,0.15,0.20,0.30,0.50,0.99]
N=400000
chi=np.concatenate([rng.uniform(lo,hi,int(N*(hi-lo))) for lo,hi in zip(edges[:-1],edges[1:])])
ctx=rng.normal(size=chi.size)
def bases(c):
    a=(1+c)/2; b=1-a; eta=a*b; h=np.sqrt(eta); R=1/(4*eta); xi=np.arctanh(c)
    return {"product":(eta,eta**2),"altitude":(h,h**2),"asym":(c,c**2),"rapidity":(xi,xi**2),"response":(R,R**2),"logR":(np.log(R),np.log(R)**2)}
def r2(X,y):
    X=np.column_stack([np.ones(len(y))]+X); beta,*_=np.linalg.lstsq(X,y,rcond=None); r=y-X@beta; return 1-r.var()/y.var()
for name,f in [("linear in chi, constant slope", lambda c:0.5*c), ("smooth sin(chi)", lambda c:0.5*np.sin(2*c)), ("depends on h", lambda c:0.5*np.sqrt(1-c**2)/2)]:
    y=f(chi)+0.5*ctx+rng.normal(size=chi.size)
    print(f"== Y = {name} + context + noise")
    mids=[];best=[];marg=[]
    for lo,hi in zip(edges[:-1],edges[1:]):
        m=(chi>=lo)&(chi<hi); c=chi[m]; yy=y[m]; base=r2([ctx[m]],yy)
        sc=sorted(((r2([ctx[m],*v],yy)-base),k) for k,v in bases(c).items())[::-1]
        mids.append((lo+hi)/2); best.append(sc[0][0]); marg.append(100*(sc[0][0]-sc[1][0])/max(sc[1][0],1e-12))
        print(f"  [{lo:.2f},{hi:.2f}) N={m.sum():6d} best partial R2={sc[0][0]:.2e} ({sc[0][1]}) margin={marg[-1]:.2f}%")
    print(f"  ratio last/first={best[-1]/best[0]:.1f}  Pearson(chi_mid,best)={np.corrcoef(mids,best)[0,1]:+.2f}  Pearson(chi_mid,margin)={np.corrcoef(mids,marg)[0,1]:+.2f}")
