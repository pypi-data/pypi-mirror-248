# TuringMachine

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Run any Turing machine possible using this function and see if the turing machine, accepts or rejects the tape yu input to it.

## Installation

```bash
pip install turing-machine-utils
```

## Usage

```python
from turing_machine_utils import create_turing_machine

# Define Turing Machine states, alphabet, and transition rules
states = ['q0', 'q1', 'accept', 'discard']
transition_rules = {
    ('q0', '0'): ('q1', '1', 'R'),
    ('q0', '1'): ('q0', '0', 'R'),
    ('q1', '0'): ('accept', '0', 'L'),
    ('q1', '1'): ('discard', '1', 'L'),
}

# Define the input tape
tape = ['0', '1', '0', '1', '0']

# Run the Turing Machine
result, new_tape = create_turing_machine(tape, states, transition_rules)
print("Result:", result)
```

The result will be:
1. 1 if the tape is accepted by the turing machine
1. -1 if the state is discarded by the turing machine
1. 0 if an undefined transition is found by the turing machine

The new_tape is the tape with the changes to the original tape

## Configuration

No specific configuration options are available at the moment.

## Contributing

Feel free to contribute by reporting issues, suggesting improvements, or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.md) file for details.