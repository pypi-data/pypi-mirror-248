from ._simhash import num_differing_bits, compute as c_compute, find_all as c_find_all

import hashlib
import struct

def unsigned_hash(obj):
    '''Returns a hash suitable for use as a hash_t.'''
    # Takes first 8 bytes of MD5 digest
    digest = hashlib.md5(obj).digest()[0:8]
    # Unpacks the binary bytes in digest into a Python integer
    return struct.unpack('>Q', digest)[0] & 0xFFFFFFFFFFFFFFFF

def shingle(tokens, window=4):
    """A generator for a moving window of the provided tokens."""
    if window <= 0:
        raise ValueError("Window size must be positive")

    # Start with an empty output set.
    curr_window = []
    # Iterate over the input tokens, once.
    for token in tokens:
        # Add to the window.
        curr_window.append(token)

        # If we've collected too many, remove the oldest item(s) from the collection
        while len(curr_window) > window:
            curr_window.pop(0)

        # Finally, if the window is full, yield the data set.
        if len(curr_window) == window:
            yield list(curr_window)

def compute(hashes):
    if not isinstance(hashes, list):
       hashes = list(hashes)
    return c_compute(hashes)

def find_all(hashes, number_of_blocks, different_bits):
    if not isinstance(hashes, set):
       hashes = set(hashes)
    return c_find_all(hashes, number_of_blocks, different_bits)