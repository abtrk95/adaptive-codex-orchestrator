def parse(item):
    value = item["value"].strip()
    digits = value[1:] if value.startswith("-") else value
    if not digits or any(char < "0" or char > "9" for char in digits):
        raise ValueError("invalid decimal value")
    return int(value)
