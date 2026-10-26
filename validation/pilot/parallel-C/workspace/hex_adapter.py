def parse(item):
    value = item['value'].strip()
    digits = value[1:] if value.startswith('-') else value
    if not digits or any(char not in '0123456789abcdefABCDEF' for char in digits):
        raise ValueError('invalid hexadecimal value')
    return int(value, 16)
