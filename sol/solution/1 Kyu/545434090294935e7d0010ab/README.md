# [**Functional SQL**](https://www.codewars.com/kata/545434090294935e7d0010ab)

## **Description:**
In this Kata we are going to mimic the `SQL` syntax.
> Note: for javascript, coffeescript and typescript, the description shows javascript examples.

To do this, you must implement the `query()` function. This function returns an object with the following methods:

```js
{
  select: ...,
  from: ...,
  where: ...,
  orderBy: ...,
  groupBy: ...,
  having: ...,
  execute: ...
}
```
The methods are chainable and the query is executed by calling the `execute` method.

⚠️ **Note:** The order of appearance of a clause in a query doesn't matter. However, when it comes time for you to run the query, you MUST execute the clauses in this logical order: `from` first, then `where`, then `groupBy`, then `having`, then `select` and finally `orderBy`.

```js
// SELECT * FROM numbers
var numbers = [1, 2, 3];
query().select().from(numbers).execute(); // [1, 2, 3]

// clauses order does not matter
query().from(numbers).select().execute(); // [1, 2, 3]
```

Of course, you can make queries over object collections:
```js
var persons = [
  {name: 'Peter', profession: 'teacher', age: 20, maritalStatus: 'married'},
  {name: 'Michael', profession: 'teacher', age: 50, maritalStatus: 'single'},
  {name: 'Peter', profession: 'teacher', age: 20, maritalStatus: 'married'},
  {name: 'Anna', profession: 'scientific', age: 20, maritalStatus: 'married'},
  {name: 'Rose', profession: 'scientific', age: 50, maritalStatus: 'married'},
  {name: 'Anna', profession: 'scientific', age: 20, maritalStatus: 'single'},
  {name: 'Anna', profession: 'politician', age: 50, maritalStatus: 'married'}
];

// SELECT * FROM persons
query().select().from(persons).execute();
// [{name: 'Peter',...}, {name: 'Michael', ...}]
```

You can select some fields:
```js
function profession(person) {
  return person.profession;
}

// SELECT profession FROM persons
query().select(profession).from(persons).execute(); // select receives a function that will be called with the values of the array
// ["teacher", "teacher", "teacher", "scientific", "scientific", "scientific", "politician"]
```

If you repeat a SQL clause (except `where()` or `having()`), an exception will be thrown:
```js
query().select().select().execute(); // Error('Duplicate SELECT');
query().select().from([]).select().execute(); // Error('Duplicate SELECT');
query().select().from([]).from([]).execute(); // Error('Duplicate FROM');
query().select().from([]).where().where() // This is an AND filter (see below)
```

You can omit any `SQL` clause:
```js
var numbers = [1, 2, 3];

query().select().execute(); // []
query().from(numbers).execute(); // [1, 2, 3]
query().execute(); // []
```

You can apply filters:
```js
function isTeacher(person) {
  return person.profession === 'teacher';
}

// SELECT profession FROM persons WHERE profession="teacher"
query().select(profession).from(persons).where(isTeacher).execute();
// ["teacher", "teacher", "teacher"]

//SELECT * FROM persons WHERE profession="teacher"
query().select().from(persons).where(isTeacher).execute();
// [{person: 'Peter', profession: 'teacher', ...}, ...]

function name(person) {
  return person.name;
}

// SELECT name FROM persons WHERE profession="teacher" 
query().select(name).from(persons).where(isTeacher).execute();
// ["Peter", "Michael", "Peter"]
```

Aggregations are also possible:
```js
// SELECT * FROM persons GROUP BY profession <- Bad in SQL but possible in this kata
query().select().from(persons).groupBy(profession).execute(); 
// [
//   ["teacher",
//      [
//        {
//         name: "Peter",
//         profession: "teacher"
//         ...
//       },
//       {
//         name: "Michael",
//         profession: "teacher"
//         ...
//       }
//     ]
//   ],
//   ["scientific",
//     [
//        {
//           name: "Anna",
//           profession: "scientific"
//         },
//      ...
//    ]
//   ]
//   ...
// ]
```

You can mix `where()` with `groupBy()`:
```js
// SELECT * FROM persons WHERE profession='teacher' GROUP BY profession
query().select().from(persons).where(isTeacher).groupBy(profession).execute();
```

Or with `select()`:
```js
function professionGroup(group) {
  return group[0];
}

// SELECT profession FROM persons GROUP BY profession
query().select(professionGroup).from(persons).groupBy(profession).execute();
// ["teacher","scientific","politician"]
```

Another example:
```js
function isEven(number) {
  return number % 2 === 0;
}

function parity(number) {
  return isEven(number) ? 'even' : 'odd';
}

var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]; 

// SELECT * FROM numbers
query().select().from(numbers).execute();
// [1, 2, 3, 4, 5, 6, 7, 8, 9]

// SELECT * FROM numbers GROUP BY parity
query().select().from(numbers).groupBy(parity).execute();
// [["odd", [1, 3, 5, 7, 9]], ["even", [2, 4, 6, 8]]]
```

Multilevel grouping:
```js
function isPrime(number) {
  if (number < 2) {
    return false;
  }
  var divisor = 2;
  for(; number % divisor !== 0; divisor++);
  return divisor === number;
}

function prime(number) {
  return isPrime(number) ? 'prime' : 'divisible';
}

// SELECT * FROM numbers GROUP BY parity, isPrime
query().select().from(numbers).groupBy(parity, prime).execute();
// [["odd", [["divisible", [1, 9]], ["prime", [3, 5, 7]]]], ["even", [["prime", [2]], ["divisible", [4, 6, 8]]]]]
```

`orderBy` should be called after `groupBy`, so the values passed to `orderBy` function are the grouped results by the `groupBy` function.<br>
Filter groups with `having()`:
```js
function odd(group) {
  return group[0] === 'odd';
}

// SELECT * FROM numbers GROUP BY parity HAVING odd(number) = true <- I know, this is not a valid SQL statement, but you can understand what I am doing
query().select().from(numbers).groupBy(parity).having(odd).execute();
// [["odd", [1, 3, 5, 7, 9]]]
```

You can order the results:
```js
var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];

function descendentCompare(number1, number2) {
  return number2 - number1;
}

// SELECT * FROM numbers ORDER BY value DESC 
query().select().from(numbers).orderBy(descendentCompare).execute();
//[9, 8, 7, 6, 5, 4, 3, 2, 1]
```

`from()` supports multiple collections:
```js
var teachers = [
  {
    teacherId: '1',
    teacherName: 'Peter'
  },
  {
    teacherId: '2',
    teacherName: 'Anna'
  }
];


var students = [
  {
    studentName: 'Michael',
    tutor: '1'
  },
  {
    studentName: 'Rose',
    tutor: '2'
  }
];

function teacherJoin(join) {
  return join[0].teacherId === join[1].tutor;
}

function student(join) {
  return {studentName: join[1].studentName, teacherName: join[0].teacherName};
}

// SELECT studentName, teacherName FROM teachers, students WHERE teachers.teacherId = students.tutor
query().select(student).from(teachers, students).where(teacherJoin).execute();
// [{"studentName": "Michael", "teacherName": "Peter"}, {"studentName": "Rose", "teacherName": "Anna"}]
```

Finally, `where()` and `having()` admit multiple `AND` and `OR` filters:
```js
function tutor1(join) {
  return join[1].tutor === "1";
}

// SELECT studentName, teacherName FROM teachers, students WHERE teachers.teacherId = students.tutor AND tutor = 1
query().select(student).from(teachers, students).where(teacherJoin).where(tutor1).execute();
// [{"studentName": "Michael", "teacherName": "Peter"}] <- AND filter

var numbers = [1, 2, 3, 4, 5, 7];

function lessThan3(number) {
  return number < 3;
}

function greaterThan4(number) {
  return number > 4;
}

// SELECT * FROM number WHERE number < 3 OR number > 4
query().select().from(numbers).where(lessThan3, greaterThan4).execute();
// [1, 2, 5, 7] <- OR filter

var numbers = [1, 2, 1, 3, 5, 6, 1, 2, 5, 6];

function greatThan1(group) {
  return group[1].length > 1;
}

function isPair(group) {
  return group[0] % 2 === 0;
}

function id(value) {
  return value;
}

function frequency(group) {
  return { value: group[0], frequency: group[1].length };      
}

// SELECT number, count(number) FROM numbers GROUP BY number HAVING count(number) > 1 AND isPair(number)
query().select(frequency).from(numbers).groupBy(id).having(greatThan1).having(isPair).execute();
// [{"value": 2, "frequency": 2}, {"value": 6, "frequency": 2}])
```

## **Requirements Recap**

### SQL-like Query Builder Clause Rules

| Clause     | ⚠️ Must be executed... | Arg(s) Count | Arg Type          | Repeatable? | Notes                                                                 |
|------------|--------------------|--------------|-------------------|-------------|-----------------------------------------------------------------------|
| **`from`**   | First              | 1 or more    | Table(s) = arrays | No          | Multiple tables trigger a cartesian product                           |
| **`where`**  | Second             | 1 or more    | Functions         | Yes (each repetition is a logical **`AND`**)         | Each call = logical **AND**; functions inside = logical **`OR`**        |
| **`groupBy`**| Third              | 1 or more    | Functions         | No          | Groups hierarchically (1st fn groups, then subgrouped by next, etc.)  |
| **`having`** | Fourth             | 1 or more    | Functions         | Yes (each repetition is a logical **`AND`**)         | Each call = logical **`AND`**; functions inside = logical **`OR`**        |
| **`select`** | Fifth              | 0 or 1       | Function          | No          | If omitted = selects everything; one fn = custom projection           |
| **`orderBy`**| Last               | 1            | Function          | No          | Sorts final results                                                   |
| **`execute`**| —                  | None (just executes the entire query)           | —                 | —           | Runs query and returns results                                        |

If any of the unrepeatable clauses are repeated in the query, your solution **MUST** raise an `Error` object with the **error message** `"duplicate"` **followed by the name of the duplicated clause**. If the clause is multi-word, merge it into one (ex: `groupby`).
- For example, if the `groupBy` clause is duplicated, you should throw an Error with the exact string message "`duplicate groupby`" (capitalization doesn't matter).

## **Solutions:**

#### **JavaScript**
```js
function query() {
  const state = {
    from: null,
    select: null,
    where: [],
    groupBy: null,
    having: [],
    orderBy: null,
    errors: [],
    flags: {
      select: false,
      from: false,
      groupBy: false,
      orderBy: false
    }
  };
  function cartesianProduct(arrays) {
    return arrays.reduce((a, b) => a.flatMap(d => b.map(e => [...d, e])), [[]]);
  }
  function applyWhere(data) {
    if (!state.where.length) return data;
    return state.where.reduce((acc, conditions) => {
      return acc.filter(item => conditions.some(fn => fn(item)));
    }, data);
  }
  function groupData(data, fns) {
    if (!fns || !fns.length) return data;
    const groupFn = fns[0];
    const groups = new Map();
    for (const item of data) {
      const key = groupFn(item);
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(item);
    }
    const result = [];
    for (const [key, values] of groups) {
      result.push([key, groupData(values, fns.slice(1))]);
    }
    return result;
  }
  function applyHaving(groups) {
    if (!state.having.length) return groups;
    return state.having.reduce((acc, conditions) => {
      return acc.filter(group => conditions.some(fn => fn(group)));
    }, groups);
  }
  function applySelect(data) {
    if (!state.select) return data;
    return data.map(state.select);
  }
  function applyOrderBy(data) {
    if (!state.orderBy) return data;
    return data.slice().sort(state.orderBy);
  }
  function markDuplicate(clause) {
    state.errors.push(`Duplicate ${clause}`);
  }
  return {
    select(fn) {
      if (state.flags.select) {
        markDuplicate('select');
      } else {
        state.flags.select = true;
        state.select = fn || null;
      }
      return this;
    },
    from(...tables) {
      if (state.flags.from) {
        markDuplicate('from');
      } else {
        state.flags.from = true;
        state.from = tables;
      }
      return this;
    },
    where(...conditions) {
      state.where.push(conditions);
      return this;
    },
    groupBy(...fns) {
      if (state.flags.groupBy) {
        markDuplicate('groupby');
      } else {
        state.flags.groupBy = true;
        state.groupBy = fns;
      }
      return this;
    },
    having(...conditions) {
      state.having.push(conditions);
      return this;
    },
    orderBy(fn) {
      if (state.flags.orderBy) {
        markDuplicate('orderby');
      } else {
        state.flags.orderBy = true;
        state.orderBy = fn;
      }
      return this;
    },
    execute() {
      if (state.errors.length) throw new Error(state.errors[0]);
      let data = [];
      if (state.from) {
        data = state.from.length === 1 ? state.from[0] : cartesianProduct(state.from);
      }
      data = applyWhere(data);
      if (state.groupBy) {
        data = groupData(data, state.groupBy);
        data = applyHaving(data);
      }
      data = applySelect(data);
      data = applyOrderBy(data);
      return data;
    }
  };
}
```

#### **Python**
```py
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
```