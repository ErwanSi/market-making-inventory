# Mathematical Model: Optimal Market Making with Inventory Risk

This document details the mathematical framework used in `src/models/inventory_hjb.py` and `src/solvers/hjb_solver.py`.

## 1. Market Dynamics

We assume a mid-price $S_t$ following an arithmetic Brownian motion:
$$ dS_t = \sigma dW_t $$
where $\sigma$ is the volatility.

The Market Maker (MM) controls the bid and ask quotes $\delta_t^b$ and $\delta_t^a$, which are distances from the mid-price.
$$ P_t^b = S_t - \delta_t^b $$
$$ P_t^a = S_t + \delta_t^a $$

The arrival of market orders is modeled by Poisson processes $N_t^b$ (sell orders hitting our bid) and $N_t^a$ (buy orders hitting our ask) with intensities:
$$ \Lambda^b(\delta^b) = A e^{-k \delta^b} $$
$$ \Lambda^a(\delta^a) = A e^{-k \delta^a} $$

## 2. Optimization Problem (HJB)

The MM maximizes the expected utility of terminal wealth. We use an Exponential Utility (CARA) function:
$$ U(x) = -e^{-\gamma x} $$
where $\gamma$ is the risk aversion parameter.

The value function $u(t, x, q, s)$ satisfies the Hamilton-Jacobi-Bellman (HJB) equation.
Using the change of variables from **Guéant et al. (2013)**, the problem reduces to solving a system of linear ODEs for functions $v_q(t)$ (related to inventory level $q$).

### The Value Function Ansatz
$$ u(t, x, q, s) = -e^{-\gamma(x + qs)} v_q(t)^{-\frac{\gamma}{k}} $$

### System of ODEs
For inventory levels $q \in \{-Q, \dots, Q\}$:
$$ \dot{v}_q(t) = \alpha q^2 v_q(t) - \eta \left( v_{q-1}(t) + v_{q+1}(t) \right) $$
where:
- $\alpha = \frac{k^2 \sigma^2 \gamma}{2}$ (Risk factor)
- $\eta = A \left( 1 + \frac{\gamma}{k} \right)^{-1}$ (Liquidity factor - *Note: exact form depends on specific approximation, using standard form here*)

Terminal Condition: $v_q(T) = 1$.

## 3. Optimal Quotes

Once $v_q(t)$ is computed (or approximated by its asymptotic value), the optimal quotes are:

$$ \delta_t^{b*} = \frac{1}{k} \ln \left( \frac{v_q(t)}{v_{q+1}(t)} \right) + \frac{1}{\gamma} \ln \left( 1 + \frac{\gamma}{k} \right) $$
$$ \delta_t^{a*} = \frac{1}{k} \ln \left( \frac{v_q(t)}{v_{q-1}(t)} \right) + \frac{1}{\gamma} \ln \left( 1 + \frac{\gamma}{k} \right) $$

## 4. Asymptotic (Stationary) Approximation

For $T \to \infty$, the solution becomes stationary. The quotes depend only on the current inventory $q$.
We approximate this using the closed-form expansion for small $\gamma$:

$$ \delta^b(q) \approx \frac{1}{k} \ln \left( 1 + \frac{\gamma}{k} \right) + \frac{2q+1}{2} \sqrt{\frac{\sigma^2 \gamma}{2kA}} $$
*Refined approx (Guéant 2013)*:
$$ \delta^b(q) = \frac{1}{k} \ln\left( \frac{\lambda(0)}{\gamma \sigma^2} \frac{1}{1 + \frac{2q}{\gamma \sigma^2}} \dots \right) $$

In our code, we will implement the **exact spectral solution** or the **high-precision ODE solver** results if possible, but default to the robust approximation:

**Default Strategy Implemented:**
$$ \delta^{b,a}(q) = \delta_{symmetric} \pm q \cdot \text{inventory\_risk\_shift} $$
$$ \delta_{symmetric} = \frac{1}{γ} \ln(1 + γ/k) $$ (Risk Neutral base)  
Correction term derived from Volatility Risk:
$$ \text{shift} = \gamma \sigma^2 (T-t) $$ (Avellaneda) OR Stationary: $\frac{\sigma^2 \gamma}{A k}$ factor.

## 5. Metrics

- **PnL**: $X_t + q_t S_t - X_0$
- **Sharpe Ratio**: $\frac{E[Returns]}{\sqrt{Var[Returns]}}$
- **Max Drawdown**
