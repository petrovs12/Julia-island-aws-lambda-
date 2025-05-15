# Julia-island-aws-lambda

Minimally working example of a 'Julia island' within AWS Lambda infrastructure.

## Motivation

Idea is Julia is state of the art for mathematical optimization, differentiable programming, and scientific computing. However, some tooling is lacking and it's risky to have a a full product in Julia- only. Adopiton is not exponential

 Python master of everything is one of the good choices for a 'glue' language for cloud/serverless, devops, and ML glue code.

Julia does have some advantages for extending math optimization algorithms.

This mini-project demonstrates a pattern for leveraging Julia's state-of-the-art optimization libraries (e.g., JuMP, HiGHS) inside a serverless Python AWS Lambda. The core optimization logic is written in Julia (`optimize.jl`), while all developer tooling, API glue, and deployment are handled in Python (`app.py`).

- **Why?**
  - Julia offers best-in-class mathematical optimization and scientific computing libraries.
  - Python is (a) lingua franca for 'glue' stuff, with tons of tooling and batteries for everything.
  - This pattern lets you keep your Lambda handler, debugging, and deployment in Python, but call into Julia for heavy-lifting math/optimization.

## How it works

- `optimize.jl`: Julia module with the optimization logic (here, a simple portfolio optimizer using JuMP/HiGHS).
- `app.py`: Python Lambda handler. Uses [juliacall](https://github.com/JuliaPy/JuliaCall) to load and call the Julia module.
- Dockerfile: Installs both Python and Julia, sets up the Lambda runtime, and ensures the right libraries are available for both.
- `sam` (Serverless Application Model): Used for local build and invoke, and for deployment.

## Local development & testing

You can run and debug the handler locally, exactly as Lambda would:

```sh
cd julia-optimizer
sam build
sam local invoke -e hello_world/test-event.json
```

Or, to run the handler directly in the built Docker image:

```sh
cd julia-optimizer/hello_world
# Default event
docker run --rm julia-lambda-test python app.py
# Custom event
docker run --rm -v "$(pwd)/test-event.json:/var/task/test-event.json" julia-lambda-test python app.py --event /var/task/test-event.json
```

## Files of interest

- `hello_world/optimize.jl`: Julia optimization logic (edit this for your use case)
- `hello_world/app.py`: Python Lambda handler (edit this for your API/glue logic)
- `hello_world/Dockerfile`: Lambda image build (edit only if you need more system deps)

## Notes
- The Dockerfile and Lambda image are set up to ensure Julia's libraries are available at runtime (see `LD_LIBRARY_PATH` and symlink logic).
- This pattern is robust for both local and cloud Lambda execution.
- You can extend this to expose more Julia functions, or to use other Julia packages, by editing `optimize.jl` and updating the Python glue in `app.py`.
