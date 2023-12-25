def is_nationalcode(code):
    """
    Validate Iran National Code.

    Parameters:
    - code (str): The Iran National Code to validate.

    Returns:
    - bool: True if the code is valid, False otherwise.
    """
    if not code or not isinstance(code, str) or not code.isdigit() or len(code) != 10:
        return False

    checksum = int(code[9])
    code_digits = [int(digit) for digit in code[:9]]

    calculated_checksum = sum((i + 2) * code_digits[i] for i in range(9)) % 11
    calculated_checksum = 11 - calculated_checksum if calculated_checksum >= 2 else calculated_checksum

    return calculated_checksum == checksum