#include <Python.h>
#include "structmember.h"

#include "client.h"

typedef struct {
    PyObject_HEAD
    PyObject* body;
    PyObject* headers;
    long status;
} PyResponse;

void PyResponse_dealloc(PyResponse* self) {
    Py_XDECREF(self->body);
    Py_XDECREF(self->headers);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

int PyResponse_init(PyResponse* self, PyObject* args, PyObject* kwds) {
    PyObject* body = NULL;
    PyObject* headers = NULL;
    long status = 0;

    static char* kwlist[] = {"body", "headers", "status", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOl", kwlist, &body, &headers, &status)) {
        return -1;
    }

    Py_XINCREF(body);
    Py_XINCREF(headers);

    self->body = body;
    self->headers = headers;
    self->status = status;

    return 0;
}

PyObject* PyResponse_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    PyResponse* self;

    self = (PyResponse*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->body = NULL;
        self->headers = NULL;
        self->status = 0;
    }

    return (PyObject*)self;
}

PyMemberDef PyResponse_members[] = {
    {"body", T_OBJECT_EX, offsetof(PyResponse, body), 0, "Response body"},
    {"headers", T_OBJECT_EX, offsetof(PyResponse, headers), 0, "Response headers"},
    {"status", T_LONG, offsetof(PyResponse, status), 0, "HTTP status code"},
    {NULL}
};

PyTypeObject PyResponseType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "recuests.Response",
    .tp_basicsize = sizeof(PyResponse),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor)PyResponse_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_members = PyResponse_members,
    .tp_new = PyResponse_new,
    .tp_init = (initproc)PyResponse_init,
};

void HashmapToDict(void* key, size_t ksize, uintptr_t value, void* userdata) {
    PyObject* pyKey = Py_BuildValue("s", key);
    PyObject* pyValue = Py_BuildValue("s", (char*)value);

    PyDict_SetItem((PyObject*)userdata, pyKey, pyValue);
}

PyObject* Py_RequestGET(PyObject* self, PyObject* args) {
    char* url;
    PyObject* headersObj = Py_None;

    if (!PyArg_ParseTuple(args, "s|O", &url, &headersObj)) {
        return NULL;
    }

    if (headersObj != Py_None && !PyDict_Check(headersObj)) {
        PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary.");
        return NULL;
    }

    HTTPHeader* headers = NULL;
    Py_ssize_t numHeaders = 0;
    if (headersObj != Py_None)
        numHeaders = PyDict_Size(headersObj);

    if (headersObj != Py_None && numHeaders > 0) {
        PyObject* key;
        PyObject* value;
        Py_ssize_t pos = 0;
        size_t i = 0;

        headers = malloc(sizeof(HTTPHeader) * numHeaders);

        while (PyDict_Next(headersObj, &pos, &key, &value)) {
            if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
                PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary of strings.");
                return NULL;
            }

            const char* keyStr = PyUnicode_AsUTF8(key);
            const char* valueStr = PyUnicode_AsUTF8(value);

            headers[i].key = malloc(sizeof(char) * (strlen(keyStr) + 1));
            headers[i].value = malloc(sizeof(char) * (strlen(valueStr) + 1));

            if (headers[i].key == NULL || headers[i].value == NULL) {
                PyErr_SetString(PyExc_MemoryError, "malloc() failed for key or value.");
                return NULL;
            }

            strcpy(headers[i].key, keyStr);
            strcpy(headers[i].value, valueStr);

            i++;
        }
    }

    Response res = RequestGET(url, headers);

    if (headers != NULL) {
        for (size_t i = 0; i < (size_t)numHeaders; i++) {
            free(headers[i].key);
            free(headers[i].value);
        }
        free(headers);
    }

    if (PyType_Ready(&PyResponseType) < 0) {
        FreeResponse(&res);
        PyErr_Print();
        return Py_None;
    }

    PyResponse* pyRes = (PyResponse*)PyResponseType.tp_alloc(&PyResponseType, 0);
    if (pyRes == NULL) {
        PyErr_SetString(PyExc_MemoryError, "malloc() failed for response.");
        return NULL;
    }

    PyObject* pyHeaders = PyDict_New();
    hashmap_iterate(res.headers, HashmapToDict, pyHeaders);
    if (res.body != NULL)
        pyRes->body = PyBytes_FromString(res.body);
    else
        pyRes->body = Py_None;

    if (res.headers != NULL)
        pyRes->headers = pyHeaders;
    else
        pyRes->headers = Py_None;

    pyRes->status = res.status;
    FreeResponse(&res);

    return (PyObject*)pyRes;
}

PyObject* Py_RequestPOST(PyObject* self, PyObject* args) {
    char* url;
    PyObject* headersObj = Py_None;
    char* reqBody;

    if (!PyArg_ParseTuple(args, "s|Os", &url, &headersObj, &reqBody)) {
        return NULL;
    }

    if (headersObj != Py_None && !PyDict_Check(headersObj)) {
        PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary.");
        return NULL;
    }

    HTTPHeader* headers = NULL;
    Py_ssize_t numHeaders = 0;
    if (headersObj != Py_None)
        numHeaders = PyDict_Size(headersObj);

    if (headersObj != Py_None && numHeaders > 0) {
        PyObject* key;
        PyObject* value;
        Py_ssize_t pos = 0;
        size_t i = 0;

        headers = malloc(sizeof(HTTPHeader) * numHeaders);

        while (PyDict_Next(headersObj, &pos, &key, &value)) {
            if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
                PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary of strings.");
                return NULL;
            }

            const char* keyStr = PyUnicode_AsUTF8(key);
            const char* valueStr = PyUnicode_AsUTF8(value);

            headers[i].key = malloc(sizeof(char) * (strlen(keyStr) + 1));
            headers[i].value = malloc(sizeof(char) * (strlen(valueStr) + 1));

            if (headers[i].key == NULL || headers[i].value == NULL) {
                PyErr_SetString(PyExc_MemoryError, "malloc() failed for key or value.");
                return NULL;
            }

            strcpy(headers[i].key, keyStr);
            strcpy(headers[i].value, valueStr);

            i++;
        }
    }

    Response res = RequestPOST(url, headers, reqBody);

    if (headers != NULL) {
        for (size_t i = 0; i < (size_t)numHeaders; i++) {
            free(headers[i].key);
            free(headers[i].value);
        }
        free(headers);
    }

    if (PyType_Ready(&PyResponseType) < 0) {
        FreeResponse(&res);
        PyErr_Print();
        return Py_None;
    }

    PyResponse* pyRes = (PyResponse*)PyResponseType.tp_alloc(&PyResponseType, 0);
    if (pyRes == NULL) {
        PyErr_SetString(PyExc_MemoryError, "malloc() failed for response.");
        return NULL;
    }

    PyObject* pyHeaders = PyDict_New();
    hashmap_iterate(res.headers, HashmapToDict, pyHeaders);
    if (res.body != NULL)
        pyRes->body = PyBytes_FromString(res.body);
    else
        pyRes->body = Py_None;

    if (res.headers != NULL)
        pyRes->headers = pyHeaders;
    else
        pyRes->headers = Py_None;

    pyRes->status = res.status;
    FreeResponse(&res);

    return (PyObject*)pyRes;
}

PyObject* Py_RequestPUT(PyObject* self, PyObject* args) {
    char* url;
    PyObject* headersObj = Py_None;
    char* reqBody;

    if (!PyArg_ParseTuple(args, "s|Os", &url, &headersObj, &reqBody)) {
        return NULL;
    }

    if (headersObj != Py_None && !PyDict_Check(headersObj)) {
        PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary.");
        return NULL;
    }

    HTTPHeader* headers = NULL;
    Py_ssize_t numHeaders = 0;
    if (headersObj != Py_None)
        numHeaders = PyDict_Size(headersObj);

    if (headersObj != Py_None && numHeaders > 0) {
        PyObject* key;
        PyObject* value;
        Py_ssize_t pos = 0;
        size_t i = 0;

        headers = malloc(sizeof(HTTPHeader) * numHeaders);

        while (PyDict_Next(headersObj, &pos, &key, &value)) {
            if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
                PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary of strings.");
                return NULL;
            }

            const char* keyStr = PyUnicode_AsUTF8(key);
            const char* valueStr = PyUnicode_AsUTF8(value);

            headers[i].key = malloc(sizeof(char) * (strlen(keyStr) + 1));
            headers[i].value = malloc(sizeof(char) * (strlen(valueStr) + 1));

            if (headers[i].key == NULL || headers[i].value == NULL) {
                PyErr_SetString(PyExc_MemoryError, "malloc() failed for key or value.");
                return NULL;
            }

            strcpy(headers[i].key, keyStr);
            strcpy(headers[i].value, valueStr);

            i++;
        }
    }

    Response res = RequestPOST(url, headers, reqBody);

    if (headers != NULL) {
        for (size_t i = 0; i < (size_t)numHeaders; i++) {
            free(headers[i].key);
            free(headers[i].value);
        }
        free(headers);
    }

    if (PyType_Ready(&PyResponseType) < 0) {
        FreeResponse(&res);
        PyErr_Print();
        return Py_None;
    }

    PyResponse* pyRes = (PyResponse*)PyResponseType.tp_alloc(&PyResponseType, 0);
    if (pyRes == NULL) {
        PyErr_SetString(PyExc_MemoryError, "malloc() failed for response.");
        return NULL;
    }

    PyObject* pyHeaders = PyDict_New();
    hashmap_iterate(res.headers, HashmapToDict, pyHeaders);
    if (res.body != NULL)
        pyRes->body = PyBytes_FromString(res.body);
    else
        pyRes->body = Py_None;

    if (res.headers != NULL)
        pyRes->headers = pyHeaders;
    else
        pyRes->headers = Py_None;

    pyRes->status = res.status;
    FreeResponse(&res);

    return (PyObject*)pyRes;
}

PyObject* Py_RequestDELETE(PyObject* self, PyObject* args) {
    char* url;
    PyObject* headersObj = Py_None;

    if (!PyArg_ParseTuple(args, "s|O", &url, &headersObj)) {
        return NULL;
    }

    if (headersObj != Py_None && !PyDict_Check(headersObj)) {
        PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary.");
        return NULL;
    }

    HTTPHeader* headers = NULL;
    Py_ssize_t numHeaders = 0;
    if (headersObj != Py_None)
        numHeaders = PyDict_Size(headersObj);

    if (headersObj != Py_None && numHeaders > 0) {
        PyObject* key;
        PyObject* value;
        Py_ssize_t pos = 0;
        size_t i = 0;

        headers = malloc(sizeof(HTTPHeader) * numHeaders);

        while (PyDict_Next(headersObj, &pos, &key, &value)) {
            if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
                PyErr_SetString(PyExc_TypeError, "Headers must be a dictionary of strings.");
                return NULL;
            }

            const char* keyStr = PyUnicode_AsUTF8(key);
            const char* valueStr = PyUnicode_AsUTF8(value);

            headers[i].key = malloc(sizeof(char) * (strlen(keyStr) + 1));
            headers[i].value = malloc(sizeof(char) * (strlen(valueStr) + 1));

            if (headers[i].key == NULL || headers[i].value == NULL) {
                PyErr_SetString(PyExc_MemoryError, "malloc() failed for key or value.");
                return NULL;
            }

            strcpy(headers[i].key, keyStr);
            strcpy(headers[i].value, valueStr);

            i++;
        }
    }

    Response res = RequestGET(url, headers);

    if (headers != NULL) {
        for (size_t i = 0; i < (size_t)numHeaders; i++) {
            free(headers[i].key);
            free(headers[i].value);
        }
        free(headers);
    }

    if (PyType_Ready(&PyResponseType) < 0) {
        FreeResponse(&res);
        PyErr_Print();
        return Py_None;
    }

    PyResponse* pyRes = (PyResponse*)PyResponseType.tp_alloc(&PyResponseType, 0);
    if (pyRes == NULL) {
        PyErr_SetString(PyExc_MemoryError, "malloc() failed for response.");
        return NULL;
    }

    PyObject* pyHeaders = PyDict_New();
    hashmap_iterate(res.headers, HashmapToDict, pyHeaders);
    if (res.body != NULL)
        pyRes->body = PyBytes_FromString(res.body);
    else
        pyRes->body = Py_None;

    if (res.headers != NULL)
        pyRes->headers = pyHeaders;
    else
        pyRes->headers = Py_None;

    pyRes->status = res.status;
    FreeResponse(&res);

    return (PyObject*)pyRes;
}