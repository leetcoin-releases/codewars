# [**An 'orrible expression on 'is face**](https://www.codewars.com/kata/57f3c59fab9a91db28000027)

## **Description:**
This regular expression is supposed to create an 'orrifically inaccurate Cockney translation of any given string. However, there's something wrong with it.

For example, given the string
```md
hello there
```

it should return the value
```md
`ello there
```

but instead it's returning
```md
Hello t`ere
```

Can you fix it?

## **Solutions:**
```js
const cockney = /\b[hH]/g;
const replacement = "`";
```