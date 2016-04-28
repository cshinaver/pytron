#!/usr/bin/python
# utils.py
# Useful functions


def apply_fn(f, coll):
    """
    Applies f to each argument of coll.
    For applying side effects.
    """
    for i in coll:
        f(i)
