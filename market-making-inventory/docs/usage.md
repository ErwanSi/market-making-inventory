# Usage Guide

## 1. Running Simulations

To run the standard comparison between the Naive strategy and the HJB Optimal strategy:

```bash
python experiments/run_backtest.py
```

This script will:
1. Initialize the `OrderBookSimulator`.
2. Run the `Naive` strategy (fixed spread).
3. Run the `HJB_Exact` strategy (matrix exponential solution).
4. Run the `HJB_Approx` strategy (closed-form approximation).
5. Generate plots in `experiments/results/`:
   - `pnl.png`: Cumulative PnL over time.
   - `inventory_dist.png`: Histogram of held inventory.

   - `inventory_dist.png`: Histogram of held inventory.

## 2. Real Data Backtesting (Phase 9)

To test the strategy on real historical data (e.g., Binance BTC/USDT), use the `run_real_data_backtest.py` script. This will download data using `ccxt` and replay the simulator.

```bash
python experiments/run_real_data_backtest.py
```

- **Data Source**: Binance (via `ccxt`)
- **Pair**: BTC/USDT (default)
- **Timeframe**: 1m
- **Results**: Generates `real_pnl.png`, `real_price.png`, `real_inventory.png`.

## 3. Training Reinforcement Learning

To train a PPO agent from scratch:

```bash
python src/rl_env/train_rl.py
```

This uses `stable-baselines3` to train an agent on the `MarketMakingEnv`. The model is saved to `models/ppo_market_maker`.

## 3. Customizing Parameters

You can modify market parameters in `experiments/run_backtest.py` or by passing a `SimulationConfig` object:

```python
from src.data.simulator import SimulationConfig
from src.models.inventory_hjb import MarketParameters

config = SimulationConfig(
    sigma=0.5,  # Annualized volatility
    T=1.0,      # Horizon in years
    dt=1/2520   # Time step
)

params = MarketParameters(
    gamma=0.1,  # Risk aversion (higher = tighter inventory control)
    k=1.5,      # Liquidity parameter (decay of filling prob)
    A=140.0     # Base order arrival intensity
)
```

## 4. Understanding the Constraints

- **Inventory Limit**: The HJB solver handles hard constraints if `max_inventory_Q` is set. The simulation will not fill orders that breach this limit.
- **Risk Aversion ($\gamma$)**: Increasing this parameter makes the agent more aggressive in liquidating inventory (widening spreads on one side, narrowing on the other).
