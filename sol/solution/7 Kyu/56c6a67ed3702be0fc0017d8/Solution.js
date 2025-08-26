/*
Solution
*/
Object.defineProperty(Array.prototype, 'toDictionary', {
    value: function toDictionary(keyFn, valueFn) {
        const result = {};
        for (let i = 0; i < this.length; i++) {
            const el = this[i];
            const key = keyFn(el, i, this);
            const value = valueFn ? valueFn(el, i, this) : el;
            result[key] = value;
        }
        return result;
    }
});





/*
Sample Tests
*/
describe('Tests', () => {
    const chai = require('chai'), { assert } = chai;
    chai.config.truncateThreshold = 0;

    it('Initial Tests', () => {
        let arr = [1, 2, 3, 4, 5];
        assert.deepEqual(arr.toDictionary(k => k, v => true), { 1: true, 2: true, 3: true, 4: true, 5: true });
        assert.deepEqual(arr.toDictionary(k => k, v => v * v), { 1: 1, 2: 4, 3: 9, 4: 16, 5: 25 });
        assert.deepEqual(arr.toDictionary(k=>k), { 1: 1, 2: 2, 3: 3, 4: 4, 5: 5 });
    });
});