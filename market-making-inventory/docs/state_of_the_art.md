# State of the Art: Optimal Market Making with Inventory Risk

This document summarizes the key theoretical frameworks and recent advancements in optimal market making, focusing on stochastic control approaches and inventory management.

## 1. High-Frequency Trading in a Limit Order Book (Avellaneda & Stoikov, 2008)

**Summary:**
The foundational paper by Avellaneda and Stoikov applies stochastic optimal control to the problem of a market maker (MM) maximizing expected utility of terminal wealth while managing inventory risk. It bridges the gap between the varying inventory literature (Ho & Stoll, 1981) and modern limit order books.

**Key Model Dynamics:**
- **Mid-price ($S_t$):** Follows Arithmetic Brownian Motion (or Geometric):
  $$ dS_t = \sigma dW_t $$
- **Arrival Rates:** Poisson processes for buy ($N_t^b$) and sell ($N_t^a$) orders, with intensities $\lambda$ depending exponentially on the distance from mid-price $\delta$:
  $$ \lambda(\delta) = A e^{-k \delta} $$
  Where $A$ and $k$ are market parameters.

**Optimization Problem:**
Maximize expected exponential utility (CARA) of terminal wealth:
$$ \sup_{\delta_t^a, \delta_t^b} \mathbb{E} \left[ -e^{-\gamma (X_T + q_T S_T)} \right] $$
where $X_T$ is cash, $q_T$ is inventory, and $\gamma$ is risk aversion.

**Key Equations (Approximation):**
The optimal bid and ask quotes are centered around a "Reservation Price" $r(s, q, t)$:
$$ r(s, q, t) = s - q \gamma \sigma^2 (T-t) $$
Optimal spread around reservation price:
$$ \delta^a + \delta^b = \frac{2}{k} \ln \left( \frac{2}{\gamma \sigma^2} \right) + \dots $$
*Note: The exact solution involves solving a system of ODEs or approximating the value function.*

**Limits:**
- Assumes constant volatility $\sigma$.
- Inventory penalty is implicit in the utility function; hard constraints require boundary conditions.
- Finite horizon $T$ effect vanishes for stationary solutions.

---

## 2. Dealing with the Inventory Risk (Guéant, Lehalle, Fernandez-Tapia, 2013)

**Summary:**
Guéant et al. provide a closed-form approximate solution to the Avellaneda-Stoikov problem by transforming the HJB equation into a system of linear Ordinary Differential Equations (ODEs). This makes the strategy computationally efficient and practical for real-time implementation.

**Key Contributions:**
- **Change of Variables:** Reduces the non-linear HJB PDE to a system of linear equations.
- **Asymptotic Behavior:** Derives stationary optimal quotes for infinite horizon (or long $T$), which is very useful for continuous trading.

**Key Equations:**
Infinite horizon stationary quotes $\delta^b, \delta^a$ as a function of inventory $q$:
$$ \delta^b(q) = \frac{1}{k} \ln \left( \frac{\lambda(0)}{ \gamma \sigma^2 (2q+1) / 2 } \right) \quad (\text{Approximation}) $$
More precisely, using the asymptotic expansion:
$$ \delta^b(q) \approx \frac{1}{k} \ln\left(1 + \frac{\gamma}{k}\right) + \frac{2q+1}{2} \frac{\gamma \sigma^2}{A k} $$
(Ideally, one solves the exact spectral problem for the matrix associated with the ODE system).

**Comparison to Avellaneda:**
- More rigorous derivation of the asymptotic strategy.
- Explicit handling of inventory bounds $Q_{max}$.

---

## 3. Review of Adaptive Market Making (SIAM 2024 / Recent Works)

**Focus:**
Recent literature (e.g., *Adaptive Optimal Market Making Strategies*, 2024) focuses on relaxing the strong assumptions of parametric intensity forms (like $A e^{-k\delta}$).

**Approaches:**
1.  **Online Learning / RL:** Using Reinforcement Learning (PPO, DQN) to learn the optimal policy $\pi(s, q)$ without assuming a specific arrival model.
2.  **Adaptive Parameters:** Bayesian updates or Kalman Filters to estimate $A, k, \sigma$ in, real-time.
3.  **Alpha-signal Integration:** Incorporating short-term price drift $\mu$ (Alpha) into the HJB framework:
    $$ r(s, q, t) = s + \frac{\mu}{\gamma \sigma^2} - q \gamma \sigma^2 (T-t) $$

**Limits:**
- RL approaches require vast amounts of data and are hard to interpret.
- Adaptive models may be unstable during regime shifts if learning rates are not tuned.

---

## Comparison of Methods

| Feature | Avellaneda-Stoikov (2008) | Guéant et al. (2013) | Deep RL (2024+) |
| :--- | :--- | :--- | :--- |
| **Model** | Stochastic Control (HJB) | Stochastic Control (Linear ODE) | Model-Free MDP |
| **Solution** | Numerical / Approx | Semi-Closed Form | Neural Network Approx |
| **Pros** | Theoretical Foundation | Computable, Stable | Captures complex dynamics |
| **Cons** | Hard to solve exactly | Assumes Poisson/Exp | Sample inefficient, Blackbox |
| **Inventory** | Soft penalty (Utility) | Hard & Soft constraints | Learned penalty |

---

## Project Direction (market-making-inventory)

We will implement the **Guéant et al.** approach as the core mathematical model (Phase 4 Solvers) due to its tractability and robustness.
We will compare this against:
1.  **Baseline Strategy:** Naive fixed spread.
2.  **RL Strategy (Phase 5):** PPO agent learning to manage inventory from scratch.

This hybrid approach ensures we have a scientifically rigorous baseline (Guéant) and an experimental "state-of-the-art" comparison (RL).
