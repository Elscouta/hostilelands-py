from decimal import Decimal

# A list of potentially useful lambda functions to be
# used for requirements description

# --- Comparators
def exact(n):
        return lambda x: x == Decimal(n)

def greater(n):
        return lambda x: x >= Decimal(n)

# --- R -> R functions (conversion of a property value to an effect)
def fixed(n):
    return lambda x: Decimal(n) if (x > 0) else 0

def linear(k):
    return lambda x: Decimal(k)*x

# -- R x R -> R functions (to be used for modified_by)
def add(k):
        return lambda orig, modif: orig + Decimal(k)*modif

def add_transf(transf):
        return lambda orig, modif: orig + transf(modif)

def multiply():
        return lambda orig, modif: orig * modif
