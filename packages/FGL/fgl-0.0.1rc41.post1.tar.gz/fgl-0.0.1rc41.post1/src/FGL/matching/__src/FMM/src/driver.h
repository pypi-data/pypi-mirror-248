#ifndef kece_wrapper_h
#define kece_wrapper_h
#include <Python.h>
void match(PyObject *edge_list, PyObject *matching, PyObject *result);
void match_track(PyObject *edge_list, PyObject *paths, PyObject *trees, PyObject *dead, PyObject *paths_sizes, PyObject *trees_sizes, PyObject *dead_sizes, PyObject *matching, PyObject *result);
#endif