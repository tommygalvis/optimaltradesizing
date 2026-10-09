import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, brentq
import warnings
warnings.filterwarnings('ignore')

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
np.set_printoptions(precision=4, suppress=True)

# Color palette
COLORS = {
    'primary': '#2ecc71',
    'secondary': '#3498db',
    'accent': '#e74c3c',
    'neutral': '#95a5a6',
}

print("Environment configured successfully.")
print(f"NumPy version: {np.__version__}")
def profit_function(x, alpha, beta, c):
    """
    Compute profit for a given trade size.
    
    P(x) = αx - βx² - cx
    
    Args:
        x: Trade size (shares)
        alpha: Expected return per share
        beta: Market impact coefficient
        c: Transaction cost per share
    
    Returns:
        Profit value
    """
    return alpha * x - beta * x**2 - c * x


def optimal_trade_size(alpha, beta, c):
    """
    Compute optimal trade size analytically.
    
    x* = (α - c) / (2β)
    """
    if alpha <= c:
        return 0  # No profitable trade exists
    return (alpha - c) / (2 * beta)


def analyze_trade_size(alpha, beta, c, name=""):
    """
    Complete analysis of trade size optimization.
    """
    x_opt = optimal_trade_size(alpha, beta, c)
    p_opt = profit_function(x_opt, alpha, beta, c)
    
    # Break-even points
    # P(x) = 0 => αx - βx² - cx = 0 => x(α - c - βx) = 0
    x_breakeven = (alpha - c) / beta if alpha > c else 0
    
    return {
        'name': name,
        'optimal_size': x_opt,
        'max_profit': p_opt,
        'breakeven_size': x_breakeven,
        'marginal_profit_at_opt': alpha - 2*beta*x_opt - c,  # Should be ~0
    }

# Base case parameters
ALPHA = 0.05      # $0.05 expected profit per share
BETA = 0.0001     # Market impact coefficient
C = 0.01          # $0.01 transaction cost per share

# Analyze base case
base_result = analyze_trade_size(ALPHA, BETA, C, "Base Case")

print("=" * 60)
print("TRADE SIZE OPTIMIZATION")
print("=" * 60)
print(f"\nParameters:")
print(f"  α (expected return/share):  ${ALPHA:.4f}")
print(f"  β (market impact coef):     {BETA:.6f}")
print(f"  c (transaction cost/share): ${C:.4f}")
print(f"\nOptimal Solution:")
print(f"  x* = (α - c) / (2β)")
print(f"  x* = ({ALPHA} - {C}) / (2 × {BETA})")
print(f"  x* = {base_result['optimal_size']:.0f} shares")
print(f"\nResults:")
print(f"  Maximum profit:    ${base_result['max_profit']:.2f}")
print(f"  Break-even size:   {base_result['breakeven_size']:.0f} shares")
print(f"  Marginal profit:   ${base_result['marginal_profit_at_opt']:.6f} (≈ 0 at optimum)")

# Visualize profit function
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Profit curve
x_range = np.linspace(0, 500, 500)
profits = profit_function(x_range, ALPHA, BETA, C)

axes[0].plot(x_range, profits, color=COLORS['secondary'], linewidth=2.5, label='P(x) = αx - βx² - cx')
axes[0].axhline(0, color=COLORS['neutral'], linestyle='-', alpha=0.5)
axes[0].axvline(base_result['optimal_size'], color=COLORS['primary'], linestyle='--', 
                linewidth=2, label=f"x* = {base_result['optimal_size']:.0f}")
axes[0].scatter([base_result['optimal_size']], [base_result['max_profit']], 
                color=COLORS['primary'], s=150, zorder=5, edgecolors='white', linewidth=2)
axes[0].fill_between(x_range, 0, profits, where=(profits > 0), alpha=0.2, color=COLORS['primary'])
axes[0].fill_between(x_range, 0, profits, where=(profits < 0), alpha=0.2, color=COLORS['accent'])

axes[0].set_xlabel('Trade Size (shares)')
axes[0].set_ylabel('Profit ($)')
axes[0].set_title('Profit Function: P(x) = αx - βx² - cx', fontweight='bold')
axes[0].legend(loc='upper right')
axes[0].set_xlim(0, 500)

# Right: Marginal analysis
marginal_benefit = np.full_like(x_range, ALPHA - C)  # α - c (constant)
marginal_cost = 2 * BETA * x_range  # 2βx

axes[1].plot(x_range, marginal_benefit, color=COLORS['primary'], linewidth=2.5, 
             label=f'Marginal Benefit = α - c = ${ALPHA - C:.2f}')
axes[1].plot(x_range, marginal_cost, color=COLORS['accent'], linewidth=2.5,
             label='Marginal Cost = 2βx')
axes[1].axvline(base_result['optimal_size'], color=COLORS['neutral'], linestyle='--', 
                linewidth=2, alpha=0.7)
axes[1].scatter([base_result['optimal_size']], [2 * BETA * base_result['optimal_size']], 
                color=COLORS['secondary'], s=150, zorder=5, edgecolors='white', linewidth=2,
                label=f"Optimal: x* = {base_result['optimal_size']:.0f}")

axes[1].set_xlabel('Trade Size (shares)')
axes[1].set_ylabel('Marginal $/share')
axes[1].set_title('Marginal Analysis: MB = MC at Optimum', fontweight='bold')
axes[1].legend(loc='upper left')
axes[1].set_xlim(0, 500)
axes[1].set_ylim(0, 0.06)

plt.tight_layout()
plt.show()

print("\nKey Insight: The optimal trade size occurs where marginal benefit equals marginal cost.")
print(f"At x* = {base_result['optimal_size']:.0f}: MB = ${ALPHA - C:.4f}, MC = ${2*BETA*base_result['optimal_size']:.4f}")
