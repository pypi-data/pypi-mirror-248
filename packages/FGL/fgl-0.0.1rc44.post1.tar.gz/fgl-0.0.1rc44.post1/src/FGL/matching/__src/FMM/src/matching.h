/*
 * matching.h -- Maximum cardinality matching definitions
 */

/*
 * Copyright 1996 by John Kececioglu
 */

#ifndef MatchingInclude
#define MatchingInclude

#include "list.h"
#include "graph.h"

extern List *MaximumCardinalityMatchingTrack Proto((Graph * G, PyObject *paths, PyObject *trees, PyObject *dead, PyObject *paths_sizes, PyObject *trees_sizes, PyObject *dead_sizes));
extern List *MaximumCardinalityMatching Proto((Graph * G));
extern List *MaximalMatching Proto((Graph * G));

#endif /* MatchingInclude */
