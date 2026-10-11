import sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from load import load
df=load(); f=df[(~df.deprecated)&(df.ecc<0.01)&(df.Erad>0.001)&(df.Erad<0.2)]; n=f[f.nonspin]
C=["#2a78d6","#eb6834","#1baf7a"]; INK2="#52514e"; GRID="#e4e3df"
plt.rcParams.update({"font.size":9,"font.family":"serif","axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":INK2,"xtick.color":INK2,"ytick.color":INK2})
fig,ax=plt.subplots(1,2,figsize=(7.4,3.0))
e=np.linspace(0.001,0.25,300)
ax[0].scatter(n.eta,n.Erad/n.eta,s=14,color=C[0],edgecolor="white",linewidth=0.8,zorder=3,label="SXS nonspinning")
ax[0].axhline(1-np.sqrt(8/9),color=C[1],lw=1.5,ls="--",label="test-particle ISCO binding, 1−√(8/9)")
ax[0].set_xlabel("coupling η = h² = ab"); ax[0].set_ylabel("leakage per coupling, (E_rad/M)/η"); ax[0].set_xlim(0,0.26)
ax[0].grid(axis="y",color=GRID,lw=0.6); ax[0].legend(frameon=False,fontsize=7,loc="upper left")
ax[0].set_title("Leakage per unit coupling",fontsize=8.5)
y=n.vkick.values*299792.458; X=np.column_stack([n.eta**2*np.sqrt(1-4*n.eta),n.eta**3*np.sqrt(1-4*n.eta)])
b,*_=np.linalg.lstsq(X,y,rcond=None)
ax[1].scatter(n.eta,y,s=14,color=C[0],edgecolor="white",linewidth=0.8,zorder=3,label="SXS nonspinning")
ax[1].plot(e,b[0]*e**2*np.sqrt(1-4*e)+b[1]*e**3*np.sqrt(1-4*e),color=C[2],lw=2,label="A·h⁴·χ·(1 + B·h²), 2 parameters")
ax[1].set_xlabel("coupling η = h² = ab"); ax[1].set_ylabel("recoil |v_kick| (km/s)"); ax[1].set_xlim(0,0.26)
ax[1].grid(axis="y",color=GRID,lw=0.6); ax[1].legend(frameon=False,fontsize=7,loc="lower center")
ax[1].set_title("Recoil against coupling",fontsize=8.5)
fig.tight_layout(); fig.savefig("fig_sxs.png",dpi=170)
print("A=%.0f km/s, B/A=%.3f, peak v=%.0f km/s"%(b[0],b[1]/b[0],max(b[0]*e**2*np.sqrt(1-4*e)+b[1]*e**3*np.sqrt(1-4*e))))
