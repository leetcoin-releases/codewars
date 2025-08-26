/*
Solution
*/
function read(tape, head, moves) {
    let result = "";
    for (let move of moves) {
        result += tape[head];
        if (move === '>') head++;
        else if (move === '<') head--;
    }
    return result;
}





/*
Sample Tests
*/
const { assert } = require('chai')

describe('Fixed tests', () => {
  it('should match the example', () => {
    assert.strictEqual(read('011010', 2, '>>><'), '1010');
  });
  it('should not read any bits if there are no moves', () => {
    assert.strictEqual(read('011010', 2, ''), '');
  })
  it('should read the tape as-is if head = 0, and moves are only >', () => {
    // except the last bit
    assert.strictEqual(read('011010', 0, '>>>>>'), '01101');
  })
  it('should read the tape in reverse if head at the end, and moves are only <', () => {
    // except the first bit
    assert.strictEqual(read('011010', 5, '<<<<<'), '01011');
  })
})