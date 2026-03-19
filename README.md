# Resistor Approximator

A tool that finds the smallest combination of resistors (or capacitors/inductors) from your available components that achieves a target value within a specified tolerance. It automatically determines the best configuration — series, parallel, or a mix of both.

Built for electrical engineering students who need to quickly find the right combination of components in circuit labs, without wasting time on trial and error.

## How It Works

Given a list of available component values and a target, the solver:

1. Tries subsets of increasing size (fewest components first)
2. For each subset, evaluates all possible topologies — pure series, pure parallel, and mixed series-parallel configurations
3. Returns the smallest subset and topology that hits the target within tolerance, with the lowest error

For small subsets (up to 4 components), it exhaustively searches all possible binary-tree circuit topologies. For larger subsets, it uses a hybrid approach that searches 2-partition mixed topologies while keeping computation fast.

## Features

- Supports SI prefix notation: `1k`, `4.7M`, `100n`, `2.2u`
- Multiplier shorthand: `1kx5` expands to five 1k resistors
- Handles resistors, inductors, and capacitors (with correct series/parallel formulas)
- Auto-detects optimal configuration (series, parallel, or mixed)
- SVG circuit diagram visualization
- Fully client-side — no backend needed, just open `index.html`

## Usage

Open `index.html` in any browser. Enter your available components (comma-separated), target value, and tolerance. Hit Solve.

Example: components `1k, 2kx5, 4.7k, 10k`, target `15k`, tolerance `5%`.

## Algorithm Credit

The original optimization approach using Mixed Integer Programming was developed by [Michael Jurasovic](https://jurasofish.github.io). His write-up on the algorithm: [Picking Resistors for Parallel and Series Equivalence](https://jurasofish.github.io/picking-resistors-for-parallel-and-series-equivalence.html).

The web version ports and extends this concept to JavaScript with a combinatorial topology search, running entirely client-side.
