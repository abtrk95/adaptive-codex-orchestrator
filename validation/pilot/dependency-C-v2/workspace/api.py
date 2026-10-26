from service import total
def quote(order):
    return {"total": total(order)}
