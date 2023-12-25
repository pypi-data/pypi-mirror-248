# XValidator

`xvalidator` is a simple Python package for validation. It includes a module for validating Iran National Codes.

## Installation

You can install `xvalidator` using pip:

```bash
pip install xvalidator
```

## Iran National Code Validation
The package provides a function is_nationalcode for validating Iran National Codes. The function takes a string representing the National Code and returns True if the code is valid and False otherwise.

```py
from xvalidator import is_nationalcode

# Validate Iran National Code
result = is_nationalcode('1234567890')

if result:
    print("Valid National Code")
else:
    print("Invalid National Code")
```

## Contributing
Contributions are welcome! If you find issues or have improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.