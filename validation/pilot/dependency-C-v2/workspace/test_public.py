from api import quote
assert quote({"price": 5, "quantity": 3}) == {"total": 15}
