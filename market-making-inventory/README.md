# Market Making Inventory

A scientifically rigorous implementation of **Optimal Market Making with Inventory Risk**, based on the frameworks of **Avellaneda-Stoikov (2008)** and **Guéant et al. (2013)**.

## Project Goal
To provide a modular, reproducible, and extensible codebase for researching and testing market making strategies that optimize PnL while managing inventory constraints.

## Features
- **Theoretical Models**: Analytical solvers for the HJB equation (Matrix Exponential method).
- **Simulation**: High-fidelity Order Book simulator with Poisson arrival rates ($A e^{-k\delta}$) and Brownian price dynamics.
- **Reinforcement Learning**: Gymnasium environment compatible with Stable Baselines 3 (PPO/DQN).
- **Experimentation**: Backtesting pipeline with automated plotting of PnL, Inventory, and Sharpe Ratios.
- **Real Data Backtest**: Integration with Binance API (via `ccxt`) to test strategies on historical market data.
- **Constraint Programming**: Experimental OR-Tools solver for optimal execution paths.

## Architecture
```
market-making-inventory/
├── src/
│   ├── models/       # Analytical models (Avellaneda-Stoikov)
│   ├── solvers/      # HJB (SciPy) and CSP (OR-Tools) solvers
│   ├── data/         # Simulators and Price generators
│   └── rl_env/       # Gymnasium MarketMakingEnv
├── experiments/      # Backtesting scripts
├── docs/             # Mathematical documentation and State of the Art
└── requirements.txt
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Backtest (Comparison of HJB vs Naive)**
   ```bash
   python experiments/run_backtest.py
   ```
   Results will be saved to `experiments/results/`.

3. **Train RL Agent**
   ```bash
   python src/rl_env/train_rl.py
   ```

## Key Results
The analytical HJB strategy consistently outperforms naive fixed-spread strategies by skewing quotes to mean-revert inventory, thus avoiding toxic inventory buildup during trends.

## References
See `docs/references.md`.
