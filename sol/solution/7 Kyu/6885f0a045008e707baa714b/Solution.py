#
# Solution
#
def read(tape, head, moves):
    result = ""
    for move in moves:
        result += tape[head]
        if move == ">":
            head += 1
        elif move == "<":
            head -= 1
    return result





#
# Sample Tests
#
import codewars_test as test
from solution import read

@test.describe('Fixed tests')
def fixed_tests():
    @test.it('should match the example')
    def _():
        test.assert_equals(read('011010', 3, '>><<'), '0101')
    
    @test.it('should not read any bits if there are no moves')
    def _():
        test.assert_equals(read('011010', 2, ''), '')
    
    @test.it('should read the tape as-is if head = 0, and moves are only >')
    def _():
        test.assert_equals(read('011010', 0, '>>>>>'), '01101')
    
    @test.it('should read the tape in reverse if head at the end, and moves are only <')
    def _():
        test.assert_equals(read('011010', 5, '<<<<<'), '01011')