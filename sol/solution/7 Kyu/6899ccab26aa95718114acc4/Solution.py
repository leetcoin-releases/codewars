#
# Solution
#
def can_draw(shape: dict[str, list[str]]) -> bool:
    odd_vertices = sum(len(neighbors) % 2 for neighbors in shape.values())
    return odd_vertices == 0 or odd_vertices == 2





#
# Sample Tests
#
import codewars_test as test
from solution import can_draw

from preloaded import shapes
import pprint

def do_test(shape, expected, pretty_shape=None):
    actual = can_draw(shape)
    if pretty_shape is None:
        test.assert_equals(actual, expected, f'can_draw({pprint.pformat(shape, sort_dicts=False)})')
    else:
        test.assert_equals(actual, expected, f"You think so? Try to draw this:\n\n{pretty_shape}")

@test.describe("Sample Tests")
def sample_tests():
    @test.it("Examples from the description")
    def description_examples():
        shape1 = {
            "A": ["B", "C"],
            "B": ["A", "C", "D", "F"],
            "C": ["A", "B", "E", "F"],
            "D": ["B", "E", "F"],
            "E": ["C", "D", "F"],
            "F": ["B", "C", "D", "E"]
        }
        
        do_test(shape1, True, shapes[0])
        
        shape2 = {
            "A": ["B", "C", "E"],
            "B": ["A", "D", "E"],
            "C": ["A", "D", "E"],
            "D": ["B", "C", "E"],
            "E": ["A", "B", "C", "D"]
        }
        
        do_test(shape2, False, shapes[1])
        
    @test.it("A few other examples")
    def other_examples():
        shape3 = {
            "A": ["B", "C"],
            "B": ["A", "D"],
            "C": ["A", "D"],
            "D": ["B", "C"]
        }
        
        do_test(shape3, True, shapes[2])
        
        shape4 = {
            "A": ["C"],
            "B": ["C"],
            "C": ["A", "B", "D", "E"],
            "D": ["C"],
            "E": ["C"]
        }
        
        do_test(shape4, False, shapes[3])
        
        shape5 = {
            "A": ["B", "D"],
            "B": ["A", "C", "E"],
            "C": ["B", "F"],
            "D": ["A", "E", "G"],
            "E": ["B", "D", "F", "H"],
            "F": ["C", "E", "I"],
            "G": ["D", "H"],
            "H": ["E", "G", "I"],
            "I": ["F", "H"]
        }
        
        do_test(shape5, False, shapes[4])
        
        shape6 = {
            "A": ["B", "D"],
            "B": ["A", "C", "E"],
            "C": ["B", "F"],
            "D": ["A", "E"],
            "E": ["B", "D", "F"],
            "F": ["C", "E"]
        }
        
        do_test(shape6, True, shapes[5])