#
# Solution
#
knock(knock)()()





#
# Test Driven Development (TDD)
#
import codewars_test as test
# TODO Write tests
import solution # or from solution import example

# test.assert_equals(actual, expected, [optional] message)
@test.describe("Example")
def test_group():
    @test.it("test case")
    def test_case():
        test.assert_equals(1 + 1, 2)
