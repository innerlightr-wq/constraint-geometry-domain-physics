"""Exact checks for every Tier-1 identity retained in Bridge Guide Revision 3."""
import sympy as sp, math
ok=[];c,xi,a,y,N,k,t,x,r1,r2,L=sp.symbols('chi xi a y N k t x r1 r2 L',real=True)
def chk(name,expr,subs=None,num=False):
    e=sp.simplify(expr)
    if num or e!=0:
        vals=[0.13,0.47,0.81]; e=max(abs(float(expr.subs(subs(v)) if subs else expr.subs(c,v))) for v in vals)
        res=e<1e-12
    else: res=True
    ok.append(res); print(("PASS " if res else "FAIL ")+name)
A=(1+c)/2;B=(1-c)/2;h=sp.sqrt(A*B);R=1/(1-c**2);Y=R/2
chk("a+b=1, chi=a-b",A+B-1+ (A-B-c))
chk("circle (a-b)^2+4ab=(a+b)^2 for any a,b",sp.expand((r1-r2)**2+4*r1*r2-(r1+r2)**2))
chk("4h^2+chi^2=1",4*h**2+c**2-1)
chk("(AM-GM)/(GM-HM)=gamma",(sp.Rational(1,2)-h)/(h-2*h**2)-1/sp.sqrt(1-c**2),num=True)
chk("Fisher: da^2/a+db^2/b = dchi^2/(1-chi^2)",(sp.Rational(1,4))*(1/A+1/B)-1/(1-c**2))
chk("Fisher flat coord theta=arcsin chi",sp.diff(sp.asin(c),c)**2-1/(1-c**2))
chk("rapidity metric flat coord xi=atanh chi",sp.diff(sp.atanh(c),c)**2-1/(1-c**2)**2)
chk("radial metric chi^2/(1-chi^2)^4 flat coord y=R/2",sp.diff(Y,c)**2-c**2/(1-c**2)**4)
chk("metric inversion g_C = J^2 gamma^2 g_P",(c**2/(1-c**2))*(1/(1-c**2))*(1/(1-c**2)**2)-c**2/(1-c**2)**4)
T=sp.tanh(xi)
for nm,e in [("chi=tanh xi=sin gd xi",sp.sin(sp.atan(sp.sinh(xi)))-T),("cos gd = sech",sp.cos(sp.atan(sp.sinh(xi)))-1/sp.cosh(xi)),("R=cosh^2 xi",1/(1-T**2)-sp.cosh(xi)**2)]:
    ok.append(abs(float(e.subs(xi,0.7)))<1e-13); print("PASS "+nm if ok[-1] else "FAIL "+nm)
# dictionary compound column (chi>0 branch)
for nm,e in [("asym sqrt(1-1/(2y))",sp.sqrt(1-1/(2*Y))-c),("coupling 1/sqrt(8y)",1/sp.sqrt(8*Y)-h),("momentum sqrt(2y-1)",sp.sqrt(2*Y-1)-c/sp.sqrt(1-c**2)),("gamma sqrt(2y)",sp.sqrt(2*Y)-1/sp.sqrt(1-c**2))]:
    chk("dictionary: "+nm,e,num=True)
# exponential family / Legendre
p=(1+T)/2
chk("logit p = 2 xi",sp.log(p/(1-p))-2*xi,subs=lambda v:{xi:v},num=True)
chk("R = d xi/d chi",sp.diff(sp.atanh(c),c)-R)
# Bernoulli Fisher
chk("I_F=1/(p(1-p))=1/h^2=4R=8y",1/(A*B)-8*Y)
# Fermi-Dirac
chk("1/(e^x+1)=(1-tanh(x/2))/2",1/(sp.exp(x)+1)-(1-sp.tanh(x/2))/2,subs=lambda v:{x:v},num=True)
# aberration: tan(th'/2)=sqrt((1-b)/(1+b)) tan(th/2) = e^-xi tan(th/2)
chk("sqrt((1-beta)/(1+beta))=e^-xi",sp.sqrt((1-T)/(1+T))-sp.exp(-xi),subs=lambda v:{xi:v},num=True)
# VSWR & resistive composition
chk("VSWR=(1+chi)/(1-chi)=e^{2xi}",(1+T)/(1-T)-sp.exp(2*xi),subs=lambda v:{xi:v},num=True)
z=sp.symbols('z',positive=True)
chk("resistive Gamma=(z-1)/(z+1)=tanh(ln(z)/2)",(z-1)/(z+1)-sp.tanh(sp.log(z)/2),subs=lambda v:{z:v+0.3},num=True)
# Altitude integrals
I1=sp.integrate(sp.sqrt(x*(1-x)),(x,0,1)); Im1=sp.integrate(1/sp.sqrt(x*(1-x)),(x,0,1))
ok.append(sp.simplify(I1/Im1-sp.Rational(1,8))==0); print(("PASS" if ok[-1] else "FAIL")+" I(1)/I(-1)=1/8 (and I(alpha)=B(alpha/2+1,alpha/2+1))")
# G(t) = sum t^m int h^{2m} = int dx/(1-t x(1-x)) = arcsin(sqrt a)/sqrt(a(1-a)), a=t/4
for tv in [0.3,1.7,2.0,3.5]:
    lhs=float(sp.Integral(1/(1-tv*x*(1-x)),(x,0,1)).evalf()); av=tv/4
    rhs=math.asin(math.sqrt(av))/math.sqrt(av*(1-av)); clo=4*math.asin(math.sqrt(tv)/2)/math.sqrt(tv*(4-tv))
    xiv=math.atanh(2*av-1); poin=(math.atan(math.sinh(xiv))+math.pi/2)*math.cosh(xiv)
    ok.append(abs(lhs-rhs)<1e-10 and abs(rhs-clo)<1e-12 and abs(rhs-poin)<1e-12); print(("PASS" if ok[-1] else "FAIL")+f" G({tv}) integral=phi/h=closed form=(gd xi+pi/2)cosh xi")
xiv=0.0; print("   note: old Rev 2 Poincare form 2 gd(xi)cosh(xi) at equipartition gives",2*math.atan(math.sinh(xiv))*math.cosh(xiv),"vs G(2)=",math.pi/2)
# leakage: active (a-b)^2+4ab=(1-L)^2 ; R_act=R_cond/(1-L)^2
A2=(1-L)*A;B2=(1-L)*B
chk("leakage circle radius (1-L)",(A2-B2)**2+4*A2*B2-(1-L)**2,subs=lambda v:{c:v,L:0.3},num=True)
chk("R_act=R_cond/(1-L)^2",1/(4*A2*B2)-R/(1-L)**2,subs=lambda v:{c:v,L:0.3},num=True)
# LCDM e-fold gauge
U=k*sp.exp(3*N); X=(1-U)/(1+U)
chk("LCDM: V^(1) in e-folds = -(9/8)(1-chi^2)",-sp.Rational(1,2)*sp.diff(X,N)**2/(1-X**2)+sp.Rational(9,8)*(1-X**2),subs=lambda v:{N:v,k:2.3},num=True)
chk("LCDM: d xi/dN = -3/2",sp.diff(sp.atanh(X),N)+sp.Rational(3,2),subs=lambda v:{N:v,k:2.3},num=True)
# SR odds composition
b1,b2=sp.symbols('b1 b2',real=True); O=lambda q:(1+q)/(1-q)
chk("Einstein addition multiplies odds",O((b1+b2)/(1+b1*b2))-O(b1)*O(b2))
# ISCO binding
ok.append(abs((1-2/6)/math.sqrt(1-3/6)-math.sqrt(8/9))<1e-15); print("PASS E_ISCO=sqrt(8/9)" if ok[-1] else "FAIL ISCO")
# --- additional checks requested in audit ---
ph=sp.asin(sp.sqrt(A)); th=sp.asin(c)
chk("theta = 2 phi - pi/2",th-(2*ph-sp.pi/2),num=True)
chk("Fisher distance = 2 d phi",sp.diff(2*ph,c)**2-1/(1-c**2),num=True)
lat=sp.symbols('lat',positive=True)
chk("Mercator: ln(sec+tan)=gd^-1 = arccosh(sec) (lat>=0)",sp.log(1/sp.cos(lat)+sp.tan(lat))-sp.acosh(1/sp.cos(lat)),subs=lambda v:{lat:v},num=True)
for al in [0.5,1,2.5,-1]:
    Ia=sp.Integral((x*(1-x))**(sp.Rational(1,2)*al),(x,0,1)).evalf(30); Bv=sp.beta(al/2+1,al/2+1).evalf(30)
    Ir=(2**(-(al+1))*sp.Integral(sp.sech(xi)**(al+2),(xi,-30,30))).evalf(30)
    ok.append(bool(abs(Ia-Bv)<1e-12 and abs(Ia-Ir)<1e-10)); print(("PASS" if ok[-1] else "FAIL")+f" I({al}) = Beta = rapidity form")
cc=sp.symbols('cc',positive=True); bta=sp.symbols('bta',real=True)
chk("SR: ab=(1-beta^2)/4=-ds^2/(4c^2dt^2)",((1+bta)/2)*((1-bta)/2)-(1-bta**2)/4)
for zv in [0.3,1.0,4.0]:
    G=(zv-1)/(zv+1); ok.append(abs((1+abs(G))/(1-abs(G))-max(zv,1/zv))<1e-12); print(("PASS" if ok[-1] else "FAIL")+f" VSWR=max(z,1/z) at z={zv}")
aa=sp.symbols('aa',positive=True)
for orient,Xf,shape in [("a=OmL",lambda U:(U-1)/(U+1),lambda X:(1-X)**sp.Rational(5,3)*(1+X)**sp.Rational(1,3)),("a=Om",lambda U:(1-U)/(1+U),lambda X:(1-X)**sp.Rational(1,3)*(1+X)**sp.Rational(5,3))]:
    X=Xf(k*aa**3); V=-sp.Rational(1,2)*sp.diff(X,aa)**2/(1-X**2); tg=-sp.Rational(9,8)*k**sp.Rational(2,3)*shape(X)
    ok.append(abs(float((V-tg).subs({k:2.3,aa:0.7})))<1e-12); print(("PASS" if ok[-1] else "FAIL")+f" LCDM scale-factor shape, {orient}")
w1,w2=sp.symbols('w1 w2',real=True)
U=k*sp.exp(3*(w2-w1)*N); X=(U-1)/(U+1)
chk("two fluids: dxi/dN = (3/2)(w_b - w_a)",sp.diff(sp.atanh(X),N)-sp.Rational(3,2)*(w2-w1),subs=lambda v:{N:v,k:1.7,w1:-1,w2:0.2},num=True)
print(f"\n{sum(ok)} PASS, {len(ok)-sum(ok)} FAIL")
