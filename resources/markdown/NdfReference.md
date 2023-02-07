###Introduction

The NDF language is used to describe game data.
It is a declarative language that defines objects with properties and relations between them, in order to instantiate
the correct data during game execution.

###Syntax

####Charset

All NDF files shall be encoded in either **UTF-8** or **ANSI restricted to the 7-bit table**.
The NDF parser is **case insensitive**: 'TRUE' and 'true' are equivalent.

####Keywords

``export, is, template, unnamed, nil, private, int, string, true, false, div, map``

####Symbols

``//, /, ?, :, =, |, &, <, >, >=, <=, !=, , +, *, %, ,`` (comma)``, . `` (dot)

#### Block delimiters

``{}, [], (), <>, (* *), /* */, ' ', " "``

#### Comments

Everything after the symbol // is ignored until the end of the line.

Everything in blocks delimited by { } or (* \*) or /* */ is ignored.

### Built-in types

#### Boolean

Can only be ``true`` or ``false``.

####Strings

Character strings are delimited by single or double quotes and can contain accentuated characters.

````
"This is a string"
'This ïs ànothér on€'
````

####Integers

Integers are written in base 10 or hexadecimal notation.

````
3
150486
36584
0xFF00A8
0x1
````

#### Floating point numbers

Floating point numbers are written in base 10 natural notation, there is no exponent or hexadecimal notation. The decimal separator is the . (dot) character.

````
3.1415954
9.81
654987.1248
````

The integer part can be omitted (implicit 0). The fractional part can be omitted (implicit 0).

````
.127
53.
````

#### Vector

A vector is a list of zero or more elements enclosed in a **[ ] block** and separated by , (comma).

````
[] // an empty vector
[1, 2, 3] // a vector of integers
["Hello", 'World',] // a trailing comma separator is accepted
````

