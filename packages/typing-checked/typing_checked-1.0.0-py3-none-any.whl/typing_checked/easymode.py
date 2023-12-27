def check(value, typehint):
    if type(value) is typehint:
        raise TypeError(value)