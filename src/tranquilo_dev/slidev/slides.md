---
# try also 'default' to start simple
theme: default
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
# background: https://source.unsplash.com/collection/94734566/1920x1080
# apply any windi css classes to the current slide
class: 'text-center'
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# show line numbers in code blocks
lineNumbers: false
# some information about the slides, markdown enabled
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
# persist drawings in exports and build
drawings:
  persist: false
# page transition
transition: slide-left
# use UnoCSS
css: unocss
---

<p style="font-size: 3em;">Tranquilo</p>

## A trustregion optimizer for economists by economists

Janoś Gabler, University of Bonn

Sebastian Gsell, LMU Munich

Tim Mensinger, University of Bonn

Mariam Petrosyan, University of Bonn


---
layout: center
---

# Prototypical optimization problems

<div class="grid grid-cols-2 gap-4">
<div>

## Agent-based Covid Model

- Fit simulated time series to data
- Computational bottleneck is serial
- Simulated cases are noisy
- 6 to 10 parameters
- Function evaluation takes 30 minutes
- Painful manual intervention needed
</div>
<div>

## DCDP Models

- Fit simulated choices to data
- Backwards induction is hard to parallelize
- Simulated choices are noisy
- 10 to 50 parameters
- Potentially expensive function

</div>
</div>

---
layout: center
---

# Goals

- Robust if function evaluations are noisy
- Parallelize at the level of function evaluations
- Suitable for data fitting problems
- Designed for non-expert users
- Assumption: Criterion function is expensive!

---
layout: center
---

# Optimization Problems

<div class="grid grid-cols-2 gap-12">
<div>

## Scalar Derministic


$\text{min}_{l \leq x \leq u} F(x)$

## Scalar Noisy

$\text{min}_{l \leq x \leq u} \mathbb{E} F(x, \epsilon)$

</div>
<div>

## Least-squares Deterministic

$\text{min}_{l \leq x \leq u} F(x) = \sum_{i} f_i(x)^2$

## Least-squares Noisy

$\text{min}_{l \leq x \leq u} \mathbb{E} F(x, \epsilon) = \mathbb{E} \sum_{i} f_i(x, \epsilon_i)^2$


</div>
</div>

---
layout: center
---

# Existing optimizers

|              | Nelder-Mead| Bobyqa     | PyBobyqa   |DFO-LS       |Pounders     | Parallel NM |
|--------------|------------|------------|------------|-------------|-------------|-------------|
| Library      | Nlopt      | Nlopt      | NAG        | NAG         | TAO         | (estimagic) |
| Class        | simplex    | trustregion| trustregion| trustregion | trustregion |simplex      |
| Noisy        | 〰         | ❌         | ✅         | ✅          | ❌          |〰           |
| Parallel     | ❌         | ❌         | 〰         | 〰          | ❌          | ✅           |
| Least-squares| ❌         | ❌         | ❌         |✅          | ✅          | ❌           |


---
layout: fact
---

<p style="font-size: 3em;">Recap: Trustregion optimizers</p>


---
layout: center
---

# Derivative free trustregion optimization

- Define a region around $x_k$
- Maintain a sample of $x$s on which criterion is evaluated
- Fit a regression or interpolation model on the sample
- Optimize the surrogate model to create a candidate
- Accept or reject the candidate
- Adjust the radius

---
layout: center
---

# Model quality, Rho, and Radius


<div class="flex gap-8">
<div>

$F$: criterion function

$k$: iteration counter

$x_k$: current x

$M_k$: surrogate model

$s_k$: candidate step


$\rho = \frac{F(x_k) - F(x_k + s_k)}{M_k(x_k) - M_k(x_k + s_k)}$

</div>
<div>

- Goal?
  - Sample few new points
  - Make large progress
- Model only needs to be good enough to point downhill
- Taylor like error bounds on $M_k$
  - Small $\rho$: decrease radius
  - Large $\rho$: increase radius
- Preview: This will fail in noisy case!


</div>
</div>


---
layout: center
---

# Least squares structure

- Surrogate should allow for internal minima
  - Quadratic model: $1 + n + \frac{n(n+1)}{2}$ points
  - Regularized quadratic model: $2n + 1$ points
- Underdetermined models often defeat intuition
- Least-square structure helps
  - Fit linear models $m_{i}(x) = a_{i} + b_{i}^T x$ for each residual $f_i(x)$
  - $M(x) = \sum_i m_{i}(x)^2 = \sum_i a_{i}^2 + \sum_i 2a_{i} b_{i}^T x + \sum_i x^T b_{i}b_{i}^T x = \alpha + g^T x + \frac{1}{2} x^T H x$
  - Fully determined model with just $n + 1$ points

---
layout: fact
---

<p style="font-size: 3em;">Noise-free and serial case</p>

---
layout: center
---

# Tranquilo and Tranquilo-LS

- **T**rust**R**egion **A**daptive **N**oise robust **QU**adrat**I**c or **L**inear approximation **O**ptimizer
- Fairly standard trustregion optimizers
  - Sampling: Approximate Fekete points
  - Subsolvers: GQTPAR or BNTR
  - Radius management: Same as pounders
- Key differences
  - History search and variable sample size
  - Switch from round to cubic trustregions close to bounds
  - Same code for scalar and least-squares version!

---
layout: center
---

# Tranquilo-LS in action


<div class="grid grid-cols-2 gap-12">
<div>

- Criterion function: $f(x) = \sum_i x_i^2$
- Start parameters: $x_0 = (1, 1)$
- Global optimum: $x^* = (0, 0)$


</div>
<div>

<img src="sphere.png" class="rounded" width="500" />

</div>
</div>


---
layout: center
transition: fade
---

<img src="animation_0.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="animation_1.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="animation_2.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="animation_3.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="animation_4.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="animation_5.svg" class="rounded" width="500" />


---
layout: center
---

# Benchmarking

- Moré-Wild Benchmark set
- 52 leasts-squares problems with 2 to 12 parameters
- Was used in pounders, PyBobyqa and DFO-LS papers
- Local optimization problems without bounds
- Differentiable (but we don't use derivatives)
- Profile plots
  - Y-axis: share of solved problems
  - X-axis: (normalized) runtime in terms of function evaluations


---
layout: center
---

# Benchmark: Tranquilo vs. other optimizers

<img src="bld/figures/profile_plots/scalar_and_ls.svg" class="rounded" width="700" />


---
layout: fact
---

<p style="font-size: 3em;">Parallel case</p>


---
layout: center
---

# Cost model for parallel optimization

- Most economists have access to:
  - 4 to 8 cores on a laptop/desktop
  - 16 to 64 cores on a server
- In practice, criterion functions are often not parallelized
  - Lack of knowledge or time to write parallel code
  - Some problems are hard to parallelize
- Cost model with batch size $b$:
  - Up to $b$ parallel evaluations have the same cost as one evaluation

---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="origin_plot.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="line_points_1.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="line_points_2.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="line_points_3.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 2: Speculative sampling

<img src="origin_plot.svg" class="rounded" width="400" />

---
layout: center
transition: fade
---

# Idea 2: Speculative sampling

<img src="empty_speculative_trustregion_small_scale.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 2: Speculative sampling

<img src="sampled_speculative_trustregion_small_scale.svg" class="rounded" width="400" />


---
layout: center
---

# Combining the two

- If candidate is close to trustregion border:
  - Allocate up to three function evaluations to a line search
- If "free" function evaluations are left:
  - Do speculative sampling
- If any line-search or speculative point yields improvement
  - Accept them as new x


---
layout: center
---

# Line search + Speculation

<img src="line_and_speculative_points.svg" class="rounded" width="400" />


---
layout: center
---

# Benchmark: Parallel tranquilo vs. DFOLS

<img src="bld/figures/profile_plots/parallelization_ls.svg" class="rounded" width="700" />


---
layout: fact
---

<p style="font-size: 3em;">Noisy case</p>


---
layout: center
---

# Problems caused by noise

- Model does not approximate well
- $\rho$ is low in many iterations
- Radius shrinks to zero -> optimization fails

---
layout: center
---

# How DFOLS handles noise

- Evaluate criterion multiple times at each point and average
- Re-start if trustregion collapses
- How many evaluations is decided by the user based on
  - Current radius
  - $\rho$
  - Iteration counter $(k)$
  - restart counter
- Very hard to get right!


---
layout: center
transition: fade
---

# Why is it hard to pick sample sizes?

<img src="noise_plot_1.svg" class="rounded" width="450" />

---
layout: center
transition: fade
---

# Why is it hard to pick sample sizes?

<img src="noise_plot_2.svg" class="rounded" width="450" />


---
layout: center
transition: fade
---

# Why is it hard to pick sample sizes?

<img src="noise_plot_3.svg" class="rounded" width="450" />


---
layout: center
---

# A different perspective on radius and $\rho$

<div class="grid grid-cols-2 gap-4">
<div>

## Noise-free case

- Problem: Approximation error
- Tuning parameter: Radius
- Performance metric: $\rho$


</div>
<div>

## Noisy case

- Problem: Random error
- Tuning parameter: Sample size
- Performance metric: $\rho_{noise}$

</div>
</div>


---
layout: center
---

# Step 1: Estimate noise variance

- Scan history for all points with multiple evaluations of criterion
- Restrict to ones that are
  - close to current trustregion
  - have the most function evaluations
- Estimate
  - $\sigma_k$: variance of the noise on a scalar criterion function
  - $\Sigma_k$: covariance matrix of the noise on the least-squares residuals
- Locally constant approximation to an arbitrary noise term

---
layout: center
---

# Step 2: Simulate $\rho_{noise}$

- Surrogate model $M_k(x)$ approximates the criterion function
- Use $M_k$ and $\sigma_k$ to simulate a noisy sample
- Fit a model $\tilde{M_{k}}(x)$ on the simulated sample
- Optimize $\tilde{M_{k}}(x)$ to get a suggested step $\tilde{s_k}$
- $\rho_{noise} = \frac{M(x_k) - M(x_k + \tilde{s}_k)}{\tilde{M_k}(x_k) - \tilde{M_k}(x_k + \tilde{s}_k)}$
- Repeat the simulation
- Increase sample size if most rhos are small


---
layout: center
---

# Noise in the acceptance step

- Noise free acceptance step is trivial
- Now: Does candidate have a lower expected value?
- Intuition: Needs large sample if values are close


---
layout: center
---

# Step 3: Power analysis

- Power analysis: $\frac{n_1 n_2}{n_s + n_2} \geq \sigma^2 \Big[\frac{\Phi^{-1}(1 - \alpha) + \Phi^{-1}(1 - \beta)}{\Delta_{min}} \Big]^2$



- $n_1, n_2$: number of evaluations at current and candidate x
- $\alpha$: confidence level
- $1 - \beta$: power level
- $\Delta_{min} = M_k(x_k) - M_k(x_k + s_k)$: Minimal detectable effect size
- Can calculate $n_1$ and $n_2$ that minimize new function evaluations




---
layout: center
---

# Benchmark: Noisy tranquilo vs. DFOLS

<img src="bld/figures/profile_plots/noisy_ls.svg" class="rounded" width="700" />


---
layout: center
---

# Summary

- We created a modular framework for derivative free trustregion optimization
- Same code for scalar and least-squares version
- Performance in noise-free and serial setting is similar to existing optimizers
- Two ideas for parallelization:
  - Line search
  - Speculative sampling
- Two ideas for noise handling
  - Simulate $\rho_{noise}$ in sampling step
  - Power analysis for acceptance step
