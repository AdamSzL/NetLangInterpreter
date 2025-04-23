grammar NetLang;

program: statement* EOF;

// ----------- Statements ----------
statement
    : listIndexAssignment
    | variableDeclaration
    | variableAssignment
    | addToListStatement
    | removeFromListStatement
    | fieldAssignment
    | connectStatement
    | disconnectStatement
    | showInterfacesStatement
    | sendPacketStatement
    | ifStatement
    | printStatement
    | loopStatement
    | functionDeclarationStatement
    | returnStatement
    ;


// ----------- Variable Declaration ----------
variableDeclaration
    : 'set' ID COLON type ASSIGN expression
    ;

// ----------- Variable Assignment ----------
variableAssignment
    : ID '<-' expression
    ;

// Add to list
addToListStatement
    : 'add' expression 'to' fieldAccess
    ;

// Remove from list
removeFromListStatement
    : 'remove' expression 'from' fieldAccess
    ;

fieldAssignment
    : fieldAccess ASSIGN expression
    ;

connectStatement
    : 'connect' fieldAccess 'to' fieldAccess
    ;

disconnectStatement
    : 'disconnect' (fieldAccess 'from' fieldAccess | ID)
    ;

showInterfacesStatement
    : 'show' 'interfaces' 'of' ID
    ;

sendPacketStatement
    : 'send' ID 'from' fieldAccess 'to' IPADDR
    | 'send' 'from' fieldAccess 'to' IPADDR 'with' objectInitializer
    ;

ifStatement
    : 'if' expression block (elseIfClause)* (elseClause)?
    ;

elseIfClause
    : 'else' 'if' expression block
    ;

elseClause
    : 'else' block
    ;

block
    : '{' statement* '}'
    ;

printStatement
    : 'print' expression
    ;

loopStatement
    : repeatTimesLoop
    | repeatWhileLoop
    | eachLoop
    ;

repeatTimesLoop
    : 'repeat' INT 'times' 'as' ID block
    ;

repeatWhileLoop
    : 'repeat' 'while' expression block
    ;

eachLoop
    : 'each' ID 'from' ID block
    ;

functionDeclarationStatement
    : 'define' ID '(' parameterList? ')' '=>' type block
    ;

parameterList
    : parameter (',' parameter)*
    ;

parameter
    : ID ':' type
    ;

returnStatement
    : 'return' expression
    ;

listIndexAssignment
    : listIndexAccess ASSIGN expression
    ;

// ----------- Types ----------
type
    : 'int'
    | 'float'
    | 'bool'
    | 'string'
    | 'IP'
    | 'MAC'
    | 'Port'
    | '[' type ']'
    | objectType
    | deviceType
    ;

objectType
    : 'CIDR'
    | 'CopperEthernetPort'
    | 'OpticalEthernetPort'
    | 'WirelessPort'
    | 'RoutingEntry'
    | 'Packet'
    ;

deviceType
    : 'Router'
    | 'Host'
    | 'Switch'
    ;

// ----------- Expressions ----------
operatorExpression
    : <assoc=right> NOT operatorExpression                #unaryNotExpr
    | operatorExpression MUL operatorExpression           #mulExpr
    | operatorExpression DIV operatorExpression           #divExpr
    | operatorExpression PLUS operatorExpression          #addExpr
    | operatorExpression MINUS operatorExpression         #subExpr
    | operatorExpression LT operatorExpression            #ltExpr
    | operatorExpression GT operatorExpression            #gtExpr
    | operatorExpression LE operatorExpression            #leExpr
    | operatorExpression GE operatorExpression            #geExpr
    | operatorExpression EQ operatorExpression            #eqExpr
    | operatorExpression NEQ operatorExpression           #neqExpr
    | operatorExpression AND operatorExpression           #andExpr
    | operatorExpression OR operatorExpression            #orExpr
    | '(' operatorExpression ')'                          #parenExpr
    //| expression                                          #primaryExpr
    ;

expression
    : ID
    | INT
    | FLOAT
    | BOOL
    | STRING
    | IPADDR
    | MACADDR
    | listLiteral
    | cidrLiteral
    | objectInitializer
    | fieldAccess
    | functionCall
    | listIndexAccess
    ;

listLiteral
    : '[' expressionList? ']'
    ;

expressionList
    : expression (COMMA expression)*
    ;

cidrLiteral
    : '[' ID ']' '/' INT
    |  IPADDR '/' INT
    ;

objectInitializer
    : (objectType | deviceType)? '{' objectFieldList? '}'
    ;

objectFieldList
    : objectField (COMMA objectField)*
    ;

objectField
    : ID ASSIGN expression
    ;

fieldAccess
    : ID ('.' ID | '<' expression '>')*
    ;

functionCall
    : 'execute' ID 'params' expression
    ;

listIndexAccess
    : ID '<' expression '>'
    ;

// ----------- Lexical Rules ----------
ASSIGN: '<-';
COLON: ':';
COMMA: ',';
DOT: '.';

// Arithmetic operators
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';

// Comparison operators
EQ: '==';
NEQ: '!=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';

// Logical operators
AND: '&&';
OR: '||';
NOT: '!';

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

WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;