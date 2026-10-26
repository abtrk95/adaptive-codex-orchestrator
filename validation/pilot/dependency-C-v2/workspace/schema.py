def normalize(order):
    quantity = order.get("quantity", 1)
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("quantity must be an integer of at least 1")
    return {"price": order["price"], "quantity": quantity}
