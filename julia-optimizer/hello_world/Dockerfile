# Dockerfile — ARM64 Julia-inside-Lambda (Python 3.11 runtime)
FROM public.ecr.aws/lambda/python:3.11-arm64

ARG JULIA_VERSION=1.11.5

# --- install Julia (Linux aarch64) ---
RUN yum -y install curl tar gzip xz && \
    curl -L https://julialang-s3.julialang.org/bin/linux/aarch64/1.11/julia-${JULIA_VERSION}-linux-aarch64.tar.gz \
    | tar -xz -C /opt && \
    ln -s /opt/julia-${JULIA_VERSION} /opt/julia && \
    ln -s /opt/julia/bin/julia /usr/local/bin/julia

# Add Julia library path so libjulia can find correct libstdc++ during Lambda init
ENV LD_LIBRARY_PATH="/opt/julia-${JULIA_VERSION}/lib/julia:${LD_LIBRARY_PATH}"
# Ensure newer libstdc++ is discoverable by default loader
RUN ln -sf /opt/julia-${JULIA_VERSION}/lib/julia/libstdc++.so.6 /usr/lib64/libstdc++.so.6

# --- Python deps ---
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# --- Julia deps ---
RUN julia -e 'using Pkg; Pkg.add(["PythonCall","JuMP","HiGHS"]); Pkg.precompile()'

# --- function code ---
COPY optimize.jl ${LAMBDA_TASK_ROOT}/optimize.jl
COPY app.py       ${LAMBDA_TASK_ROOT}/app.py

CMD ["app.lambda_handler"]
