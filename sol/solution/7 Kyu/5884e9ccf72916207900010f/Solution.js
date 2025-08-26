/*
Solution
*/
function diff(s1, s2) {
  return new Set([...s1].filter(x => !s2.has(x)));
}





/*
Sample Tests
*/
describe("Basic tests", function()  {
    const chai = require('chai'), {assert} = chai;
    chai.config.truncateThreshold = 0;

  const A = new Set([1,2,3,4]), B = new Set([1,3,5,7]), AB = new Set([2,4]), BA = new Set([5,7]), E = new Set();
      
  it("A - A", function() { assert.deepEqual( diff(A,A), E, "A - A == {}") });
  it("A - B", function() {  assert.deepEqual( diff(A,B), AB ) });
  it("B - A", function() {  assert.deepEqual( diff(B,A), BA ) });
  it("A - {}", function() {  assert.deepEqual( diff(A,E), A ) });
  it("B - {}", function() {  assert.deepEqual( diff(B,E), B ) });  
});