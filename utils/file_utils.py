''' Contains utility functions for file manipulation/analytics '''

from typing import AnyStr
import filecmp
import time


def is_same(filename1: AnyStr, filename2: AnyStr) -> bool:
    '''Check whether two files are equivalent'''
    return filecmp.cmp(filename1, filename2)


def function_timer(func):
    def wrapper_function(*args, **kwargs):
        t1 = time.time()
        func(*args,  **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
    return wrapper_function