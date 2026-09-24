import json
from pathlib import Path
import pandas as pd
from options.models import OptionSpec, black_scholes, crr_binomial, monte_carlo, greeks
from options.validation import convergence_table, greek_surface, delta_hedge, variance_reduction_comparison
out=Path("results"); out.mkdir(exist_ok=True)
o=OptionSpec(spot=100,strike=100,maturity=1,rate=0.04,volatility=0.20)
bsm=black_scholes(o); tree=crr_binomial(o,500); mc=monte_carlo(o,200000)
convergence_table(o).to_csv(out/"convergence.csv",index=False)
greek_surface(o).to_csv(out/"greek_surface.csv",index=False)
variance_reduction_comparison(o).to_csv(out/"variance_reduction.csv",index=False)
err=delta_hedge(o); pd.Series(err,name="hedging_error").to_csv(out/"hedging_errors.csv",index=False)
metrics={"bsm":bsm,"crr_500":tree,"mc_200k":mc["price"],"mc_stderr":mc["stderr"],**greeks(o),
         "hedge_error_mean":float(err.mean()),"hedge_error_std":float(err.std(ddof=1))}
(out/"metrics.json").write_text(json.dumps(metrics,indent=2)); print(json.dumps(metrics,indent=2))
