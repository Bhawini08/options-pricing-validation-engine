from dataclasses import replace
import numpy as np
from options.models import OptionSpec, black_scholes, crr_binomial, monte_carlo, greeks

def test_put_call_parity():
    c=OptionSpec(100,105,1.2,0.03,0.25,0.01,"call"); p=replace(c,option_type="put")
    lhs=black_scholes(c)-black_scholes(p); rhs=c.spot*np.exp(-c.dividend*c.maturity)-c.strike*np.exp(-c.rate*c.maturity)
    assert abs(lhs-rhs)<1e-8

def test_binomial_converges_to_bsm():
    o=OptionSpec(100,100,1,0.04,0.2)
    assert abs(crr_binomial(o,1000)-black_scholes(o))<0.05

def test_monte_carlo_within_sampling_error():
    o=OptionSpec(100,100,1,0.04,0.2); m=monte_carlo(o,150000)
    assert abs(m["price"]-black_scholes(o)) < 4*m["stderr"]

def test_greeks_have_expected_signs():
    o=OptionSpec(100,100,1,0.04,0.2); g=greeks(o)
    assert 0<g["delta"]<1 and g["gamma"]>0 and g["vega"]>0
