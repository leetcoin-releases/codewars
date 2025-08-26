# [**Turing Machine: Movement**](https://www.codewars.com/kata/6885f0a045008e707baa714b)

## **Description**
In 1936, **Alan Turing** introduced the concept of a "universal machine": a theoretical device that could simulate any computation with a simple set of instructions and infinite tape. One of the simplest possible forms of computer.

[Computerphile Video](https://www.youtube.com/watch?v=DILF8usqp7M) | [Wikipedia](https://en.wikipedia.org/wiki/Turing_machine)

At each step, a Turing Machine needs to decide three things:
- what bit (`0` or `1`) to leave at the current position*
- **where next to move on the tape**
- which state to enter next*
- It does this based on the current state*, and the **bit at the current position**.

* = we don't worry about these in this kata

## **Your task**
In this kata, you will simulate movement of a Turing Machine in isolation.

You will be given:
- `tape`: a string of `1`s and `0`s
- `head`: the starting position on the tape
- `moves`: a string of left (`<`) and right (`>`) movements

Your function should simulate moving the `head` according to `moves`, and should return a string of `1`s and `0`s at the position of the head at the beginning of each step.

## **Example**

Given inputs:
- `tape`: `011010`
- `head`: `3`
- `moves`: `>><<`
The output should be: `0101`.

Let's look at it step by step:
1. We start at the `0`, the 3nd (0-indexed) bit (`0` or `1`) from the left, which we read, and move `>`.
2. We read the `1`, and move `>` again.
3. We read another `0` and move `<`.
4. We read another `1`, and move `<` again.
We're out of moves, and can return our output: the bits we read along the way (the last 4 bits in this case).

```md
     : start  | step 1 | step 2 | step 3 | end     : read path
tape : 011010 | 011010 | 011010 | 011010 | 011010  :    1    >
head :    ^   |     ^  |      ^ |     ^  |    ^    :     0   >
move :    >   |     >  |      < |     <  |         :      1  <
read : 0      | 01     | 010    | 0101   | 0101    :     0   <
```
See more examples in the tests.

## **Constraints**
You will never be given moves that take you outside the tape, so don't worry about that.

The tape will have at most 100 bits, and you will be given at most 20 moves to simulate.

## **Ready for the next step?**
This kata is part 1 of ? of [the series](https://www.codewars.com/collections/6893029636adaa8d39552930).<br>
The [next kata](https://www.codewars.com/kata/6885f65cb86c03bd3cd25353) in the series will have you fully simulate a Turing Machine.

### **Credits**
[towc](https://www.codewars.com/users/towc): came up with the idea and fixed tests<br>
[hobovsky](https://www.codewars.com/users/hobovsky) - minor curation

## **Solutions:**

#### **JavaScript**
```js
function read(tape, head, moves) {
    let result = "";
    for (let move of moves) {
        result += tape[head];
        if (move === '>') head++;
        else if (move === '<') head--;
    }
    return result;
}
```

#### **Python**
```py
def read(tape, head, moves):
    result = ""
    for move in moves:
        result += tape[head]
        if move == ">":
            head += 1
        elif move == "<":
            head -= 1
    return result
```