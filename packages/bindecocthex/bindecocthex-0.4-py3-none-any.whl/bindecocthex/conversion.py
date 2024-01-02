class Conversion:
    def init(self):
        pass

    def decimal_to_binary(self, number):
        try:
            decimal_number = int(number)
            binary_representation = format(decimal_number, 'b')
            return binary_representation
        except ValueError:
            return "Invalid input"

    def decimal_to_octal(self, number):
        try:
            decimal_number = int(number)
            octal_representation = format(decimal_number, 'o')
            return octal_representation
        except ValueError:
            return "Invalid input"

    def decimal_to_hexadecimal(self, number):
        try:
            decimal_number = int(number)
            hexadecimal_representation = format(decimal_number, 'X')
            return hexadecimal_representation
        except ValueError:
            return "Invalid input"

    def binary_to_decimal(self, number):
        try:
            decimal_number = int(number, 2)
            return str(decimal_number)
        except ValueError:
            return "Invalid input"

    def binary_to_octal(self, number):
        try:
            decimal_number = int(number, 2)
            octal_representation = format(decimal_number, 'o')
            return octal_representation
        except ValueError:
            return "Invalid input"

    def binary_to_hexadecimal(self, number):
        try:
            decimal_number = int(number, 2)
            hexadecimal_representation = format(decimal_number, 'X')
            return hexadecimal_representation
        except ValueError:
            return "Invalid input"

    def octal_to_decimal(self, number):
        try:
            decimal_number = int(number, 8)
            return str(decimal_number)
        except ValueError:
            return "Invalid input"

    def octal_to_binary(self, number):
        try:
            decimal_number = int(number, 8)
            binary_representation = format(decimal_number, 'b')
            return binary_representation
        except ValueError:
            return "Invalid input"

    def octal_to_hexadecimal(self, number):
        try:
            decimal_number = int(number, 8)
            hexadecimal_representation = format(decimal_number, 'X')
            return hexadecimal_representation
        except ValueError:
            return "Invalid input"

    def hexadecimal_to_decimal(self, number):
        try:
            decimal_number = int(number, 16)
            return str(decimal_number)
        except ValueError:
            return "Invalid input"

    def hexadecimal_to_binary(self, number):
        try:
            decimal_number = int(number, 16)
            binary_representation = format(decimal_number, 'b')
            return binary_representation
        except ValueError:
            return "Invalid input"

    def hexadecimal_to_octal(self, number):
        try:
            decimal_number = int(number, 16)
            octal_representation = format(decimal_number, 'o')
            return octal_representation
        except ValueError:
            return "Invalid input"