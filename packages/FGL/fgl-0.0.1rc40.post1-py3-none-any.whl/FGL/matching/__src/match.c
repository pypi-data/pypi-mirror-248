// In all C files, include its corresponding header file in the very first line.
// No need to include <Python.h> as we did that already in the header file.
// Just make sure that <Python.h> is included BEFORE any other header file.
#include "match.h"
#include "FMM/src/driver.h"

// Our function implementation
// Our modified function implementation to accept two lists
PyObject *match_wrapper(PyObject *self, PyObject *args)
{
    PyObject *list1;
    PyObject *list2;
    PyObject *list3;

    // Parse the input arguments, expecting two lists of integers
    if (!PyArg_ParseTuple(args, "OOO", &list1, &list2, &list3))
    {
        return NULL;
    }

    // Check if the input is a list
    if (!PyList_Check(list1) || !PyList_Check(list2) || !PyList_Check(list3))
    {
        PyErr_SetString(PyExc_TypeError, "All inputs must be lists");
        return NULL;
    }

    // return match(list1, list2);
    match(list1, list2, list3);
    // return list4;
    Py_RETURN_NONE;
}

PyObject *match_track_wrapper(PyObject *self, PyObject *args)
{
    PyObject *list1;
    PyObject *list2;
    PyObject *list3;
    PyObject *list4;
    PyObject *list5;
    PyObject *list6;
    PyObject *list7;
    PyObject *list8;
    PyObject *list9;
    // Parse the input arguments, expecting two lists of integers
    if (!PyArg_ParseTuple(args, "OOOOOOOOO", &list1, &list2, &list3, &list4, &list5, &list6, &list7, &list8, &list9))
    {
        return NULL;
    }

    // Check if the input is a list
    if (!PyList_Check(list1) || !PyList_Check(list2) || !PyList_Check(list3))
    {
        PyErr_SetString(PyExc_TypeError, "All inputs must be lists");
        return NULL;
    }

    // return match(list1, list2);
    match_track(list1, list2, list3, list4, list5, list6, list7, list8, list9);
    // return list4;
    Py_RETURN_NONE;
}
