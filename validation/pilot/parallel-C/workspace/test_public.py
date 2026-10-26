from dispatcher import parse
assert parse("decimal", {"value":"13"}) == 13
assert parse("hex", {"value":"a"}) == 10
assert parse("binary", {"value":"11"}) == 3
