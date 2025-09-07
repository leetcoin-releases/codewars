/*
Solution
*/
function sakuraFall(v) {
  if (v <= 0) return 0;
  return 400 / v;
}





/*
Sample Tests
*/
describe("The falling speed of petals", () => {
    const {assert} = require("chai");
    const DELTA = 1e-6;

  it("sample tests", () => {
    assert.approximately(sakuraFall(5),80, DELTA)
    assert.approximately(sakuraFall(10),40, DELTA)
    assert.approximately(sakuraFall(200),2, DELTA)
    assert.approximately(sakuraFall(-1),0, DELTA)
    });
});