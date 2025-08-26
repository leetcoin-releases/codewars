#
# Solution
#
def binary_to_string(binary: str) -> str:
    parts = binary.split("0b")[1:]
    return "".join(chr(int(bits, 2)) for bits in parts)





#
# Sample Tests
#
import codewars_test as test
from solution import binary_to_string

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(binary_to_string('0b10000110b11000010b1110100'), 'Cat')
        test.assert_equals(binary_to_string('0b10010000b11001010b11011000b11011000b11011110b1000000b10101110b11011110b11100100b11011000b11001000b100001'
        ), 'Hello World!')
        test.assert_equals(binary_to_string('0b10100110b11001010b11000110b11100100b11001010b11101000b1000000b11011010b11001010b11100110b11100110b11000010b11001110b11001010b1000000b110001'
        ), 'Secret message 1')