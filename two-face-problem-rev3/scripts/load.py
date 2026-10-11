import json, numpy as np, pandas as pd
import os
def load(path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"data_simulations.json")):
    d=json.load(open(path)); rows=[]
    for k,s in d.items():
        if not k.startswith("SXS:BBH:"): continue
        try:
            m1=float(s["reference_mass1"]); m2=float(s["reference_mass2"]); Mf=float(s["remnant_mass"])
            c1=np.array(s["reference_dimensionless_spin1"],float); c2=np.array(s["reference_dimensionless_spin2"],float)
            vk=np.linalg.norm(np.array(s["remnant_velocity"],float)); af=np.linalg.norm(np.array(s["remnant_dimensionless_spin"],float))
        except Exception: continue
        if not (m1>0 and m2>0 and 0<Mf<m1+m2): continue
        e=s.get("reference_eccentricity"); 
        try: e=float(e)
        except Exception: e=np.nan
        rows.append(dict(id=k,m1=m1,m2=m2,Mf=Mf,c1=c1,c2=c2,chieff=float(s.get("reference_chi_eff",np.nan)),
                         ecc=e,D=float(s.get("initial_separation",np.nan)),Madm=float(s.get("initial_ADM_energy",np.nan)),
                         Mi=float(s.get("initial_mass1",np.nan))+float(s.get("initial_mass2",np.nan)),
                         vkick=vk,af=af,deprecated=("deprecated" in s.get("keywords",[])),
                         nonspin=(np.linalg.norm(c1)<1e-3 and np.linalg.norm(c2)<1e-3)))
    df=pd.DataFrame(rows)
    M=df.m1+df.m2
    df["a"]=np.maximum(df.m1,df.m2)/M; df["b"]=1-df["a"]          # a = heavier share
    df["chi"]=df.a-df.b; df["eta"]=df.a*df.b; df["h"]=np.sqrt(df.eta); df["R"]=1/(4*df.eta)
    df["xi"]=np.arctanh(df.chi.clip(upper=1-1e-12)); df["theta"]=np.arcsin(df.chi)
    df["q"]=df.b/df.a
    df["Erad"]=1-df.Mf/M                                            # leakage fraction L
    df["bbind"]=(df.Mi-df.Madm)/df.Mi
    return df
if __name__=="__main__":
    df=load(); print(len(df), "BBH rows;", (~df.deprecated).sum(),"non-deprecated;", df.nonspin.sum(),"nonspinning")
    print(df[["q","chi","eta","Erad","vkick","af","chieff","ecc","D","bbind"]].describe().T.round(4))
