import decimal_adapter, hex_adapter, binary_adapter
def parse(kind, item):
    return {"decimal": decimal_adapter.parse, "hex": hex_adapter.parse, "binary": binary_adapter.parse}[kind](item)
