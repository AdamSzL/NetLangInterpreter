# 📘 NetLang Language Specification

NetLang is a programming language designed to describe, simulate, and operate on computer networks. 
It enables users to define hosts, routers, switches, interfaces, and connections between them, while also supporting the sending and forwarding of packets in a simulated environment.

This document provides a complete specification of the NetLang language, including its syntax, data types, operators, control structures, and built-in networking instructions.

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Data Types](#data-types)
3. [Variables and Assignments](#variables-and-assignments)
4. [Object Initialization](#object-initialization)
5. [Working with Lists](#working-with-lists)
6. [Scoped Identifiers](#scoped-identifiers)
7. [Operators](#operators)
8. [Control Structures](#control-structures)
9. [Functions](#functions)
10. [Networking Instructions](#networking-instructions)
11. [Printing to the Console](#printing-to-the-console)
12. [Formal Grammar Reference](#formal-grammar-reference)

---

## Introduction

NetLang is a minimal and readable programming language focused on modeling computer networks. It is designed to be intuitive for both students and networking enthusiasts, allowing for the creation of network topologies, routing behaviors, and packet transmission scenarios.

Programs in NetLang typically consist of:
- Definitions of network devices and their ports
- Variable declarations and logic
- Instruction-based interaction with the simulated network (e.g., `send`, `connect`)
- Optional user-defined functions for automation or abstraction

The language is interpreted and is backed by a custom interpreter built using Python and ANTLR.

---

## Data Types

NetLang supports a variety of data types, grouped into two categories:

---

### 🔹 Primitive Types

These types represent single, non-structured values.

| Type     | Description                                                   |
|----------|---------------------------------------------------------------|
| `int`    | Integer number                                                |
| `float`  | Floating-point number                                         |
| `bool`   | Boolean value (`true` / `false`)                              |
| `string` | Text string                                                   |
| `void`   | Special type for functions with no return value               |
| `IP`     | Represents an IPv4 address (e.g. `192.168.1.1`)               |
| `MAC`    | Represents a MAC address (e.g. `00:1A:2B:3C:4D:5E`)           |
| `[type]` | List of values of the specified type (e.g. `[int]`, `[Port]`) |

---

### 🧱 Object Types

These are complex structured types used for network modeling.

#### 🟦 `CopperEthernetPort`

| Field       | Type   | Required? |
|-------------|--------|-----------|
| `portId`    | string | ✅         |
| `ip`        | CIDR   | ❌         |
| `mac`       | MAC    | ❌         |
| `bandwidth` | int    | ❌         |
| `mtu`       | int    | ❌         |
| `gateway`   | IP     | ❌         |

---

#### 🟦 `OpticalEthernetPort`

| Field        | Type   | Required? |
|--------------|--------|-----------|
| `portId`     | string | ✅         |
| `ip`         | CIDR   | ❌         |
| `mac`        | MAC    | ❌         |
| `bandwidth`  | int    | ❌         |
| `wavelength` | int    | ❌         |
| `mtu`        | int    | ❌         |
| `connector`  | string | ❌         |
| `gateway`    | IP     | ❌         |

---

#### 🟦 `Port`

Generic, abstract port type (shared structure with Copper/Optical).

| Field       | Type   | Required? |
|-------------|--------|-----------|
| `portId`    | string | ✅         |
| `ip`        | CIDR   | ❌         |
| `mac`       | MAC    | ❌         |
| `bandwidth` | int    | ❌         |
| `mtu`       | int    | ❌         |
| `gateway`   | IP     | ❌         |

---

#### 🟦 `CIDR`

Represents an IP address with subnet mask.

| Field       | Type | Required?     |
|-------------|------|---------------|
| `ip`        | IP   | ✅             |
| `mask`      | int  | ✅             |
| `network`   | CIDR | 🔒 (readonly) |
| `broadcast` | CIDR | 🔒 (readonly) |

---

#### 🟦 `Host`

| Field     | Type    | Required? |
|-----------|---------|-----------|
| `name`    | string  | ✅         |
| `ports`   | [Port]  | ✅         |

---

#### 🟦 `Switch`

| Field     | Type    | Required? |
|-----------|---------|-----------|
| `name`    | string  | ✅         |
| `ports`   | [Port]  | ✅         |

---

#### 🟦 `Router`

| Field          | Type           | Required? |
|----------------|----------------|-----------|
| `name`         | string         | ✅         |
| `ports`        | [Port]         | ✅         |
| `routingTable` | [RoutingEntry] | ✅         |

---

#### 🟦 `RoutingEntry`

| Field         | Type   | Required? |
|---------------|--------|-----------|
| `destination` | CIDR   | ✅         |
| `via`         | string | ✅         |
| `nextHop`     | IP     | ❌         |

## Variables and Assignments

In NetLang, variables are declared using the `set` keyword. A variable declaration can include a type annotation, an initial value, or both. NetLang supports both **explicit typing** and **type inference**, as well as later assignment using the `<-` operator.

---

### 🔹 Variable Declaration Syntax

```netlang
set variableName: type <- value
```

You can omit either the type or the value, but **not both**.

#### ✅ Valid declarations

```netlang
set a: int <- 5          // Explicit type and initial value
set b <- "hello"         // Type inferred from the value
set c: float             // Declared but not initialized (unassigned)
```

#### ❌ Invalid declarations

```netlang
set d                   // ❌ Missing both type and value
```

If a variable is declared with a type but no value, it is **uninitialized**. Using such a variable before assignment will result in a **runtime error**.

---

### 🔹 Variable Assignment

To assign or update the value of an existing variable, use the `<-` operator:

```netlang
x <- 10
host.ports<0>.ip <- CIDR { 
    ip <- 10.0.0.1, 
    mask <- 24 
}
```

The left-hand side may be a plain variable or a field access expression.

---

### 🧠 Notes

- Once a variable is declared, its type is fixed.
- You cannot assign a value of a mismatched type.
- Nested object fields (e.g. `router.routingTable<0>.via`) can also be updated via assignment.

## Object Initialization

NetLang supports inline object initialization using a clear, structured syntax.  
Objects are created by specifying the type followed by a block of field assignments using `<-`.

---

### 🔹 Syntax

```netlang
TypeName {
    field1 <- value1,
    field2 <- value2,
    ...
}
```

- Field names must match the names defined in the type.
- Required fields must be specified.
- Optional fields may be omitted.
- Fields are assigned using `<-`, not `=`.
- Nested objects and lists are supported.

---

### ✅ Example: Creating a Host with a Port

```netlang
set hostA <- Host {
    name <- "Host A",
    ports <- [
        OpticalEthernetPort {
            portId <- "eth0",
            ip <- 192.168.1.0/24
        }
    ]
}
```

This creates a `Host` object with:
- `name` set to `"Host A"`
- `ports` containing a single `OpticalEthernetPort` with:
  - `portId = "eth0"`
  - `ip = 192.168.1.0/24`

---

### 🔁 Nested Initialization

Object fields can themselves be other objects or lists of objects:

```netlang
set route <- RoutingEntry {
    destination <- CIDR {
        ip <- 10.0.0.0,
        mask <- 24
    },
    via <- "eth1"
}
```

---

### 🧠 Notes

- You can combine object initializers inside expressions or assignments.
- You cannot omit required fields.
- Read-only fields (e.g. `network`, `broadcast` in `CIDR`) are computed automatically and cannot be set manually.

## Working with Lists

NetLang supports list types (`[type]`) and provides syntax for element access, insertion, and deletion.

---

### 🔹 List Indexing

To access an element at a specific index, use angle bracket notation:

```netlang
names<0>         // Access the first element
host.ports<1>    // Access the second port in a host
```

- Indexing starts at 0
- Out-of-range access results in a runtime error
- You can chain indexes and field access

---

### ➕ Adding to a List

Use the `add` statement to append an element to a list field.

#### 🔹 Syntax

```netlang
add value to list
```

#### ✅ Example

```netlang
add "Alice" to names
add CopperEthernetPort {
    portId <- "eth2"
} to host.ports
```

- `fieldAccess` must refer to a list
- The type of `expression` must match the element type of the list

---

### ❌ Deleting from a List

Use the `delete` statement to remove an element by index.

#### 🔹 Syntax

```netlang
delete list<index>
```

#### ✅ Example

```netlang
delete names<0>
delete router.routingTable<2>
```

- Removing out-of-range indexes will cause a runtime error

---

### 🧠 Notes

- Lists are mutable
- You can assign a new value directly to a list element using indexing:

```netlang
names<1> <- "Bob"
host.ports<0>.ip <- 192.168.1.1/24
```
- Adding and deleting elements modifies the list in place

## Scoped Identifiers

NetLang allows variables and functions to be referenced from different scopes using prefix operators. This mechanism is especially useful inside nested functions or control blocks.

---

### 🔹 Syntax

A `scopedIdentifier` may include one of the following optional prefixes:

| Prefix  | Meaning                      | Example             |
|---------|------------------------------|---------------------|
| `~`     | Global scope                 | `~globalVar`        |
| `^`     | Parent scope (one level up)  | `^x`, `^^x`         |

---

### 📘 Examples

```netlang
set x <- 10

define outer() => void {
    set x <- 20

    define inner() => void {
        print x        // Refers to local x = 20
        print ^x       // Refers to x in outer() = 20
        print ~x       // Refers to global x = 10
    }

    inner()
}
```

---

### 🧠 Notes

- You can stack `^` symbols to move further up the call hierarchy (`^^x`, `^^^x`, etc.).
- If the referenced scope does not exist (e.g. too many `^`), a runtime error will occur.
- This applies to both **variables** and **function references**.

---

Scoped access helps prevent accidental shadowing and enables better modularity in nested environments.


## Operators

NetLang supports a rich set of operators for building expressions. These include arithmetic, logical, comparison, equality, and casting operations. Expressions follow a strict operator precedence model, similar to C or Java.

---

### 🔢 Operator Precedence

Operators are grouped by precedence (from highest to lowest):

| Precedence | Operator(s)          | Description                             | Associativity     |
|------------|----------------------|-----------------------------------------|-------------------|
| 1          | `()`                 | Parentheses (grouping)                  | —                 |
| 2          | `x^y`                | Power                                   | Right-associative |
| 3          | `+x`, `-x`           | Unary plus, minus                       | Right-associative |
| 4          | `as type`            | Explicit cast                           | Right-associative |
| 5          | `*`, `/`, `\`, `%`   | Multiplication, division, floor, modulo | Left-associative  |
| 6          | `+`, `-`             | Addition, subtraction                   | Left-associative  |
| 7          | `==`, `!=`           | Equality                                | Left-associative  |
| 8          | `<`, `>`, `<=`, `>=` | Comparison                              | Left-associative  |
| 9          | `!`                  | Logical NOT                             | Right-associative |
| 10         | `&&`                 | Logical AND                             | Left-associative  |
| 11         | `\|\|`               | Logical OR                              | Left-associative  |

---

### 📘 Supported Operators by Type

#### ➕ Addition (`+`)
- Supported types:
  - `int + int` → `int`
  - `float + float` → `float`
  - `int + float` / `float + int` → `float`
  - `string + anything` -> `string`
  - `IP + int` → `IP`
  - `CIDR + int` → `CIDR`

#### ➖ Subtraction (`-`)
- Supported types:
  - `int - int` → `int`
  - `float - float` → `float`
  - `int - float` / `float - int` → `float`
  - `IP - int` → `IP`
  - `CIDR - int` → `CIDR`

#### ✖️➗ Multiplication, Division, Floor Division, Modulo (`*`, `/`, `\`, `%`)
- Supported types:
  - `int * int` → `int`
  - `int / int` or with `float` → `float`
  - `float * float` → `float`
  - `int \ int` or `float \ float` (any combination) → `int`
  - `int % int` → `int`
- ❌ Modulo `%` is **only allowed for `int % int`**

#### ⬆️ Power (`^`)
- Supported types:
  - Base: `int` or `float`
  - Exponent: `int` or `float`
  - Result:
    - If both are `int` → `int`
    - Otherwise → `float`

#### 🔁 Casting (`as`)
- Supported cast pairs:
  - `int` ↔ `float`
  - `int`, `float`, `bool`, `string` (all mutually castable)
- Lists `[T]` can be cast to `[U]` if `T → U` is a valid scalar cast

---

Invalid or unsupported operations will trigger a `NetLangTypeError` before runtime.

---

### 🧪 Example Expressions

```netlang
print 5 + 2 * 3                 // 11
print (5 + 2) * 3               // 21
print !true || false            // false
print "abc" + 5                 // "abc5"
print 2.3 as int                // 2
```

---

### 🧠 Notes

- You can use parentheses `()` to override precedence.
- All expressions are evaluated left-to-right unless otherwise noted.
- Object creation (`MyType { ... }`) and function calls are also expressions.

## Control Structures

NetLang supports conditional statements and several loop constructs to control the flow of program execution.

---

### ✅ Conditional Statements (`if`, `else if`, `else`)

NetLang allows standard branching logic using `if`, `else if`, and `else`.

#### 🔹 Syntax

```netlang
if condition {
    // code block
} else if anotherCondition {
    // optional else-if
} else {
    // optional fallback
}
```

- `condition` must be a boolean expression.
- You can include any number of `else if` branches.
- The `else` clause is optional.

---

### 🔁 Loops

NetLang includes three main types of loops:

### 1️⃣ `repeat x times as index { ... }`

Repeat a block a fixed number of times.

#### 🔹 Syntax

```netlang
repeat x times as i {
    print i
}
```

- The loop runs from `0` to `x - 1`.
- The loop variable (`i`) is available inside the block.

---

### 2️⃣ `repeat from a to b step s as index { ... }`

Repeat over a numeric range.

#### 🔹 Syntax

```netlang
repeat from a to b step s as index {
    print index
}
```

- Loops from `a` (inclusive) to `b` (inclusive).
- `step` is optional and defaults to `1`.

---

### 3️⃣ `repeat while condition { ... }`

Standard while-loop that continues as long as the condition is true.

#### 🔹 Syntax

```netlang
repeat while x < 10 {
    x <- x + 1
}
```

---

### 4️⃣ `each item from list { ... }`

Iterate over each element of a list.

#### 🔹 Syntax

```netlang
each item from devices {
    print device.name
}
```

- The loop variable (e.g. `device`) is assigned to each element of the list.
- List must be iterable (e.g. `[int]`, `[Port]`, etc.).

---

### ⏹️ Loop Control: `exit` and `next`

NetLang provides two statements for controlling the flow inside loops:

---

#### 🔹 `exit`

Immediately terminates the nearest enclosing loop (similar to `break` in other languages).

```netlang
repeat 10 times as i {
    if i == 5 {
        exit
    }
    print i
}
```

---

#### 🔹 `next`

Skips the rest of the current loop iteration and continues with the next one (similar to `continue`).

```netlang
each name from names {
    if name == "admin" {
        next
    }
    print name
}
```

---

These statements can be used in any loop: `repeat`, `repeat from`, `repeat while`, or `each`.


### 🧠 Notes

- Loop variables are scoped within the loop body.
- You can use nested loops and conditional blocks.
- All blocks use `{ ... }` regardless of context.

## Functions

NetLang allows users to define reusable blocks of logic using named functions. Functions can have typed parameters and an optional return type.

---

### 🧾 Function Definition

Functions are defined using the `define` keyword.

#### 🔹 Syntax

```netlang
define functionName(param1: Type1, param2: Type2) => ReturnType {
    // function body
}
```

- You may omit the return type for `void` functions.
- Parameters must include both name and type.
- The return type must be a valid NetLang type (`int`, `bool`, `string`, etc.).

#### ✅ Examples

```netlang
define add(a: int, b: int) => int {
    return a + b
}

define sayHello(name: string) => void {
    print "Hello ", name
}
```

---

### 📞 Function Calls

Functions are called by their name followed by arguments in parentheses.

#### 🔹 Syntax

```netlang
functionName(arg1, arg2)
```

- The number and types of arguments must match the function's signature.
- You can also use scoped access (`~function`, `^function`) to call non-local functions.

#### ✅ Example

```netlang
set result <- add(3, 5)
sayHello("NetLang")
```

---

### 🔙 Return Statement

Use the `return` keyword to return a value from a function.

#### 🔹 Syntax

```netlang
return expression
```

- The expression must match the function’s declared return type.
- `return` without an expression is only allowed in `void` functions.

#### ✅ Example

```netlang
define square(x: int) => int {
    return x * x
}

define logMessage(msg: string) => void {
    print msg
    return
}
```

---

### 🧠 Notes

- Functions may be defined globally or nested within other functions.
- You can use scoped identifiers (`^`, `~`) to access functions from parent/global scopes.
- Recursive calls are allowed.


## Networking Instructions

NetLang provides special statements for modeling and simulating network behavior. These include port connections and packet transmissions.

---

### 🔗 `connect` – Connecting Ports

The `connect` instruction is used to create a link between two ports on different devices.

#### 🔹 Syntax

```netlang
connect firstPort to secondPort
```

#### ✅ Example

```netlang
connect hostA.ports<0> to switch.ports<0>
connect hostB.ports<0> to switch.ports<1>
```

- Both sides must refer to valid `Port` objects (e.g. `CopperEthernetPort`, `OpticalEthernetPort`)
- You cannot connect two ports of the same device
- The port types must match (e.g. copper-to-copper)
- Each port can only be connected to one other port

---

### 📦 `send` – Sending a Packet

The `send` instruction is used to transmit a packet from one host to a target IP address.

#### 🔹 Syntax

```netlang
send "message" from port to ipAddress
```

#### ✅ Example

```netlang
send "Hi from Host A" from hostA.ports<0> to 192.168.1.1
```

- The first argument is a string representing the message payload
- The target must be a valid IPv4 address
- The interpreter will simulate transmission using ARP, routing, and connected devices

---

### 🎨 Visualization

Calling `send` will also:
- Display the **network graph** with currently connected devices
- Animate the **packet path** across links and routers
- Log the **delivery status**

---

### 🧠 Notes

- `connect` modifies the simulated topology
- `send` uses routing tables and gateways defined earlier in the program
- Invalid or unreachable destinations will trigger an error or visualization of a failed delivery

## Printing to the Console

NetLang provides a `print` statement to output one or more values to the console.

---

### 🔹 Syntax

```netlang
print expression1, expression2, ...
```

- You can print a single expression or a comma-separated list.
- Each expression is evaluated, converted to string, and separated by a space.

---

### ✅ Examples

```netlang
set x <- 2
set y <- 6.82

print "Hello, world"
print x
print "Result:", x + y
print true, false, 123, "text"
```

Output:

```
Hello, world
2
Result: 8.82
true false 123 text
```

---

### 🧠 Notes

- Boolean values print as `true` or `false`.
- `void` (no value) prints as `void`.
- Lists, objects, and IP/MAC types are converted using their string representation.

## Formal Grammar Reference

See [grammar.md](grammar.md) for the complete ANTLR grammar used to parse NetLang.
