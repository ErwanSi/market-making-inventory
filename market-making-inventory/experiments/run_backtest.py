import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.simulator import OrderBookSimulator, SimulationConfig
from src.models.inventory_hjb import InventoryHJBModel, MarketParameters
from src.solvers.hjb_solver import HJBSolver

def run_backtest():
    print("Starting Backtest...")
    
    # Configuration
    config = SimulationConfig(T=1.0, dt=1/2520, sigma=0.5) # Higher sigma to see effects
    params = MarketParameters(sigma=0.5, gamma=0.1, k=1.5, A=140.0)
    
    # Initialize Models
    hjb_model = InventoryHJBModel(params)
    solver_hjb = HJBSolver(params, max_inventory_Q=20)
    
    # Strategies definitions
    def strategy_naive(q, t_left):
        # Fixed symmetric spread
        fixed_spread = 0.05
        return fixed_spread, fixed_spread
        
    def strategy_hjb_approx(q, t_left):
        # Analytical Approximation
        return hjb_model.get_quotes(q, t_left)

    def strategy_hjb_exact(q, t_left):
        # Matrix Exponential exact solution
        return solver_hjb.get_optimal_quotes(q, t_left)

    # Run Simulations
    results = {}
    strategies = {
        'Naive': strategy_naive,
        'HJB_Approx': strategy_hjb_approx,
        'HJB_Exact': strategy_hjb_exact
    }
    
    for name, strat in strategies.items():
        print(f"Running {name}...")
        sim = OrderBookSimulator(config)
        df = sim.run_simulation(strat)
        results[name] = df
        
        print(f"{name} Final PnL: {df['pnl'].iloc[-1]:.2f}")
        
    # Plotting
    plot_results(results)
    print("Backtest Complete. Results saved in experiments/results/")

def plot_results(results):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'results'), exist_ok=True)
    
    # 1. PnL Trajectories
    plt.figure(figsize=(10, 6))
    for name, df in results.items():
        plt.plot(df['time'], df['pnl'], label=name)
    plt.title('PnL Trajectories')
    plt.xlabel('Time')
    plt.ylabel('PnL')
    plt.legend()
    plt.grid(True)
    plt.savefig('experiments/results/pnl.png')
    plt.close()
    
    # 2. Inventory Distribution
    plt.figure(figsize=(10, 6))
    for name, df in results.items():
        plt.hist(df['inventory'], bins=20, alpha=0.5, label=name, density=True)
    plt.title('Inventory Distribution')
    plt.xlabel('Inventory')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.savefig('experiments/results/inventory_dist.png')
    plt.close()
    
    # 3. Inventory vs Time (for HJB Exact) (Detail)
    if 'HJB_Exact' in results:
        df = results['HJB_Exact']
        plt.figure(figsize=(10, 6))
        plt.plot(df['time'], df['inventory'], color='purple')
        plt.title('HJB Exact: Inventory Management')
        plt.xlabel('Time')
        plt.ylabel('Inventory')
        plt.grid(True)
        plt.savefig('experiments/results/hjb_inventory.png')
        plt.close()

if __name__ == "__main__":
    run_backtest()
