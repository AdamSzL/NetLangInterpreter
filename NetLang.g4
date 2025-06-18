grammar NetLang;

program: statement* EOF;

statement
    : variableDeclaration
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
    | block
    ;

variableDeclaration
    : 'set' ID (COLON type)? (ASSIGN expression)?
    ;

variableAssignment
    : scopedIdentifier '<-' expression
    ;

addToListStatement
    : 'add' expression 'to' fieldAccess
    ;

deleteListElementStatement
    : 'delete' fieldAccess
    ;

fieldAssignment
    : fieldAccess ASSIGN expression
    ;

connectStatement
    : 'connect' fieldAccess 'to' fieldAccess
    ;

sendPacketStatement
    : 'send' STRING 'from' fieldAccess 'to' IPADDR
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
    : 'print' expressionList
    ;

loopStatement
    : repeatTimesLoop
    | repeatWhileLoop
    | eachLoop
    ;

repeatTimesLoop
    : 'repeat' expression 'times' 'as' ID block # RepeatTimes
    | 'repeat' 'from' expression 'to' expression ('step' expression)? 'as' ID block # RepeatRange
    ;

repeatWhileLoop
    : 'repeat' 'while' expression block
    ;

eachLoop
    : 'each' ID 'from' expression block
    ;

functionDeclarationStatement
    : 'define' ID '(' parameterList? ')' ('=>' type)? block
    ;

parameterList
    : parameter (',' parameter)*
    ;

parameter
    : ID ':' type
    ;

returnStatement
    : 'return' expression?
    ;

breakStatement
    : EXIT
    ;

continueStatement
    : NEXT
    ;

scopedIdentifier
    : scopePrefix? ID
    ;

scopePrefix
    : '^'+
    | '~'
    ;

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
    ;

objectType
    : 'CIDR'
    | 'CopperEthernetPort'
    | 'OpticalEthernetPort'
    | 'RoutingEntry'
    | 'Port'
    | 'Router'
    | 'Host'
    | 'Switch'
    ;

expression
    : orExpr
    ;

orExpr
    : andExpr (OR andExpr)*
    ;

andExpr
    : notExpr (AND notExpr)*
    ;

notExpr
    : NOT notExpr
    | comparisonExpr
    ;

comparisonExpr
    : equalityExpr ( (LT | GT | LE | GE) equalityExpr )*
    ;

equalityExpr
    : addSubExpr ( (EQ | NEQ) addSubExpr )*
    ;

addSubExpr
    : mulDivExpr ( (PLUS | MINUS) mulDivExpr )*
    ;

mulDivExpr
    : castExpr ( (MUL | DIV | FLOORDIV | MOD) castExpr)*
    ;

castExpr
    : unaryExpr ('as' type)?
    ;

unaryExpr
    : PLUS unaryExpr
    | MINUS unaryExpr
    | powExpr
    ;

powExpr
    : atomExpr (POW powExpr)?
    ;

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
    ;

listLiteral
    : '[' expressionList? ']'
    ;

expressionList
    : expression (COMMA expression)*
    ;

cidrLiteral
    : '[' fieldAccess ']' '/' INT
    |  IPADDR '/' INT
    ;

objectInitializer
    : objectType '{' objectFieldList? '}'
    ;

objectFieldList
    : objectField (COMMA objectField)*
    ;

objectField
    : ID ASSIGN expression
    ;

fieldAccess
    : scopedIdentifier ('.' ID | '<' expression '>')*
    ;

functionCall
    : scopedIdentifier '(' expressionList? ')'
    ;

// ----------- Lexical Rules ----------
EXIT: 'exit';
NEXT: 'next';

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