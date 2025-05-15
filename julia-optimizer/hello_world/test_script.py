#!/usr/bin/env python
import json
import sys
from pathlib import Path

import numpy as np

try:
    from juliacall import Main as jl

    # Load the Julia code
    print("Loading Julia module...")
    jl.include(str((Path(__file__).resolve().parent / "optimize.jl")))

    # Get the function
    optimize_portfolio = jl.OptMod.optimize_portfolio

    # Test data
    returns = np.array([0.05, 0.10, 0.12])

    # Run optimization
    print("Running optimization...")
    weights = optimize_portfolio(returns)

    # Print results
    print(f"Optimal weights: {weights}")
    print(f"Result as JSON: {json.dumps({'weights': list(weights)})}")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
