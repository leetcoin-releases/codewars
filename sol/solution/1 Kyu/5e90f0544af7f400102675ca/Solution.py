#
# Solution
#
def minimum_transportation_price(suppliers, consumers, costs):
    # Fast specialized solver for the balanced/unbalanced transportation problem.
    supply = suppliers[:]
    demand = consumers[:]
    n = len(supply)
    m = len(demand)
    total_supply = sum(supply)
    total_demand = sum(demand)
    if total_supply == 0 or total_demand == 0:
        return 0
    remaining = min(total_supply, total_demand)
    # Track active rows/cols
    active_rows = [i for i, s in enumerate(supply) if s > 0]
    active_cols = [j for j, d in enumerate(demand) if d > 0]
    # For each column store current minimal cost row achieving the (updated) column minimum.
    best_row = [-1] * m
    col_min = [0] * m  # acts like consumer potentials
    cost_total = 0
    while remaining and active_rows and active_cols:
        # Recompute column minima only for active columns.
        for j in active_cols:
            br = -1
            mc = None
            for i in active_rows:
                c = costs[i][j]
                if mc is None or c < mc:
                    mc = c
                    br = i
            best_row[j] = br
            col_min[j] = mc
        # Pick column whose minimum is globally minimal.
        # (All reduced costs >=0; choosing any zero reduced-cost edge is safe.)
        j_pick = min(active_cols, key=lambda j: col_min[j])
        i_pick = best_row[j_pick]
        if i_pick == -1:
            # No feasible edge (should not happen with positive remaining), break safeguard.
            break
        f = supply[i_pick] if supply[i_pick] < demand[j_pick] else demand[j_pick]
        if f > remaining:
            f = remaining
        cost_total += f * costs[i_pick][j_pick]
        supply[i_pick] -= f
        demand[j_pick] -= f
        remaining -= f
        if supply[i_pick] == 0:
            active_rows.remove(i_pick)
        if demand[j_pick] == 0:
            active_cols.remove(j_pick)
    return cost_total





#
# Sample Tests
#
import codewars_test as test
from solution import minimum_transportation_price

@test.describe("5 Fixed tests")
def fixed_tests():
    @test.it("5 Sample tests")
    def sample_tests():
        suppliers = [10, 7, 13]
        consumers = [6, 20, 4]
        costs = [
            [4, 12, 3],
            [20, 1, 6],
            [7, 0, 5]
        ]
        test.assert_equals(minimum_transportation_price(suppliers, consumers, costs), 43)

        suppliers = [8, 15, 21]
        consumers = [8, 36]
        costs = [
            [9, 16],
            [7, 13],
            [25, 1]
        ]
        test.assert_equals(minimum_transportation_price(suppliers, consumers, costs), 288)

        suppliers = [31, 16]
        consumers = [14, 17, 16]
        costs = [
            [41, 18, 0],
            [4, 16, 37]
        ]
        test.assert_equals(minimum_transportation_price(suppliers, consumers, costs), 358)

        suppliers = [10, 20, 20]
        consumers = [5, 25, 10, 10]
        costs = [
            [2, 5, 3, 0],
            [3, 4, 1, 4],
            [2, 6, 5, 2]
        ]
        test.assert_equals(minimum_transportation_price(suppliers, consumers, costs), 150)

        suppliers = [13, 44, 27, 39, 17]
        consumers = [28, 12, 30, 17, 19, 34]
        costs = [
            [6, 6, 12, 8, 13, 13],
            [7, 20, 5, 16, 11, 16],
            [4, 6, 19, 0, 2, 18],
            [1, 16, 6, 11, 8, 11],
            [5, 6, 11, 1, 6, 14]
        ]
        test.assert_equals(minimum_transportation_price(suppliers, consumers, costs), 759)