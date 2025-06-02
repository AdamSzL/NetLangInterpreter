# NetLang Grammar Documentation

This document provides a detailed overview of the grammar rules defined in the `NetLang.g4` file used by the NetLang interpreter.

---

# Parser Rules

## Program Structure

```
program: statement* EOF;
```

A NetLang program consists of a sequence of statements, followed by the end of file.

---

## Statements

The core building blocks of the language:

```
statement:
    : listIndexAssignment
    | variableDeclaration
    | variableAssignment
    | addToListStatement
    | deleteListElementStatement
    | fieldAssignment
    | connectStatement
    | sendPacketStatement
    | ifStatement
    | printStatement
    | loopStatement
    | functionDeclarationStatement
    | returnStatement
    | functionCall
    | breakStatement
    | continueStatement
    ;
```

---

### Variable Declarations and Assignments

```antlr
variableDeclaration
    : 'set' ID COLON type ASSIGN expression
    ;
```
Declares a new variable with type and value.

```antlr
variableAssignment
    : scopedIdentifier '<-' expression
    ;
```
Assigns a new value to an existing variable.

---

### List Operations

```antlr
addToListStatement
    : 'add' expression 'to' fieldAccess
    ;
```
Adds a new element with value 'expression' to a list.

```antlr
deleteListElementStatement
    : 'delete' listIndexAccess
    ;
```
Removes an element from a specified index of a list.

---

### Field Assignment

```antlr
fieldAssignment
    : fieldAccess ASSIGN expression
    ;
```
Assigns a value to an object's field.

---

### Connection and Packet

```antlr
connectStatement
    : 'connect' fieldAccess 'to' fieldAccess
    ;
```
Connects two ports.

```antlr
sendPacketStatement
    : 'send' STRING 'from' fieldAccess 'to' IPADDR
    ;
```
Sends a packet from source port represented by fieldAccess to destination ip address.
Draws the network graph and starts the packet animation.

---

### Print statement

```antlr
printStatement
    : 'print' expression
    ;
```

---

### Control Flow

#### If-else Statement statements
```antlr
ifStatement
    : 'if' expression block (elseIfClause)* (elseClause)?
    ;
```
Classic if-else statement.

```antlr
elseIfClause
    : 'else' 'if' expression block
    ;
```

```antlr
elseClause
    : 'else' block
    ;
```

```antlr
block
    : '{' statement* '}'
    ;
```
A block of statements. Creates a new scope.

#### Loop Statement
```antlr
loopStatement:
    : repeatTimesLoop
    | repeatWhileLoop
    | eachLoop;
```

```antlr
repeatTimesLoop
    : 'repeat' expression 'times' 'as' ID block # RepeatTimes
    | 'repeat' 'from' expression 'to' expression ('step' expression)? 'as' ID block # RepeatRange
    ;
```
- `RepeatTimes`: repeat a block N times.
- `RepeatRange`: initializes a counter with value specified after 'from', after each iteration updates the counter by the value after 'step' (1 if not specified), and loops until it reaches the value after 'to'.

```antlr
repeatWhileLoop
    : 'repeat' 'while' expression block
    ;
```
Repeats the block as long as 'expression' evaluates to true.

```antlr
eachLoop
    : 'each' ID 'from' expression block
    ;
```
Loops through each element of the list (of value 'expression'), with each item being accessible as ID.

---

### Functions

#### Function declaration

```antlr
functionDeclarationStatement
    : 'define' ID '(' parameterList? ')' ('=>' type)? block
    ;
```
Declares a function with name ID, parameters specified by parameterList, and with return type of 'type' and 'block' for the function body.
If the return type is not specified, it defaults to 'void'.

```antlr
parameterList
    : parameter (',' parameter)*
    ;
```

```antlr
parameter
    : ID ':' type
    ;
```

```antlr
returnStatement
    : 'return' expression?
    ;
```
Used to return a value from a function. Cannot be used outside of one.

#### Calling functions

```antlr
functionCall
    : scopedIdentifier '(' expressionList? ')'
    ;
```
Invokes a function referenced by scopedIdentifier, with parameters specified by expressionList.

---

### Break ('exit') and continue ('next')

```antlr
breakStatement: 'exit';
```
The 'exit' keyword is used to break from a loop.

```antlr
continueStatement: 'next';
```
The 'next' keyword is used to skip the current iteration and proceed to the next one.

---

## Types

```antlr
type
    : 'int'
    | 'float'
    | 'bool'
    | 'string'
    | 'void'
    | 'IP'
    | 'MAC'
    | '[' type ']'
    | objectType
    | deviceType
    ;
```
All types in NetLang.

```antlr
objectType
    : 'CIDR'
    | 'CopperEthernetPort'
    | 'OpticalEthernetPort'
    | 'WirelessPort'
    | 'RoutingEntry'
    | 'Port'
    ;
```
Types of objects in NetLang. These can be used in objectInitializer to construct objects.

```antlr
deviceType
    : 'Router'
    | 'Host'
    | 'Switch'
    ;
```
Types of devices in NetLang. These can also be used in objectInitializer.

---

## Expressions

### Identifiers


```antlr
scopedIdentifier
    : scopePrefix? ID
    ;
```

```antlr
scopePrefix
    : '^'+
    | '~'
    ;
```
Scoped identifier is used to access variables and functions defined in different scopes.
'^' is used for referencing parent scope (can be stacked - e.g. '^^^'). '~' is used for referencing the global scope.

---

### Operators

Expressions support arithmetic, logical, comparison, and function calls. Expressions are chained in a way that supports proper operator precedence. Part of the expression tree:
```antlr
expression: orExpr;
orExpr: andExpr ('||' andExpr)*;
andExpr: notExpr ('&&' notExpr)*;
notExpr: '!' notExpr | comparisonExpr;
...
```
Full tree is available in the NetLang.g4 file.

Expressions include:
- Arithmetic: `+`, `-`, `*`, `/`, `\`, `%`, `^`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logic: `&&`, `||`, `!`
- Literals: int, float, bool, string, IPADDR, MACADDR
- Casts: `as` type

---

### Atom expression
```antlr
atomExpr
    : '(' expression ')'              # ParensExpr
    | scopedIdentifier                # VariableExpr
    | INT                             # IntLiteral
    | FLOAT                           # FloatLiteral
    | BOOL                            # BoolLiteral
    | STRING                          # StringLiteral
    | cidrLiteral                     # CIDRLiteralExpr
    | IPADDR                          # IPAddressLiteral
    | MACADDR                         # MacAddressLiteral
    | listLiteral                     # ListLiteralExpr
    | objectInitializer               # ObjectInitializerExpr
    | fieldAccess                     # FieldAccessExpr
    | functionCall                    # FunctionCallExpr
    | listIndexAccess                 # ListIndexAccessExpr
    ;
```

---

### Literals

#### List literal
```antlr
listLiteral
    : '[' expressionList? ']'
    ;
```
A literal representing a list, with values expressed by 'expressionList'.

```antlr
expressionList
    : expression (COMMA expression)*
    ;
```
A list of values separated by a comma.

---

#### CIDR literal
```antlr
cidrLiteral
    : '[' scopedIdentifier ']' '/' INT
    |  IPADDR '/' INT
    ;
```
An IP address with a subnet mask. Can be used either with an identifier representing the IP, e.g. [hostIP]/24, or with an IP literal.

---

#### Object literals

```antlr
objectInitializer
    : (objectType | deviceType)? '{' objectFieldList? '}'
    ;
```
```antlr
objectFieldList
    : objectField (COMMA objectField)*
    ;
```

```antlr
objectField
    : ID ASSIGN expression
    ;
```
Used for instantiating objects with fields specified by objectFieldList.

---

### Accessing Fields and Lists

```antlr
fieldAccess
    : scopedIdentifier ('.' ID | '<' expression '>')*
    ;
```
Used to access object fields or list elements.

---

# Lexical Rules

## Break ('exit') and continue ('next')

```antlr
EXIT: 'exit';
NEXT: 'next';
```

## Operators

```antlr
ASSIGN: '<-';
COLON: ':';
COMMA: ',';
DOT: '.';

PLUS: '+';
MINUS: '-';
MUL: '*';
FLOORDIV: '\\';
DIV: '/';
MOD: '%';
POW: '^';

EQ: '==';
NEQ: '!=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';

AND: '&&';
OR: '||';
NOT: '!';
```

## Literals - bool, ID, int, float, string, IP and MAC addresses

```antlr
BOOL: 'true' | 'false';
ID: [a-zA-Z_] [a-zA-Z_0-9]*;

INT: [0-9]+;
FLOAT: [0-9]+ DOT [0-9]+;
STRING: '"' (~["\\] | '\\' .)* '"';

IPADDR: UP_TO_THREE_DIGITS DOT UP_TO_THREE_DIGITS DOT UP_TO_THREE_DIGITS DOT UP_TO_THREE_DIGITS;
fragment UP_TO_THREE_DIGITS: [0-9] [0-9]? [0-9]?;

MACADDR: HEXPAIR COLON HEXPAIR COLON HEXPAIR COLON HEXPAIR COLON HEXPAIR COLON HEXPAIR;
fragment HEXPAIR: HEX HEX;
fragment HEX: [0-9A-Fa-f];
```

## Comments

```antlr
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
```