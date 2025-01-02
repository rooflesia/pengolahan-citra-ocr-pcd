import re

def validate_plate_number(plate_text):
    """
    Validasi format plat nomor Indonesia.
    Format umum: B 1234 XYZ
    """
    pattern = r'^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{1,3}$'
    if re.match(pattern, plate_text):
        return True
    return False


if __name__ == "__main__":
    test_plates = ["B 1234 XYZ", "123 ABC", "D 5678 AB", "INVALID"]
    for plate in test_plates:
        is_valid = validate_plate_number(plate)
        print(f"Plat nomor '{plate}' valid: {is_valid}")
