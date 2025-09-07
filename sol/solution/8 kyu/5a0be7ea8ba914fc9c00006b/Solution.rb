=begin
Solution
=end
def sakura_fall(v)
  return 0.0 if v <= 0
  400.0 / v
end





=begin
Sample Tests
=end
describe "Solution" do
    $DELTA = 1e-6

  it "Fixed tests" do
    expect(sakura_fall(5)).to be_within($DELTA).of(80)
    expect(sakura_fall(10)).to be_within($DELTA).of(40)
    expect(sakura_fall(200)).to be_within($DELTA).of(2)
    expect(sakura_fall(-1)).to be_within($DELTA).of(0)
  end
end