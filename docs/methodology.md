# Methodology

## Analytical benchmark

Black-Scholes-Merton is used as the analytical benchmark for European options under lognormal diffusion, constant volatility and rates, frictionless trading, and continuous hedging.

## Cox-Ross-Rubinstein tree

The CRR model approximates the same risk-neutral diffusion using a recombining binomial tree. Validation focuses on convergence toward BSM as the number of time steps increases.

For the default case, the 500-step CRR value differs from BSM by only about 0.004.

## Monte Carlo

Monte Carlo simulates terminal prices under the risk-neutral measure and discounts expected payoff. The validation engine reports both the estimated price and sampling standard error.

Antithetic variates are implemented as a variance-reduction technique. Convergence is evaluated by increasing path counts rather than presenting one simulation result in isolation.

For the default 200k-path run, the Monte Carlo estimate differs from BSM by less than one reported standard error.

## Greeks

Delta, Gamma, Vega, Theta, and Rho are calculated analytically from BSM. Sensitivity surfaces vary spot, volatility, maturity, and moneyness to show where exposures change most rapidly.

## Delta hedging

The hedging simulation rebalances a BSM delta hedge at discrete intervals along simulated paths. Because BSM replication is continuous-time in theory, finite rebalancing creates residual hedging error even when the pricing model is internally consistent.

The default run produces a mean hedging error close to zero with meaningful dispersion, which is the expected result from discretization rather than evidence of a pricing bias.

## Model limitations

BSM assumes constant volatility and continuous trading. CRR inherits the same diffusion assumptions as it converges. Monte Carlo introduces sampling error. None of these models captures volatility smiles, stochastic volatility, jumps, liquidity, or discrete transaction costs unless those features are explicitly added.

The project therefore separates numerical validation from model realism.
