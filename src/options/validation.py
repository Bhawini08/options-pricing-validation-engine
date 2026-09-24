from dataclasses import replace
import numpy as np
import pandas as pd
from .models import OptionSpec, black_scholes, crr_binomial, monte_carlo, greeks

def convergence_table(o: OptionSpec, tree_steps=(10,25,50,100,250,500), mc_paths=(1000,5000,10000,50000,100000)):
    bsm=black_scholes(o); rows=[]
    for n in tree_steps:
        p=crr_binomial(o,n); rows.append({"method":"CRR","resolution":n,"price":p,"abs_error":abs(p-bsm),"stderr":np.nan})
    for n in mc_paths:
        m=monte_carlo(o,n); rows.append({"method":"Monte Carlo","resolution":n,"price":m["price"],"abs_error":abs(m["price"]-bsm),"stderr":m["stderr"]})
    return pd.DataFrame(rows)

def greek_surface(base: OptionSpec, spots=None, vols=None):
    spots=np.linspace(0.6*base.strike,1.4*base.strike,31) if spots is None else spots
    vols=np.linspace(0.08,0.60,25) if vols is None else vols
    rows=[]
    for s in spots:
        for v in vols:
            o=replace(base,spot=float(s),volatility=float(v)); g=greeks(o)
            rows.append({"spot":s,"volatility":v,"price":black_scholes(o),**g})
    return pd.DataFrame(rows)

def delta_hedge(o: OptionSpec, steps=63, paths=2000, seed=7):
    rng=np.random.default_rng(seed); dt=o.maturity/steps; errors=[]
    for _ in range(paths):
        s=o.spot; cash=black_scholes(o); opt=replace(o,spot=s,maturity=o.maturity); delta=greeks(opt)["delta"]; cash-=delta*s
        for i in range(steps):
            z=rng.standard_normal(); s*=np.exp((o.rate-o.dividend-0.5*o.volatility**2)*dt+o.volatility*np.sqrt(dt)*z)
            cash*=np.exp(o.rate*dt)
            remaining=max(o.maturity-(i+1)*dt,1e-8)
            if i<steps-1:
                new_delta=greeks(replace(o,spot=s,maturity=remaining))["delta"]
                cash-=(new_delta-delta)*s; delta=new_delta
        portfolio=cash+delta*s
        payoff=max(s-o.strike,0) if o.option_type=="call" else max(o.strike-s,0)
        errors.append(portfolio-payoff)
    return np.asarray(errors)
