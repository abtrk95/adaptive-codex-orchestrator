def parse(item):
    value = item["value"].strip()
    digits = value[1:] if value.startswith("-") else value
    if not digits or any(digit not in "01" for digit in digits):
        raise ValueError("Invalid binary value")
    return int(value, 2)
