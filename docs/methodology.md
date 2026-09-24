# Methodology

Black-Scholes-Merton is the analytical benchmark for European options under lognormal diffusion, constant volatility/rates, frictionless trading, and continuous hedging assumptions. CRR approximates the same risk-neutral process with a recombining tree, while Monte Carlo estimates discounted expected payoff by simulation.

Validation compares numerical prices to BSM where the analytical assumptions match. Tree error should shrink with more steps; Monte Carlo error should decrease approximately with the square root of the number of paths. Antithetic sampling is included as a variance-reduction technique.

Greeks are generated analytically from BSM. The delta-hedging experiment discretizes rebalancing, intentionally demonstrating that continuous-time replication assumptions produce hedging error when trading occurs at finite intervals.
