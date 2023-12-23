#ifndef MATCH_WRAPPER_H
#define MATCH_WRAPPER_H

// Always include Python.h in the very first line in all header files.
#include <Python.h>

PyObject *match_wrapper(PyObject *self, PyObject *args);
PyObject *match_track_wrapper(PyObject *self, PyObject *args);

#endif
