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

The project focuses on transparent numerical validation and model limitations rather than treating one pricing model as universally correct.
