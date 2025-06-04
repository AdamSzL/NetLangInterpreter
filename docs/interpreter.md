# 🧠 Interpreter Architecture (Implementation Overview)

This document describes the structure and implementation of the NetLang interpreter.

---

## 🧾 Overview

The NetLang interpreter is implemented in **Python** and designed as a **two-pass execution engine** using the ANTLR4 parser generator.

### 🔁 Two-pass design:
1. **TypeCheckingVisitor** – validates variable declarations, type safety, expressions, and function calls.
2. **Interpreter** – executes the code after type checking has passed successfully.

Both visitors implement traversal over the AST (Abstract Syntax Tree) produced from the grammar defined in [`NetLang.g4`](../NetLang.g4).

---

## 📁 Project Structure

### `main.py`
Entry point script for launching the interpreter from the command line:
```bash
python3 main.py program.netlang
```
This script initializes the ANTLR parser, runs type checking, and executes the program using the interpreter.

### `/interpreter/` – Execution logic (main visitor)

| File             | Description                                                                                                           |
|------------------|-----------------------------------------------------------------------------------------------------------------------|
| `interpreter.py` | Entry point for executing NetLang programs. Implements `visitProgram`, `visitPrintStatement`, and statement dispatch. |
| `flowcontrol.py` | Implements loops (`repeat`, `while`, `each`) and `if` statements.                                                     |
| `functions.py`   | Handles function definitions, return statements, and calling functions.                                               |
| `variables.py`   | Manages variable declaration, assignment, and scope resolution.                                                       |
| `fields.py`      | Processes field access and indexed access like `host.ports<0>.ip`.                                                    |
| `packets.py`     | Contains logic for building and forwarding network packets.                                                           |
| `devices.py`     | Handles `connect` and device-specific routing behavior.                                                               |
| `lists.py`       | Implements list operations: `add`, `delete`, list literals.                                                           |
| `operators.py`   | Processes all binary/unary operations and casting logic.                                                              |
| `expressions.py` | Central handling of expression nodes and evaluation.                                                                  |
| `utils.py`       | Shared utility functions used in interpreter execution.                                                               |

---

### `/typechecker/` – Type-checking visitor logic

| File                                                                 | Description                                                                                               |
|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `type_checker.py`                                                    | Main class `TypeCheckingVisitor`. Called before execution to validate types.                              |
| Other files (e.g. `flowcontrol.py`, `functions.py`, `devices.py`...) | Mirror the structure of `/interpreter/`. Each file handles the same logic but statically validates types. |
| `utils.py`                                                           | Additional utility functions used only by the `TypeCheckingVisitor`                                       |

---

### `/shared/model/` – Core domain models

| File                                                         | Description                                       |
|--------------------------------------------------------------|---------------------------------------------------|
| `Host.py`, `Switch.py`, `Router.py`, `Device.py`             | Represent network devices.                        |
| `Port.py`, `CopperEthernetPort.py`, `OpticalEthernetPort.py` | Represent physical ports.                         |
| `CIDR.py`, `IPAddress.py`, `MACAddress.py`                   | Represent address-related objects and validation. |
| `Packet.py`                                                  | Structure of an IP packet used for delivery.      |
| `RoutingEntry.py`                                            | Object used in routers’ routing tables.           |
| `Connection.py`                                              | Defines physical connections between ports.       |
| `Scope.py`, `Function.py`, `Variable.py`                     | Runtime containers for interpreter state.         |
| `ReturnValue.py`                                             | Signal for returning values from functions.       |
| `base.py`                                                    | Base class for typed objects.                     |

---

### `/shared/utils/`

| File         | Description                                          |
|--------------|------------------------------------------------------|
| `types.py`   | Defines subtyping and type compatibility checks.     |
| `errors.py`  | Contains all custom interpreter/runtime/type errors. |
| `scopes.py`  | Stack-based scope resolution logic.                  |
| `logging.py` | Helpers for structured logging and debug output.     |

---

### `/generated/` – Files generated by ANTLR

| File                                      | Description                                                     |
|-------------------------------------------|-----------------------------------------------------------------|
| `NetLangLexer.py`, `NetLangParser.py`     | Lexer/parser generated from `NetLang.g4`.                       |
| `NetLangListener.py`, `NetLangVisitor.py` | Base classes for listener/visitor logic.                        |
| `.tokens`, `.interp` files                | Internal files used for ANTLR interpreter and token management. |

---

### `/programs/` – Program testing system

| Subfolder | Description                                                      |
|-----------|------------------------------------------------------------------|
| `source/` | Contains test `.netlang` programs organized by number.           |
| `output/` | Expected `.txt` outputs for each test, used by `test_runner.py`. |

---

### `/docs/` – Documentation

| File              | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `installation.md` | Instructions for installing and running the interpreter.     |
| `grammar.md`      | Detailed breakdown of grammar rules defined in `NetLang.g4`. |
| `language.md`     | Complete language reference guide.                           |
| `interpreter.md`  | This file – explains the internal interpreter structure.     |
| `examples.md`     | Sample programs with explanations.                           |

---

### `/images/`
Contains icon files (PNG) used in the network visualization module (e.g. `host.png`, `router.png`, `switch.png`, `packet.png`). These icons are rendered using **PyGame** during packet transmission animation.

### `/fonts/`
Contains the `OpenSans-Regular.ttf` font used for rendering labels and messages in the visual simulation window.

### `test_runner.py`
Custom test runner used to verify the correctness of `.netlang` test files.
- Loads test programs from `programs/source/`
- Compares output to `programs/output/`
- Reports pass/fail/missing statuses
- Useful for regression testing and continuous integration

## 🧪 Interpreter Flow Summary

1. The program is parsed using ANTLR (`NetLang.g4`) into a syntax tree.
2. `TypeCheckingVisitor` validates the entire AST.
3. If type checking passes, `Interpreter` executes the AST.
4. Visualization and packet forwarding is rendered using PyGame and NetworkX.

---