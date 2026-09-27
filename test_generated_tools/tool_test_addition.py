# Dynamic POOL-VIS Generated Tool: test_addition
# Description: Adds two numbers

def execute(*args, **kwargs):
    if kwargs.get('test_mode'):
        return 'Test add OK'
    a = kwargs.get('a', 0)
    b = kwargs.get('b', 0)
    return a + b
