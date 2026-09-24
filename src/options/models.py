from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.stats import norm

@dataclass(frozen=True)
class OptionSpec:
    spot: float
    strike: float
    maturity: float
    rate: float
    volatility: float
    dividend: float = 0.0
    option_type: str = "call"

    def validate(self):
        if self.spot<=0 or self.strike<=0 or self.maturity<=0 or self.volatility<=0:
            raise ValueError("spot, strike, maturity and volatility must be positive")
        if self.option_type not in {"call","put"}: raise ValueError("option_type must be call or put")

def _d1d2(o: OptionSpec):
    o.validate(); s,k,t,r,q,v=o.spot,o.strike,o.maturity,o.rate,o.dividend,o.volatility
    d1=(np.log(s/k)+(r-q+0.5*v*v)*t)/(v*np.sqrt(t)); d2=d1-v*np.sqrt(t)
    return d1,d2

def black_scholes(o: OptionSpec) -> float:
    d1,d2=_d1d2(o); s,k,t,r,q=o.spot,o.strike,o.maturity,o.rate,o.dividend
    if o.option_type=="call":
        return float(s*np.exp(-q*t)*norm.cdf(d1)-k*np.exp(-r*t)*norm.cdf(d2))
    return float(k*np.exp(-r*t)*norm.cdf(-d2)-s*np.exp(-q*t)*norm.cdf(-d1))

def greeks(o: OptionSpec):
    d1,d2=_d1d2(o); s,k,t,r,q,v=o.spot,o.strike,o.maturity,o.rate,o.dividend,o.volatility
    discq=np.exp(-q*t); discr=np.exp(-r*t); pdf=norm.pdf(d1)
    if o.option_type=="call":
        delta=discq*norm.cdf(d1); theta=(-s*discq*pdf*v/(2*np.sqrt(t))-r*k*discr*norm.cdf(d2)+q*s*discq*norm.cdf(d1))/365
        rho=k*t*discr*norm.cdf(d2)/100
    else:
        delta=discq*(norm.cdf(d1)-1); theta=(-s*discq*pdf*v/(2*np.sqrt(t))+r*k*discr*norm.cdf(-d2)-q*s*discq*norm.cdf(-d1))/365
        rho=-k*t*discr*norm.cdf(-d2)/100
    gamma=discq*pdf/(s*v*np.sqrt(t)); vega=s*discq*pdf*np.sqrt(t)/100
    return {"delta":float(delta),"gamma":float(gamma),"vega":float(vega),"theta":float(theta),"rho":float(rho)}

def crr_binomial(o: OptionSpec, steps=200, american=False) -> float:
    o.validate(); n=int(steps)
    if n<1: raise ValueError("steps must be positive")
    dt=o.maturity/n; u=np.exp(o.volatility*np.sqrt(dt)); d=1/u
    p=(np.exp((o.rate-o.dividend)*dt)-d)/(u-d)
    if not 0<=p<=1: raise ValueError("invalid risk-neutral probability; increase steps or review inputs")
    j=np.arange(n+1); st=o.spot*(u**j)*(d**(n-j))
    vals=np.maximum(st-o.strike,0) if o.option_type=="call" else np.maximum(o.strike-st,0)
    disc=np.exp(-o.rate*dt)
    for i in range(n-1,-1,-1):
        vals=disc*(p*vals[1:]+(1-p)*vals[:-1])
        if american:
            j=np.arange(i+1); st=o.spot*(u**j)*(d**(i-j))
            intrinsic=np.maximum(st-o.strike,0) if o.option_type=="call" else np.maximum(o.strike-st,0)
            vals=np.maximum(vals,intrinsic)
    return float(vals[0])

def monte_carlo(o: OptionSpec, paths=100_000, seed=42, antithetic=True):
    o.validate(); rng=np.random.default_rng(seed); n=int(paths)
    if antithetic:
        half=(n+1)//2; z=rng.standard_normal(half); z=np.concatenate([z,-z])[:n]
    else: z=rng.standard_normal(n)
    st=o.spot*np.exp((o.rate-o.dividend-0.5*o.volatility**2)*o.maturity+o.volatility*np.sqrt(o.maturity)*z)
    payoff=np.maximum(st-o.strike,0) if o.option_type=="call" else np.maximum(o.strike-st,0)
    pv=np.exp(-o.rate*o.maturity)*payoff
    return {"price":float(pv.mean()),"stderr":float(pv.std(ddof=1)/np.sqrt(n))}
