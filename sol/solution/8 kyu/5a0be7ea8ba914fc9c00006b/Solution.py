#
# Solution
#
def sakura_fall(v):
    if v <= 0:
        return 0.0
    return 400.0 / v





#
# Sample Tests
#
import codewars_test as test
from solution import sakura_fall

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_approx_equals(sakura_fall(5), 80)
        test.assert_approx_equals(sakura_fall(10), 40)
        test.assert_approx_equals(sakura_fall(-1), 0)