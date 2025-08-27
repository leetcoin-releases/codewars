/*
Solution
*/
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





/*
Sample Tests
*/
const chai               = require('chai')
const { expect, assert } = chai
const { deepEqual }      = assert
chai.config.truncateThreshold = 0

describe("SQL Tests", function() {
  describe("Fixed Tests", function() {
    function runTests(tests) {
      tests.forEach(({ query, stringified, expected, msg, shouldThrow }) => it(stringified, () => deepEqual(query.execute(), expected, msg)))
    }

    function runErroredTests(tests) {
      tests.forEach(({ fn, stringified, clause }) => it(stringified, () => expect(fn).to.throw(Error, new RegExp(`^Duplicate ${clause}$`, 'i'), `An error should be thrown due to duplicate ${clause} clause`)))
    }

    describe("Basic SELECT Tests", function() {
      const numbers = [1, 2, 3]

      runTests([
        {
          query: query().select().from(structuredClone(numbers)),
          stringified: 'query().select().from(numbers).execute()',
          expected: numbers,
        },
        {
          query: query().select(),
          stringified: 'query().select().execute()',
          expected: [],
          msg: 'An empty array should be produced if there is no FROM clause'        
        },
        {
          query: query().from(structuredClone(numbers)),
          stringified: 'query().from(numbers).execute()',
          expected: numbers,
          msg: 'SELECT can be omited'
        },
        {
          query: query(),
          stringified: 'query().execute()',
          expected: [],
        },
        {
          query: query().from(structuredClone(numbers)).select(),
          stringified: 'query().from(numbers).select().execute()',
          expected: numbers,
          msg: 'The order of appearance of the clauses in the chain does not matter'        
        },
      ])
    })

    describe("Basic SELECT and WHERE Over Objects", function() {
      const persons = [
        {name: 'Peter', profession: 'teacher', age: 20, maritalStatus: 'married'},
        {name: 'Michael', profession: 'teacher', age: 50, maritalStatus: 'single'},
        {name: 'Peter', profession: 'teacher', age: 20, maritalStatus: 'married'},
        {name: 'Anna', profession: 'scientific', age: 20, maritalStatus: 'married'},
        {name: 'Rose', profession: 'scientific', age: 50, maritalStatus: 'married'},
        {name: 'Anna', profession: 'scientific', age: 20, maritalStatus: 'single'},
        {name: 'Anna', profession: 'politician', age: 50, maritalStatus: 'married'}
      ]

      function profession(person) { return person.profession }
      function isTeacher(person)  { return person.profession === 'teacher' }
      function name(person)       { return person.name }

      runTests([
        {
          query: query().select().from(structuredClone(persons)),
          stringified: 'query().select().from(persons).execute()',
          expected: persons,
        },
        {
          query: query().select(profession).from(structuredClone(persons)),
          stringified: 'query().select(profession).from(persons).execute()\n[i.e., SELECT profession FROM persons]',
          expected: ['teacher', 'teacher', 'teacher', 'scientific', 'scientific', 'scientific', 'politician']
        },
        {
          query: query().select(profession),
          stringified: 'query().select(profession).execute()',
          expected: [],
          msg: 'No FROM clause produces empty array'
        },
        {
          query: query().select(profession).from(structuredClone(persons)).where(isTeacher),
          stringified: 'query().select(profession).from(persons).where(isTeacher).execute()\n[i.e., SELECT profession FROM persons WHERE profession = "teacher"]',
          expected: ['teacher', 'teacher', 'teacher'],
        },
        {
          query: query().from(structuredClone(persons)).where(isTeacher),
          stringified: 'query().from(persons).where(isTeacher).execute()\n[i.e., SELECT * FROM persons WHERE profession = "teacher" ]',
          expected: persons.slice(0, 3)
        },
        {
          query: query().select(name).from(structuredClone(persons)).where(isTeacher),
          stringified: 'query().select(name).from(persons).where(isTeacher).execute()\n[i.e., SELECT name FROM persons WHERE profession = "teacher"]',
          expected: ['Peter', 'Michael', 'Peter'] 
        },
        {
          query: query().where(isTeacher).from(structuredClone(persons)).select(name),
          stringified: 'query().where(isTeacher).from(persons).select(name).execute()\n[i.e., SELECT name FROM persons WHERE profession = "teacher"]',
          expected: ['Peter', 'Michael', 'Peter'],
          msg: 'The order of appearance of the clauses in the chain does not matter'        
        }
      ]) 
    })

    describe('GROUP BY Tests', function() {
      const persons = [
        {name: 'Peter', profession: 'teacher', age: 20, maritalStatus: 'married'},
        {name: 'Michael', profession: 'teacher', age: 50, maritalStatus: 'single'},
        {name: 'Peter', profession: 'teacher', age: 20, maritalStatus: 'married'},
        {name: 'Anna', profession: 'scientific', age: 20, maritalStatus: 'married'},
        {name: 'Rose', profession: 'scientific', age: 50, maritalStatus: 'married'},
        {name: 'Anna', profession: 'scientific', age: 20, maritalStatus: 'single'},
        {name: 'Anna', profession: 'politician', age: 50, maritalStatus: 'married'}
      ]

      const numbers = [6, 1, 5]

      function profession(person)             { return person.profession }
      function isTeacher(person)              { return person.profession === 'teacher' }
      function professionGroup(group)         { return group[0] }
      function name(person)                   { return person.name }
      function age(person)                    { return person.age }
      function maritalStatus(person)          { return person.maritalStatus }
      function professionCount(group)         { return [group[0], group[1].length] }
      function naturalCompare(value1, value2) { return (value1 < value2) ? -1 : (value1 > value2) ? 1 : 0 }
      function number(number)                 { return number }

      runTests([
        {
          query: query().select().from(structuredClone(persons)).groupBy(profession),
          stringified: 'query().select().from(persons).groupBy(profession).execute()\n[i.e., SELECT * FROM persons GROUP BY profession <- Bad in SQL but possible in JavaScript]',
          expected: [ [ 'teacher', [ { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' }, { 'name': 'Michael', 'profession': 'teacher', 'age': 50, 'maritalStatus': 'single' }, { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' } ] ], [ 'scientific', [ { 'name': 'Anna', 'profession': 'scientific', 'age': 20, 'maritalStatus': 'married' }, { 'name': 'Rose', 'profession': 'scientific', 'age': 50, 'maritalStatus': 'married' }, { 'name': 'Anna', 'profession': 'scientific', 'age': 20, 'maritalStatus': 'single' } ] ], [ 'politician', [ { 'name': 'Anna', 'profession': 'politician', 'age': 50, 'maritalStatus': 'married' } ] ] ],
        },
        {
          query: query().select().from(structuredClone(persons)).where(isTeacher).groupBy(profession),
          stringified: 'query().select().from(persons).where(isTeacher).groupBy(profession).execute()\n[i.e., SELECT * FROM persons WHERE profession = "teacher" GROUP BY profession]',
          expected: [ [ 'teacher', [ { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' }, { 'name': 'Michael', 'profession': 'teacher', 'age': 50, 'maritalStatus': 'single' }, { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' } ] ] ],
        },
        {
          query: query().select().from(structuredClone(persons)).groupBy(profession, name),
          stringified: 'query().select().from(persons).groupBy(profession, name).execute()\n[i.e., SELECT * FROM persons GROUP BY profession, name]',
          expected: [ [ 'teacher', [ [ 'Peter', [ { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' }, { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' } ] ], [ 'Michael', [ { 'name': 'Michael', 'profession': 'teacher', 'age': 50, 'maritalStatus': 'single' } ] ] ] ], [ 'scientific', [ [ 'Anna', [ { 'name': 'Anna', 'profession': 'scientific', 'age': 20, 'maritalStatus': 'married' }, { 'name': 'Anna', 'profession': 'scientific', 'age': 20, 'maritalStatus': 'single' } ] ], [ 'Rose', [ { 'name': 'Rose', 'profession': 'scientific', 'age': 50, 'maritalStatus': 'married' } ] ] ] ], [ 'politician', [ [ 'Anna', [ { 'name': 'Anna', 'profession': 'politician', 'age': 50, 'maritalStatus': 'married' } ] ] ] ] ],
        },
        {
          query: query().select().from(structuredClone(persons)).groupBy(profession, name, age, maritalStatus),
          stringified: 'query().select().from(persons).groupBy(profession, name, age, maritalStatus).execute()\n[i.e., SELECT * FROM persons GROUP BY profession, name, age, maritalStatus]',
          expected: [ [ 'teacher', [ [ 'Peter', [ [ 20, [ [ 'married', [ { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' }, { 'name': 'Peter', 'profession': 'teacher', 'age': 20, 'maritalStatus': 'married' } ] ] ] ] ] ], [ 'Michael', [ [ 50, [ [ 'single', [ { 'name': 'Michael', 'profession': 'teacher', 'age': 50, 'maritalStatus': 'single' } ] ] ] ] ] ] ] ], [ 'scientific', [ [ 'Anna', [ [ 20, [ [ 'married', [ { 'name': 'Anna', 'profession': 'scientific', 'age': 20, 'maritalStatus': 'married' } ] ], [ 'single', [ { 'name': 'Anna', 'profession': 'scientific', 'age': 20, 'maritalStatus': 'single' } ] ] ] ] ] ], [ 'Rose', [ [ 50, [ [ 'married', [ { 'name': 'Rose', 'profession': 'scientific', 'age': 50, 'maritalStatus': 'married' } ] ] ] ] ] ] ] ], [ 'politician', [ [ 'Anna', [ [ 50, [ [ 'married', [ { 'name': 'Anna', 'profession': 'politician', 'age': 50, 'maritalStatus': 'married' } ] ] ] ] ] ] ] ] ],
        },
        {
          query: query().select(professionCount).from(structuredClone(persons)).groupBy(profession).orderBy(naturalCompare),
          stringified: 'query().select(professionCount).from(persons).groupBy(profession).orderBy(naturalCompare).execute()\n[i.e., SELECT profession, count(profession) FROM persons GROUP BY profession ORDER BY profession]',
          expected: [ [ 'politician', 1 ], [ 'scientific', 3 ], [ 'teacher', 3 ] ],
        },
        {
          query: query().from(structuredClone(numbers)).groupBy(number),
          stringified: `query().from(numbers).groupBy(number).execute()\n[i.e., SELECT * FROM numbers GROUP BY number]\n[If this errors, the data structure you're using to store groups (if any) fails to preserve insertion order, and is instead ordering by number value or randomly]`,
          expected: [ [ 6, [ 6 ] ], [ 1, [ 1 ] ], [ 5, [ 5 ] ] ],
        },
      ])
    })

    describe('Numbers Tests', function() {
      function isPrime(number) {
        if (number < 2) return false
        let divisor = 2
        for(; number % divisor !== 0; divisor++);
        return divisor === number
      }

      function prime(number)                       { return isPrime(number) ? 'prime' : 'divisible' }
      function isEven(number)                      { return number % 2 === 0 }
      function parity(number)                      { return isEven(number) ? 'even' : 'odd' }
      function descendentCompare(number1, number2) { return number2 - number1 }   
      function odd(group)                          { return group[0] === 'odd' }
      function lessThan3(number)                   { return number < 3 }
      function greaterThan4(number)                { return number > 4 }

      const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

      runTests([
        {
          query: query().select().from(structuredClone(numbers)),
          stringified: 'query().select().from(numbers).execute()\n[i.e., SELECT * FROM numbers]',
          expected: numbers,
        },
        {
          query: query().select().from(structuredClone(numbers)).groupBy(parity),
          stringified: 'query().select().from(numbers).groupBy(parity).execute()\n[i.e., SELECT * FROM numbers GROUP BY parity]',
          expected: [ [ 'odd', [ 1, 3, 5, 7, 9 ] ], [ 'even', [ 2, 4, 6, 8 ] ] ],
        },
        {
          query: query().select().from(structuredClone(numbers)).groupBy(parity, prime),
          stringified: 'query().select().from(numbers).groupBy(parity, prime).execute()\n[i.e., SELECT * FROM numbers GROUP BY parity, isPrime]',
          expected: [ [ 'odd', [ [ 'divisible', [ 1, 9 ] ], [ 'prime', [ 3, 5, 7 ] ] ] ], [ 'even', [ [ 'prime', [ 2 ] ], [ 'divisible', [ 4, 6, 8 ] ] ] ] ],
        },
        {
          query: query().select().from(structuredClone(numbers)).groupBy(parity).having(odd),
          stringified: 'query().select().from(numbers).groupBy(parity).having(odd).execute()\n[i.e., SELECT * FROM numbers GROUP BY parity HAVING odd(number) = true  <- Bad in SQL but possible in JavaScript]',
          expected: [ [ 'odd', [ 1, 3, 5, 7, 9 ] ] ],
        },
        {
          query: query().select().from(structuredClone(numbers)).orderBy(descendentCompare),
          stringified: 'query().select().from(numbers).orderBy(descendentCompare).execute()\n[i.e., SELECT * FROM numbers ORDER BY value DESC]',
          expected: [ 9, 8, 7, 6, 5, 4, 3, 2, 1 ],
        },
        {
          query: query().select().from(structuredClone(numbers)).where(lessThan3, greaterThan4),
          stringified: 'query().select().from(numbers).where(lessThan3, greaterThan4).execute()\n[i.e., SELECT * FROM number WHERE number < 3 OR number > 4]',
          expected: [ 1, 2, 5, 6, 7, 8, 9 ],
        },
      ])
    })

    describe('Frequency Tests', function() {
      function sumValues(value) {
        return [value[0], value[1].reduce(function(result, person) {
          return result + person[1]
        }, 0)]
      }

      function nameGrouping(person)           { return person[0] }
      function naturalCompare(value1, value2) { return (value1 < value2) ? -1 : (value1 > value2) ? 1 : 0 }
      function id(value)                      { return value }
      function frequency(group)               { return { value: group[0], frequency: group[1].length } }
      function greatThan1(group)              { return group[1].length > 1 }
      function greatThan5(group)              { return group[0] > 5 }
      function isOdd(group)                   { return group[0] % 2 !== 0 }
      function isPair(group)                  { return group[0] % 2 === 0 }

      const persons = [
        [ 'Peter', 3 ],
        [ 'Anna', 4 ],
        [ 'Peter', 7 ],
        [ 'Michael', 10 ],
      ]

      const numbers = [1, 2, 1, 3, 5, 6, 1, 2, 5, 6]

      runTests([
        {
          query: query().select(sumValues).from(structuredClone(persons)).orderBy(naturalCompare).groupBy(nameGrouping),
          stringified: 'query().select(sumValues).from(persons).orderBy(naturalCompare).groupBy(nameGrouping).execute()\n[i.e., SELECT name, sum(value) FROM persons ORDER BY naturalCompare GROUP BY name]',
          expected: [ [ 'Anna', 4 ], [ 'Michael', 10 ], [ 'Peter', 10 ] ],
        },
        {
          query: query().select(frequency).from(structuredClone(numbers)).groupBy(id),
          stringified: 'query().select(frequency).from(numbers).groupBy(id).execute()\n[i.e., SELECT number, count(number) FROM numbers GROUP BY number]',
          expected: [ { 'value': 1, 'frequency': 3 }, { 'value': 2, 'frequency': 2 }, { 'value': 3, 'frequency': 1 }, { 'value': 5, 'frequency': 2 }, { 'value': 6, 'frequency': 2 } ],
        },
        {
          query: query().select(frequency).from(structuredClone(numbers)).groupBy(id).having(greatThan1).having(isPair),
          stringified: 'query().select(frequency).from(numbers).groupBy(id).having(greatThan1).having(isPair).execute()\n[i.e., SELECT number, count(number) FROM numbers GROUP BY number HAVING count(number) > 1 AND isPair(number)]',
          expected: [ { 'value': 2, 'frequency': 2 }, { 'value': 6, 'frequency': 2 } ],
        },
        {
          query: query().select(frequency).from(structuredClone(numbers)).groupBy(id).having(greatThan5, isOdd),
          stringified: 'query().select(frequency).from(numbers).groupBy(id).having(greatThan5, isOdd).execute()\n[i.e., SELECT number, count(number) FROM numbers GROUP BY number HAVING number > 5 OR isOdd(number)]',
          expected: [ { 'value': 1, 'frequency': 3 }, { 'value': 3, 'frequency': 1 }, { 'value': 5, 'frequency': 2 }, { 'value': 6, 'frequency': 2 } ],
        },
      ])
    })

    describe('Join Tests', function() {
      function teacherJoin(join) { return join[0].teacherId === join[1].tutor }
      function student(join)     { return {studentName: join[1].studentName, teacherName: join[0].teacherName} }
      function tutor1(join)      { return join[1].tutor === "1" }

      const teachers = [
        {
          teacherId: '1',
          teacherName: 'Peter'
        },
        {
          teacherId: '2',
          teacherName: 'Anna'
        }
      ]

      const students = [
        {
          studentName: 'Michael',
          tutor: '1'
        },
        {
          studentName: 'Rose',
          tutor: '2'
        }
      ]

      const numbers1 = [1, 2]
      const numbers2 = [4, 5]

      runTests([
        {
          query: query().select(student).from(structuredClone(teachers), structuredClone(students)).where(teacherJoin),
          stringified: 'query().select(student).from(teachers, students).where(teacherJoin).execute()\n[i.e., SELECT studentName, teacherName FROM teachers, students WHERE teachers.teacherId = students.tutor]',
          expected: [ { 'studentName': 'Michael', 'teacherName': 'Peter' }, { 'studentName': 'Rose', 'teacherName': 'Anna' } ],
        },
        {
          query: query().select().from(structuredClone(numbers1), structuredClone(numbers2)),
          stringified: 'query().select().from(numbers1, numbers2).execute()',
          expected: [ [ 1, 4 ], [ 1, 5 ], [ 2, 4 ], [ 2, 5 ] ],
        },
        {
          query: query().select(student).from(structuredClone(teachers), structuredClone(students)).where(teacherJoin).where(tutor1),
          stringified: 'query().select(student).from(teachers, students).where(teacherJoin).where(tutor1).execute()\n[i.e., SELECT studentName, teacherName FROM teachers, students WHERE teachers.teacherId = students.tutor AND tutor = 1]',
          expected: [ { 'studentName': 'Michael', 'teacherName': 'Peter' } ],
        },
        {
          query: query().where(teacherJoin).select(student).where(tutor1).from(structuredClone(teachers), structuredClone(students)),
          stringified: 'query().where(teacherJoin).select(student).where(tutor1).from(teachers, students).execute()\n[i.e., SELECT studentName, teacherName FROM teachers, students WHERE teachers.teacherId = students.tutor AND tutor = 1]',
          expected: [ { 'studentName': 'Michael', 'teacherName': 'Peter' } ],
          msg: 'The order of appearance of the clauses in the chain does not matter'
        },
      ])
    })

    describe('Order of Clause Execution Tests', function() {
      function firstElement(pair)             { return pair[0] }
      function secondElement(pair)            { return pair[1] }
      function naturalCompare(value1, value2) { return (value1 < value2) ? -1 : (value1 > value2) ? 1 : 0 }
      function firstElementOdd(pair)          { return pair[0] % 2 !== 0  }
      function greaterThan6(group)            { return group[0] > 6  }

      const numbers = [[9, 5], [2, 8], [3, 3], [0, 5]]

      runTests([
        {
          query: query().orderBy(naturalCompare).select(secondElement).from(structuredClone(numbers)),
          stringified: 'query().orderBy(naturalCompare).select(secondElement).from(numbers).execute()\n[orderBy MUST execute **AFTER** select; it orders the selected entries, not the other way around!]',
          expected: [3, 5, 5, 8],
        },
        {
          query: query().groupBy(secondElement).where(firstElementOdd).from(structuredClone(numbers)),
          stringified: 'query().groupBy(secondElement).where(firstElementOdd).from(numbers).execute()\n[where MUST execute **BEFORE** groupBy]',
          expected: [[5, [[9, 5]]], [3, [[3, 3]]]],
          msg: `If you are sure you've ordered the two clauses correctly and still get this error, the data structure you're using to store groups (if any) fails to preserve insertion order - make some tweaks ;)`,
        },
        {
          query: query().having(greaterThan6).groupBy(secondElement).from(structuredClone(numbers)),
          stringified: 'query().having(greaterThan6).groupBy(secondNumber).from(numbers).execute()\n[having MUST execute **AFTER** groupBy]',
          expected: [[8, [[2, 8]]]],
        },
        {
          query: query().select(secondElement).having(greaterThan6).groupBy(firstElement).from(structuredClone(numbers)),
          stringified: 'query().select(secondElement).having(greaterThan6).groupBy(firstElement).from(numbers).execute()\n[select MUST execute **AFTER** having and groupBy]',
          expected: [[[9, 5]]],
        },
      ])
    })

    describe('Duplication Exception Tests', function() {
      function id(value) {
        return value
      }

      runErroredTests([
        {
          fn: () => query().select().select().execute(),
          stringified: 'query().select().select().execute()',
          clause: 'SELECT'
        },
        {
          fn: () => query().select().from([]).select().execute(),
          stringified: 'query().select().from([]).select().execute()',
          clause: 'SELECT'
        },
        {
          fn: () => query().select().from([]).from([]).execute(),
          stringified: 'query().select().from([]).from([]).execute()',
          clause: 'FROM'
        },
        {
          fn: () => query().select().from([]).orderBy(id).orderBy(id).execute(),
          stringified: 'query().select().from([]).orderBy(id).orderBy(id).execute()',
          clause: 'ORDERBY'
        },
        {
          fn: () => query().select().groupBy(id).from([]).groupBy(id).execute(),
          stringified: 'query().select().groupBy(id).from([]).groupBy(id).execute()',
          clause: 'GROUPBY'
        },
      ]) 
    })    
  })
})