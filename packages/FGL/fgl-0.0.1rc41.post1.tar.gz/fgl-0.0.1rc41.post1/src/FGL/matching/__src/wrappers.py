from .. import __lib
import networkx
import scipy
import copy
from typing import Optional
# This file contains python wrappers for our C functions.
# The whole purpose of that is to make it easier for
# auto-completions to know our function definitions.

# __lib is the compiled library containing our c functions.

def max_cardinality_matching(rows, cols, matching):
    return __lib.match_wrapper(rows, cols, matching)

def max_cardinality_matching(G: networkx.Graph, init_list: Optional[list] = []):
    edge_list = list(G.edges)
    result_matching = []
    __lib.match_wrapper(edge_list, init_list, result_matching)
    return copy.deepcopy(result_matching)


def max_cardinality_matching_track(G: networkx.Graph, paths: list, trees: list, dead: list, \
                                   path_sizes: list, tree_sizes: list, dead_sizes: list, init_list: Optional[list] = []):
    edge_list = list(G.edges)
    result_matching = []
    __lib.match_track_wrapper(edge_list, paths, trees, dead, path_sizes, tree_sizes, dead_sizes, init_list, result_matching)
    return copy.deepcopy(result_matching)