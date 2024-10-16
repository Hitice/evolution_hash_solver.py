# Hash Evolution Solver

Hash Evolution Solver is an experimental project that attempts to solve 32-bit hashes using non-standard mathematical formulas. Unlike traditional hash-solving techniques using cryptographic hash functions like SHA-256, this project explores evolving mathematical formulas via evolutionary algorithms and multi-core processing over millions of iterations.

## Features

- Explore non-standard mathematical formulas to generate hash-like values.
- Uses evolutionary algorithms to "evolve" formulas that approximate a target hash.
- Parallel processing support using multiple CPU cores for faster computations.
- Progress tracking with a visual progress bar using `tqdm`.

## How it Works

1. **Random Formula Population**: The program begins with a randomly generated population of formulas, each represented as a tuple of (input, formula_index).
2. **Hash Calculation**: Each formula in the population is applied to an input value, and a hash-like value is calculated.
3. **Evolution**: Over many generations, formulas are mutated and selected based on their proximity to the target hash.
4. **Termination**: The program continues to evolve formulas until the target hash is found or a defined maximum number of iterations is reached.

This program provides a unique approach to solving user-provided 32-bit hashes through experimentation rather than traditional cryptographic functions.

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
