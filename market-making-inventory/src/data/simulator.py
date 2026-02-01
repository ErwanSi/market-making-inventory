import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class SimulationConfig:
    S0: float = 100.0       # Initial price
    T: float = 1.0          # Total time (years)
    dt: float = 1/2520      # Time step (e.g. 10 steps per day if 1/252 is daily)
    sigma: float = 0.2      # Volatility
    seed: int = 42

class OrderBookSimulator:
    """
    Simulates a simplified Limit Order Book with:
    - Mid-price following Arithmetic Brownian Motion
    - Probability of Fill based on quote distance (Poisson intensity)
    """
    
    
    def __init__(self, config: SimulationConfig, price_path: Optional[np.ndarray] = None):
        self.config = config
        self.rng = np.random.default_rng(config.seed)
        self.external_price_path = price_path
        self.reset()
        
    def reset(self):
        if self.external_price_path is not None:
             self.current_price = self.external_price_path[0]
        else:
             self.current_price = self.config.S0
        
        self.current_time = 0.0
        self.current_idx = 0 # For replaying path
        self.cash = 0.0
        self.inventory = 0
        self.history = {
            'time': [],
            'price': [],
            'inventory': [],
            'cash': [],
            'pnl': []
        }
    
    def step(self, delta_b: float, delta_a: float) -> Tuple[bool, bool, float]:
        """
        Advance one time step and determine if orders are filled.
        
        Args:
            delta_b: Bid distance from mid-price (must be > 0)
            delta_a: Ask distance from mid-price (must be > 0)
            
        Returns:
            filled_buy (bool): True if bid was filled
            filled_sell (bool): True if ask was filled
            new_price (float): Updated mid-price
        """
        dt = self.config.dt
        sigma = self.config.sigma
        
        # 1. Update Price (Arithmetic Brownian Motion for simplicity in HJB context, or Geometric)
        # Using Arithmetic dS = sigma * dW often matches Guéant paper assumptions better,
        # but Geometric is more realistic. Let's strictly follow the S0 * exp(...) for realism
        # unless user requested arithmetic. Math model said dS = sigma dW.
        # Let's stick to dS = sigma * dW (Arithmetic) to match HJB derivation exactly.
        
        
        # 1. Update Price
        if self.external_price_path is not None:
            # Replay Mode
            self.current_idx += 1
            if self.current_idx < len(self.external_price_path):
                self.current_price = self.external_price_path[self.current_idx]
            else:
                # End of path, just hold last price
                pass
        else:
            # Simulation Mode (Brownian)
            # dW ~ Normal(0, sqrt(dt))
            dW = self.rng.standard_normal() * np.sqrt(dt)
            self.current_price += sigma * dW 
        
        self.current_time += dt
        
        # 2. Determine Fills
        # Lambda = A * exp(-k * delta)
        # Prob of fill in dt approx = 1 - exp(-Lambda * dt)
        
        # Constants from model (should ideally be passed in or config)
        A = 140.0 
        k = 1.5
        
        lambda_b = A * np.exp(-k * delta_b)
        lambda_a = A * np.exp(-k * delta_a)
        
        prob_b = 1 - np.exp(-lambda_b * dt)
        prob_a = 1 - np.exp(-lambda_a * dt)
        
        filled_buy = self.rng.random() < prob_b
        filled_sell = self.rng.random() < prob_a
        
        # Update Inventory & Cash
        if filled_buy:
            self.inventory += 1
            self.cash -= (self.current_price - delta_b)
            
        if filled_sell:
            self.inventory -= 1
            self.cash += (self.current_price + delta_a)
            
        # Log state
        self._log_state()
        
        return filled_buy, filled_sell, self.current_price

    def _log_state(self):
        # Mark-to-market PnL
        pnl = self.cash + self.inventory * self.current_price
        
        self.history['time'].append(self.current_time)
        self.history['price'].append(self.current_price)
        self.history['inventory'].append(self.inventory)
        self.history['cash'].append(self.cash)
        self.history['pnl'].append(pnl)

    def run_simulation(self, strategy_fn):
        """
        Run full simulation using a strategy function.
        strategy_fn: (inventory, time) -> (delta_b, delta_a)
        """
        steps = int(self.config.T / self.config.dt)
        for _ in range(steps):
            delta_b, delta_a = strategy_fn(self.inventory, self.config.T - self.current_time)
            self.step(delta_b, delta_a)
        return pd.DataFrame(self.history)

def generate_price_path(config: SimulationConfig, steps: int) -> np.ndarray:
    """
    Generate pre-computed price path for reproducible testing.
    """
    rng = np.random.default_rng(config.seed + 1)
    dW = rng.standard_normal(steps) * np.sqrt(config.dt)
    path = np.zeros(steps + 1)
    path[0] = config.S0
    # Cumulative sum for Arithmetic Brownian Motion
    path[1:] = config.S0 + np.cumsum(config.sigma * dW)
    return path
