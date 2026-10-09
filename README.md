# Optimal Trade Sizing

Finds the trade size that maximizes profit when larger trades move the price against you (market impact).

## Model

Profit for a trade of `x` shares:

```
P(x) = αx − βx² − cx
```

- `α`: expected return per share
- `β`: market impact coefficient (impact cost grows with the square of size)
- `c`: transaction cost per share

Setting the marginal profit to zero gives the optimal size:

```
x* = (α − c) / (2β)
```

The trade breaks even at `x = (α − c) / β`. If `α ≤ c`, no trade size is profitable.

## Base case

With `α = $0.05`, `β = 0.0001` and `c = $0.01`:

- Optimal size: 200 shares
- Maximum profit: $4.00
- Break-even size: 400 shares

## Usage

```bash
pip install -r requirements.txt
python optimaltradesizing.py
```

The script prints the solution and plots two charts: the profit curve, and marginal benefit against marginal cost, which cross at the optimum.
