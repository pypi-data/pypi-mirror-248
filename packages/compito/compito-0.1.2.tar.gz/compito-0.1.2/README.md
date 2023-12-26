# Compito

This project is a command executor that allows scheduling and execution of commands. It is written in Python and uses the `croniter` library for scheduling.

## Installation

To install the project, you need to have Python 3.12 or higher. You can install the dependencies with the following command:

```bash
pip install compito
```

## Usage/Examples

The project provides a command-line interface for scheduling and executing commands. Here is an example of how to use it:

```bash
python -m compito <command> [options] [args]
```
You can find more examples in [examples](examples) directory.

## Commands
Each command can be scheduled to run at specific intervals using the `Scheduler` class.

## Testing

To run the automated tests for this system, use the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are always welcome! Please feel free to submit a pull request.
