# Options Pricing, Greeks & Model Validation Engine

A derivatives research platform that implements multiple pricing methods, computes Greeks, and validates numerical methods against analytical benchmarks.

## Pricing models

- Black-Scholes-Merton
- Cox-Ross-Rubinstein binomial tree
- Monte Carlo
- Antithetic variance reduction

## Analytics

- Delta, Gamma, Vega, Theta, Rho
- Greek surfaces
- Volatility, maturity, and moneyness sensitivity
- Binomial convergence
- Monte Carlo convergence and simulation error
- Cross-model pricing comparison
- Delta-hedging simulation

## Validation snapshot

For the default at-the-money European call:

- BSM price: **9.9251**
- CRR price, 500 steps: **9.9211**
- Monte Carlo price, 200k paths: **9.9499**
- Monte Carlo standard error: **0.0324**
- Absolute CRR error vs BSM: **0.0040**
- Absolute Monte Carlo error vs BSM: **0.0248**

The CRR tree is extremely close to the analytical benchmark, while the Monte Carlo estimate is well within one standard error of BSM.

Analytical Greeks:

- Delta: **0.6179**
- Gamma: **0.0191**
- Vega: **0.3814**
- Theta: **-0.0161 per day**
- Rho: **0.5187 per 1% rate move**

The discrete delta-hedging experiment produces:

- Mean hedging error: **-0.011**
- Hedging error stdev: **0.918**

The near-zero mean but non-zero dispersion is exactly what we expect when a continuous-time replication argument is implemented with discrete rebalancing.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest -q
python scripts/run_validation.py
streamlit run dashboard/app.py
```

## Research discipline

The project uses BSM only where its assumptions provide a valid analytical benchmark. Numerical error, simulation error, and hedging error are reported explicitly rather than hidden.

The objective is model validation, not claiming that one pricing model is universally correct.
