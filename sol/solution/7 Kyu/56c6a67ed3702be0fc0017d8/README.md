# [**I need a lookup quick!**](https://www.codewars.com/kata/56c6a67ed3702be0fc0017d8)

## **Description:**
Write
```js
Array.prototype.toDictionary = function(keyFn, valueFn) {}
```
that will take in a key selector function keyFn and an optional value selector function valueFn and return a hash.

**For Example:**
```js
var arr = [1,2,3,4,5];
arr.toDictionary(k=>k, v=> true) === {1:true, 2:true, 3:true, 4:true, 5:true};
arr.toDictionary(k=>k, v=> v*v) === {1:1, 2:4, 3:9, 4:16, 5:25};
arr.toDictionary(k=>k) === {1:1, 2:2, 3:3, 4:4, 5:5}; // if no valueFn supplied, use the current item
```

## **Solutions:**

#### **JavaScript**
```js
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
```