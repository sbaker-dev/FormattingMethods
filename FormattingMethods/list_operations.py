from collections import Counter
from itertools import chain
import sys


def flatten(list_of_lists):
    """
    Flatten a list of lists into a list
    """
    return list(chain(*list_of_lists))


def flip_list(list_of_lists, length_return=False):
    """
    This will take a list of lists, and then flip it. It requires all sub lists to be the same length.
    """

    list_of_keys = Counter([len(sub_list) for sub_list in list_of_lists])
    sub_key_length = list(list_of_keys.keys())

    if len(list_of_keys.keys()) == 1:
        if length_return:
            return [[sub[i] for sub in list_of_lists] for i in range(sub_key_length[0])], sub_key_length[0]
        else:
            return [[sub[i] for sub in list_of_lists] for i in range(sub_key_length[0])]

    else:
        sys.exit(f"Sub lists should be all of the same length yet found lengths {sub_key_length}")

