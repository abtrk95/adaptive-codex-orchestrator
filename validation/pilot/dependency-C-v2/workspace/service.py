from schema import normalize


def total(order):
    normalized = normalize(order)
    return normalized["price"] * normalized["quantity"]
