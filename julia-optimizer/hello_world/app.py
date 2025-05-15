# app.py — Python ⇄ Julia via juliacall
import json
import sys
from pathlib import Path

import numpy as np
from juliacall import Main as jl

# jl.include("optimize.jl")
jl.include(str((Path(__file__).resolve().parent / "optimize.jl")))

optimize_portfolio = jl.OptMod.optimize_portfolio


def lambda_handler(event, context):
    returns = np.asarray(event.get("returns", [0.05, 0.10, 0.12]))
    weights = optimize_portfolio(returns)
    return {"statusCode": 200, "body": json.dumps({"weights": list(weights)})}


if __name__ == "__main__":
    try:
        # Try to load event from file if provided
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--event", type=str, default=None, help="Path to event JSON file")
        args = parser.parse_args()
        if args.event:
            with open(args.event) as f:
                event = json.load(f)
        else:
            event = {"returns": [0.05, 0.10, 0.12]}
        print("Invoking lambda_handler with event:", event)
        result = lambda_handler(event, None)
        print("Lambda result:", result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
