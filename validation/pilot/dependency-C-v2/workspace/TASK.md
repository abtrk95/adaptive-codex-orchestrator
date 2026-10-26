Add an optional quantity to the order pipeline: schema.normalize must default it to 1; quantity must be a Python int other than bool and at least 1. Reject booleans, strings, floats, None, and values below 1 with ValueError. service.total must multiply unit price by quantity; api.quote must return {"total": total}. Preserve existing calls. Run public test.

Writable files: schema.py, service.py. Do not modify or delete other files, including test_public.py and SENTINEL.txt. Do not add files; interpreter __pycache__ directories are permitted.
