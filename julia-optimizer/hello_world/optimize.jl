# optimize.jl — unchanged
module OptMod
using JuMP, HiGHS
export optimize_portfolio

function optimize_portfolio(r::AbstractVector{<:Real})
    println("optimize_portfolio")
    n = length(r)
    model = Model(HiGHS.Optimizer)
    @variable(model, w[1:n] >= 0)
    @constraint(model, sum(w) == 1)
    @objective(model, Max, sum(r .* w))
    optimize!(model)
    return value.(w)
end

end
