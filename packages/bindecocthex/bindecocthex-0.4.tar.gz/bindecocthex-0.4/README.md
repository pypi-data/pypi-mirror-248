# bindecocthex

`bindecocthex` is a Python library that provides a `Conversion` class for converting numbers between decimal, binary, octal, and hexadecimal representations.

## Installation

You can install `bindecocthex` using pip:

```
pip install bindecocthex
```
## Usage
```
from bindecocthex.conversion import Conversion

# Create an instance of the Conversion class
converter = Conversion()

# Example usage
decimal_number = 10

# Decimal to Binary
binary_representation = converter.decimal_to_binary(decimal_number)
print(f"Binary representation: {binary_representation}")

# Binary to Decimal
decimal_result = converter.binary_to_decimal(binary_representation)
print(f"Decimal result: {decimal_result}")

```
## Methods
- `decimal_to_binary(number)`
Converts a decimal number to binary.

- `decimal_to_octal(number)`
Converts a decimal number to octal.

- `decimal_to_hexadecimal(number)`
Converts a decimal number to hexadecimal.

- `binary_to_decimal(number)`
Converts a binary number to decimal.

- `binary_to_octal(number)`
Converts a binary number to octal.

- `binary_to_hexadecimal(number)`
Converts a binary number to hexadecimal.

- `octal_to_decimal(number)`
Converts an octal number to decimal.

- `octal_to_binary(number)`
Converts an octal number to binary.

- `octal_to_hexadecimal(number)`
Converts an octal number to hexadecimal.

- `hexadecimal_to_decimal(number)`
Converts a hexadecimal number to decimal.

- `hexadecimal_to_binary(number)`
Converts a hexadecimal number to binary.

- `hexadecimal_to_octal(number)`
Converts a hexadecimal number to octal.

## License
This project is licensed under the [MIT License](LICENSE).
