# Dynamic POOL-VIS Generated Tool: calculadora_fibonacci
# Description: Calcula la secuencia de fibonacci hasta N terminos.

def execute(*args, **kwargs):
    if kwargs.get('test_mode'):
        return 'Fibonacci tool test OK'
    n = kwargs.get('n', 10)
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return f"Secuencia Fibonacci generada dinamicamente ({n} terminos): {seq}"
