#=
Solution
=#
function sakura_fall(v)
    if v <= 0
        return 0.0
    else
        return 400.0 / v
    end
end





#=
Sample Tests
=#
using FactCheck

facts("sakura_fall") do

  context("basic tests") do
    @fact sakura_fall(5) --> roughly(80; atol=1e-6)
    @fact sakura_fall(10) --> roughly(40; atol=1e-6)
    @fact sakura_fall(200) --> roughly(2; atol=1e-6)
    @fact sakura_fall(-1) --> roughly(0; atol=1e-6)
  end
end