# NDF Reference

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

``//, /, ?, :, =, |, &, <, >, >=, <=, !=, , +, *, %, ,`` (comma)``, . ``(dot)

#### Block delimiters

``{}, [], (), <>, (* *), /* */, ' ', " "``

#### Comments

Everything after the symbol // is ignored until the end of the line.

Everything in blocks delimited by { } or (* \*) or /* */ is ignored.

### Built-in types

#### Boolean

Can only be ``true`` or ``false``.

