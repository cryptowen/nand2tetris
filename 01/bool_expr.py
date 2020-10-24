from inspect import signature
from itertools import product
from sympy.logic import SOPform
from sympy import symbols

def mux(a, b, sel):
    return a if sel == 0 else b

def func2truth_table(f):
    """
    >>> def _or(a, b): 
    ...     return a or b
    >>> func2truth_table(_or)
    {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}
    >>> func2truth_table(mux)
    {(0, 0, 0): 0, (0, 0, 1): 0, (0, 1, 0): 0, (0, 1, 1): 1, (1, 0, 0): 1, (1, 0, 1): 0, (1, 1, 0): 1, (1, 1, 1): 1}
    """
    d = {}
    sig = signature(f)
    for params in product([0, 1], repeat=len(sig.parameters)):
        d[params] = f(*params)
    return d

def func2expr(f):
    """
    >>> def _or(a, b): 
    ...     return a or b
    >>> func2expr(_or)
    Or(a, b)
    >>> func2expr(mux)
    Or(And(Not(c), a), And(b, c)
    """
    sig = signature(f)
    parameters_len = len(sig.parameters)
    s = symbols('a:z')[:parameters_len]
    minterms = [k for k, v in func2truth_table(f).items() if v ]
    return SOPform(s, minterms)



if __name__ == "__main__":
    import doctest
    doctest.testmod()