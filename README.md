# Propositional Logic Proof Verifier

This project implements a simple logic engine in Python to evaluate and verify propositional logic formulas. It supports logical constructs like variables, implication, conjunction, disjunction, and negation, and allows verification of formal proofs using axioms and the **Modus Ponens** inference rule.

## Features

- Logical formula representation using classes:
  - `Variable`, `Implies`, `And`, `Or`, `Not`
- Evaluation of logical formulas under a truth assignment (environment)
- Recognition of formulas derived from three common axiom schemas
- Application of Modus Ponens
- Proof verification based on assumptions and inference steps

## Logical Inference

### Axiom Schemes

1. Axiom 1: `A → (B → A)`
2. Axiom 2: `(A → (B → C)) → ((A → B) → (A → C))`
3. Axiom 3: `(¬B → ¬A) → ((¬B → A) → B)`

### Inference Rule

- **Modus Ponens (MP)**: From `A` and `A → B`, infer `B`.

## Project Structure

- `Formula`: Base class for all formulas; provides methods like `modus_ponens`, `is_axiom`, `evaluate`, etc.
- `Variable`, `Implies`, `And`, `Or`, `Not`: Subclasses of `Formula` that represent specific logical operations.
- `Proof`: Represents a proof consisting of assumptions and a sequence of formulas. The `verify()` method checks whether the proof is valid.
- Test cases are defined at the end of the file to validate different proof scenarios.

## Usage

Run the Python file to see the result of predefined test cases:

```bash
python your_file_name.py
