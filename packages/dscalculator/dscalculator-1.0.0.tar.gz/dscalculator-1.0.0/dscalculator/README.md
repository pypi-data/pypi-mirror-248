# dscalculator Package

This package provides a Calculator class to handle simple mathematical operations building upon Calculator's memory value which, upon initialization, is equal to 0.

## Installation

```sh
pip install dscalculator
```

## Usage

Add one or more numbers to the calculator's memorised value:

```python
>>> from dscalculator.calculator import Calculator
>>> calcul = Calculator()
>>> calcul.memorised_value
0.0
>>> calcul.add(3, 2, 5)
10.0

Take n root of the calculator's memorised value:

```python
>>> from dscalculator.calculator import Calculator
>>> calcul = Calculator()
>>> calcul.add(64)
>>> calcul.root_n(2)
8.0
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

The package includes test module named "test_calculator.py" - make sure to add or update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Testing

Run unit tests to test main use cases and some edge cases:
pytest dscalculator/test_calculator.py