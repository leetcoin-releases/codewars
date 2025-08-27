#
# Solution
#
from preloaded import DuplicateFromError, DuplicateSelectError, DuplicateGroupByError, DuplicateOrderByError
from itertools import product
from functools import cmp_to_key
def query():
    return Query()
class Query:
    def __init__(self):
        self._from_tables = None
        self._select_func = None
        self._where_conditions = []
        self._group_by_funcs = None
        self._having_conditions = []
        self._order_by_func = None
        self._from_called = False
        self._select_called = False
        self._group_by_called = False
        self._order_by_called = False
    def select(self, func=None):
        if self._select_called:
            raise DuplicateSelectError()
        self._select_called = True
        self._select_func = func
        return self
    def from_(self, *tables):
        if self._from_called:
            raise DuplicateFromError()
        self._from_called = True
        self._from_tables = tables
        return self
    def where(self, *conditions):
        if conditions:
            self._where_conditions.append(conditions)
        return self
    def group_by(self, *funcs):
        if self._group_by_called:
            raise DuplicateGroupByError()
        self._group_by_called = True
        self._group_by_funcs = funcs
        return self
    def having(self, *conditions):
        if conditions:
            self._having_conditions.append(conditions)
        return self
    def order_by(self, func):
        if self._order_by_called:
            raise DuplicateOrderByError()
        self._order_by_called = True
        self._order_by_func = func
        return self
    def execute(self):
        if not self._from_tables:
            data = []
        elif len(self._from_tables) == 1:
            data = list(self._from_tables[0])
        else:
            data = list(product(*self._from_tables))
            data = [list(row) for row in data]
        if self._where_conditions:
            for condition_group in self._where_conditions:
                data = [item for item in data if any(cond(item) for cond in condition_group)]
        if self._group_by_funcs:
            data = self._group_data(data, self._group_by_funcs)
        if self._having_conditions and self._group_by_funcs:
            for condition_group in self._having_conditions:
                data = [item for item in data if any(cond(item) for cond in condition_group)]
        if self._select_func:
            data = [self._select_func(item) for item in data]
        if self._order_by_func:
            data.sort(key=cmp_to_key(self._order_by_func))
        return data
    def _group_data(self, data, group_funcs):
        if not group_funcs:
            return data
        groups = {}
        for item in data:
            key = group_funcs[0](item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        if len(group_funcs) > 1:
            result = []
            for key, group_data in groups.items():
                sub_groups = self._group_data(group_data, group_funcs[1:])
                result.append([key, sub_groups])
        else:
            result = [[key, group_data] for key, group_data in groups.items()]
        return result





#
# Sample Tests
#
import codewars_test as test
from preloaded import DuplicateFromError, DuplicateSelectError, DuplicateGroupByError, DuplicateOrderByError
from solution import query
from functools import reduce


def run_tests(tests: list[tuple]) -> None:
    for q, expected, msg in tests:
        test.assert_equals(q.execute(), expected, msg)


def run_errored_tests(tests: list[tuple]) -> None:
    for func, exc in tests:
        test.expect_error(
            f"A \"{exc.__name__}\" exception should be thrown due to duplicate \"{exc().clause}\" clause",
            func,
            exc,
        )


@test.describe("Fixed tests")
def fixed_tests():
    @test.it("Basic SELECT Tests")
    def it_1():
        numbers = [1, 2, 3]

        run_tests([
            (
                query().select().from_(numbers[:]),
                numbers,
                "SELECT * FROM numbers",
            ),
            (
                query().select(),
                [],
                "An empty list should be produced if there is no FROM clause",
            ),
            (
                query().from_(numbers[:]),
                numbers,
                "SELECT can be omited",
            ),
            (
                query(),
                [],
                "An empty list should be produced for an empty query",
            ),
            (
                query().from_(numbers[:]).select(),
                numbers,
                "The order of the clauses does not matter",
            ),
        ])

    @test.it("Basic SELECT and WHERE Over Objects")
    def it_2():
        persons = [
            {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
            {"name": "Michael", "profession": "teacher", "age": 50, "marital_status": "single"},
            {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
            {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "married"},
            {"name": "Rose", "profession": "scientific", "age": 50, "marital_status": "married"},
            {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "single"},
            {"name": "Anna", "profession": "politician", "age": 50, "marital_status": "married"}
        ]

        def profession(person): return person["profession"]
        def is_teacher(person): return person["profession"] == "teacher"
        def name(person): return person["name"]

        run_tests([
            (
                query().select().from_(persons[:]),
                persons,
                "SELECT * FROM persons",
            ),
            (
                query().select(profession).from_(persons[:]),
                ["teacher", "teacher", "teacher", "scientific", "scientific", "scientific", "politician"],
                "SELECT profession FROM persons",
            ),
            (
                query().select(profession),
                [],
                "No FROM clause produces empty array",
            ),
            (
                query().select(profession).from_(persons[:]).where(is_teacher),
                ["teacher", "teacher", "teacher"],
                "SELECT profession FROM persons WHERE profession = \"teacher\"",
            ),
            (
                query().from_(persons[:]).where(is_teacher),
                persons[:3],
                "SELECT * FROM persons WHERE profession = \"teacher\"",
            ),
            (
                query().select(name).from_(persons[:]).where(is_teacher),
                ["Peter", "Michael", "Peter"],
                "SELECT name FROM persons WHERE profession = \"teacher\"",
            ),
            (
                query().where(is_teacher).from_(persons[:]).select(name),
                ["Peter", "Michael", "Peter"],
                "The order of the clauses does not matter",
            ),
        ])

    @test.it("GROUP BY Tests")
    def it_3():
        persons = [
            {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
            {"name": "Michael", "profession": "teacher", "age": 50, "marital_status": "single"},
            {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
            {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "married"},
            {"name": "Rose", "profession": "scientific", "age": 50, "marital_status": "married"},
            {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "single"},
            {"name": "Anna", "profession": "politician", "age": 50, "marital_status": "married"}
        ]

        def profession(person): return person["profession"]
        def is_teacher(person): return person["profession"] == "teacher"
        def name(person): return person["name"]
        def name(person): return person["name"]
        def age(person): return person["age"]
        def marital_status(person): return person["marital_status"]
        def profession_count(group): return [group[0], len(group[1])]
        def natural_compare(value1, value2): return -1 if (value1 < value2) else 1 if (value1 > value2) else 0

        run_tests([
            (
                query().select().from_(persons[:]).group_by(profession),
                [
                    ["teacher", [
                        {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
                        {"name": "Michael", "profession": "teacher", "age": 50, "marital_status": "single"},
                        {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"}
                    ]],
                    ["scientific", [
                        {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "married"},
                        {"name": "Rose", "profession": "scientific", "age": 50, "marital_status": "married"},
                        {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "single"}
                    ]],
                    ["politician", [
                        {"name": "Anna", "profession": "politician", "age": 50, "marital_status": "married"}
                    ]]
                ],
                "SELECT * FROM persons GROUP BY profession <- Bad in SQL but possible in Python",
            ),
            (
                query().select().from_(persons[:]).where(is_teacher).group_by(profession),
                [
                    ["teacher", [
                        {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
                        {"name": "Michael", "profession": "teacher", "age": 50, "marital_status": "single"},
                        {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"}
                    ]]
                ],
                "SELECT * FROM persons WHERE profession = \"teacher\" GROUPBY profession",
            ),
            (
                query().select().from_(persons[:]).group_by(profession, name),
                [
                    ["teacher", [
                        ["Peter", [
                            {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
                            {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"}
                        ]],
                        ["Michael", [
                            {"name": "Michael", "profession": "teacher", "age": 50, "marital_status": "single"}
                        ]]
                    ]],
                    ["scientific", [
                        ["Anna", [
                            {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "married"},
                            {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "single"}
                        ]],
                        ["Rose", [
                            {"name": "Rose", "profession": "scientific", "age": 50, "marital_status": "married"}
                        ]]
                    ]],
                    ["politician", [
                        ["Anna", [
                            {"name": "Anna", "profession": "politician", "age": 50, "marital_status": "married"}
                        ]]
                    ]]
                ],
                "SELECT * FROM persons WHERE profession = \"teacher\" GROUP BY profession, name",
            ),
            (
                query().select().from_(persons[:]).group_by(profession, name, age, marital_status),
                [
                    ["teacher", [
                        ["Peter", [
                            [20, [["married", [
                                {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"},
                                {"name": "Peter", "profession": "teacher", "age": 20, "marital_status": "married"}
                            ]]]]
                        ]],
                        ["Michael", [
                            [50, [["single", [
                                {"name": "Michael", "profession": "teacher", "age": 50, "marital_status": "single"}
                            ]]]]
                        ]]
                    ]],
                    ["scientific", [
                        ["Anna", [[20, [
                            ["married", [
                                {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "married"}
                            ]],
                            ["single", [
                                {"name": "Anna", "profession": "scientific", "age": 20, "marital_status": "single"}
                            ]]
                        ]]]],
                        ["Rose", [[50, [
                            ["married", [
                                {"name": "Rose", "profession": "scientific", "age": 50, "marital_status": "married"}
                            ]]
                        ]]]]
                    ]],
                    ["politician", [["Anna", [[50, [["married", [
                        {"name": "Anna", "profession": "politician", "age": 50, "marital_status": "married"}
                    ]]]]]]]]
                ],
                "SELECT * FROM persons WHERE profession = \"teacher\" GROUP BY profession, name, age",
            ),
            (
                query().select(profession_count).from_(persons[:]).group_by(profession).order_by(natural_compare),
                [["politician", 1], ["scientific", 3], ["teacher", 3]],
                "SELECT profession, count(profession) FROM persons GROUP BY profession ORDER BY profession",
            ),
        ])

    @test.it("Numbers Tests")
    def it_4():
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        def is_prime(number):
            if number < 2:
                return False

            divisor = 2

            while number % divisor != 0:
                divisor += 1

            return divisor == number

        def prime(number): return "prime" if is_prime(number) else "divisible"
        def is_even(number): return number % 2 == 0
        def parity(number): return "even" if is_even(number) else "odd"
        def descendent_compare(number1, number2): return number2 - number1
        def odd(group): return group[0] == "odd"
        def less_than_3(number): return number < 3
        def greater_than_4(number): return number > 4

        run_tests([
            (
                query().select().from_(numbers[:]),
                numbers,
                "SELECT * FROM numbers",
            ),
            (
                query().select().from_(numbers[:]).group_by(parity),
                [["odd", [1, 3, 5, 7, 9]], ["even", [2, 4, 6, 8]]],
                "SELECT * FROM numbers GROUP BY parity",
            ),
            (
                query().select().from_(numbers[:]).group_by(parity, prime),
                [
                    ["odd", [["divisible", [1, 9]], ["prime", [3, 5, 7]]]],
                    ["even", [["prime", [2]], ["divisible", [4, 6, 8]]]]
                ],
                "SELECT * FROM numbers GROUP BY parity, is_prime",
            ),
            (
                query().select().from_(numbers[:]).group_by(parity).having(odd),
                [["odd", [1, 3, 5, 7, 9]]],
                "SELECT * FROM numbers GROUP BY parity HAVING odd(number) = true <- Bad in SQL but possible in Python",
            ),
            (
                query().select().from_(numbers[:]).order_by(descendent_compare),
                [9, 8, 7, 6, 5, 4, 3, 2, 1],
                "SELECT * FROM numbers ORDER BY value DESC",
            ),
            (
                query().select().from_(numbers[:]).where(less_than_3, greater_than_4),
                [1, 2, 5, 6, 7, 8, 9],
                "SELECT * FROM number WHERE number < 3 OR number > 4",
            ),
        ])

    @test.it("Frequency Tests")
    def it_5():
        def sum_values(value): return [value[0], reduce(lambda result, person: result + person[1], value[1], 0)]
        def name_grouping(person): return person[0]
        def natural_compare(value1, value2): return -1 if value1 < value2 else 1 if value1 > value2 else 0
        def val(value): return value
        def frequency(group): return {"value": group[0], "frequency": len(group[1])}
        def greater_than_1(group): return len(group[1]) > 1
        def is_pair(group): return group[0] % 2 == 0

        persons = [
            ["Peter", 3],
            ["Anna", 4],
            ["Peter", 7],
            ["Michael", 10],
        ]

        numbers = [1, 2, 1, 3, 5, 6, 1, 2, 5, 6]

        run_tests([
            (
                query().select(sum_values).from_(persons[:]).order_by(natural_compare).group_by(name_grouping),
                [["Anna", 4], ["Michael", 10], ["Peter", 10]],
                "SELECT name, sum(value) FROM persons ORDER BY natural_compare GROUP BY name_grouping",
            ),
            (
                query().select(frequency).from_(numbers[:]).group_by(val),
                [
                    {"value": 1, "frequency": 3},
                    {"value": 2, "frequency": 2},
                    {"value": 3, "frequency": 1},
                    {"value": 5, "frequency": 2},
                    {"value": 6, "frequency": 2}
                ],
                "SELECT number, count(number) FROM numbers GROUP BY number",
            ),
            (
                query().select(frequency).from_(numbers[:]).group_by(val).having(greater_than_1).having(is_pair),
                [{"value": 2, "frequency": 2}, {"value": 6, "frequency": 2}],
                "SELECT number, count(number) FROM numbers GROUP BY number HAVING count(number) > 1 AND is_pair(number)",
            ),
        ])

    @test.it("Join Tests")
    def it_6():
        def teacher_join(join): return join[0]["teacher_id"] == join[1]["tutor"]
        def student(join): return {"student_name": join[1]["student_name"], "teacher_name": join[0]["teacher_name"]}
        def tutor1(join): return join[1]["tutor"] == "1"

        teachers = [
            {
                "teacher_id": "1",
                "teacher_name": "Peter"
            },
            {
                "teacher_id": "2",
                "teacher_name": "Anna"
            }
        ]

        students = [
            {
                "student_name": "Michael",
                "tutor": "1"
            },
            {
                "student_name": "Rose",
                "tutor": "2"
            }
        ]

        numbers1 = [1, 2]
        numbers2 = [4, 5]

        run_tests([
            (
                query().select(student).from_(teachers, students).where(teacher_join),
                [{"student_name": "Michael", "teacher_name": "Peter"}, {"student_name": "Rose", "teacher_name": "Anna"}],
                "SELECT student_name, teacher_name FROM teachers, students WHERE teachers.teacher_id = students.tutor",
            ),
            (
                query().select().from_(numbers1, numbers2),
                [[1, 4], [1, 5], [2, 4], [2, 5]],
                "SELECT * FROM numbers1, numbers2",
            ),
            (
                query().select(student).from_(teachers, students).where(teacher_join).where(tutor1),
                [{"student_name": "Michael", "teacher_name": "Peter"}],
                "SELECT student_name, teacher_name FROM teachers, students WHERE teachers.teacher_id = students.tutor AND tutor = 1",
            ),
            (
                query().where(teacher_join).select(student).where(tutor1).from_(teachers, students),
                [{"student_name": "Michael", "teacher_name": "Peter"}],
                "The order of the clauses does not matter"
            ),
        ])

    @test.it("Duplication Exception Tests")
    def it_7():
        def val(value): return value

        run_errored_tests([
            (lambda: query().select().select().execute(), DuplicateSelectError),
            (lambda: query().select().from_([]).select().execute(), DuplicateSelectError),
            (lambda: query().select().from_([]).from_([]).execute(), DuplicateFromError),
            (lambda: query().select().from_([]).order_by(val).order_by(val).execute(), DuplicateOrderByError),
            (lambda: query().select().group_by(val).from_([]).group_by(val).execute(), DuplicateGroupByError),
        ])
