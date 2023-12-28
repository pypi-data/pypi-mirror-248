from sys import argv 
from typing import Callable

from .runner import run


def command(func: Callable):
    """
    Command Decorator
    -----------------
    
    Use by putting this on top of any function.
        ```python
        @command
        def myfunc(x, y = 56):
            ...
        ```
    """
    
    if "--upycli.debug" in argv:
        print(f"Debug: Arguments `{argv}`")
        
    if func.__name__ in argv:
        run(func)
        exit(0)
    