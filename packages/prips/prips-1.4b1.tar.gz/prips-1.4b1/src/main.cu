#ifdef _WIN32
#define PLUGIN_API extern "C" __declspec(dllexport)
#elif __linux__
#define PLUGIN_API extern "C"
#endif

#include "common.cuh"
#include "control.cuh"
#include "collective_variable/collective_variable.cuh"
#include "MD_core/MD_core.cuh"
#include "neighbor_list/neighbor_list.cuh"
#include <sstream>

#include "Python.h"

static MD_INFORMATION* md_info = NULL;
static CONTROLLER* controller = NULL;
static COLLECTIVE_VARIABLE_CONTROLLER* cv_controller = NULL;
static NEIGHBOR_LIST* neighbor_list = NULL;
static int is_initialized = 0;


struct SpongeCVObject
{
    PyObject_HEAD
    COLLECTIVE_VARIABLE_PROTOTYPE* cv;
};

static PyObject *SpongeCVNew(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    SpongeCVObject *self;
    self = (SpongeCVObject *) type->tp_alloc(type, 0);
    if (self != NULL)
    {
        self->cv = NULL;
    }
    return (PyObject *) self;
}

static int SpongeCVInit(SpongeCVObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {(char*)"ptr", NULL};
    intptr_t tmp;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "L", kwlist, &tmp))
        return -1;

    self->cv = (COLLECTIVE_VARIABLE_PROTOTYPE*) tmp;

    return 0;
}

static PyObject* SpongeCVGetValue(SpongeCVObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("f", self->cv->value);
}

static PyObject* SpongeCVSetValue(SpongeCVObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {(char*)"value", NULL};
    float value;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "f", kwlist, &value))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    self->cv->value = value;
    
    return Py_BuildValue("");
}

static PyObject* SpongeCVGetLastUpdateStep(SpongeCVObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {(char*)"need", NULL};
    int need;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "i", kwlist, &need))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    return Py_BuildValue("i", self->cv->last_update_step[(COLLECTIVE_VARIABLE_NEED)need]);
}

static PyObject* SpongeCVSetLastUpdateStep(SpongeCVObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {(char*)"need", (char*)"step", NULL};
    int need;
    int step;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii", kwlist, &need, &step))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    for (int i = 1; i <= 8; i <<= 1)
    {
        if (need && i)
            self->cv->last_update_step[(COLLECTIVE_VARIABLE_NEED)i] = step;
    }
    return Py_BuildValue("");
}

static PyObject* SpongeCVGetStream(SpongeCVObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("L", (intptr_t)self->cv->cuda_stream);
}

static PyObject* SpongeCVDeviceValue(SpongeCVObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("((Lizi),i,s)",(intptr_t)self->cv->d_value, sizeof(float), NULL, controller->working_device, 1, "f");
}

static PyObject* SpongeCVCrdGrads(SpongeCVObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)self->cv->crd_grads, sizeof(float) * 3 * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, 3, "f");
}

static PyObject* SpongeCVBoxGrads(SpongeCVObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("((Lizi),i,s)",(intptr_t)self->cv->box_grads, sizeof(float) * 3, NULL, controller->working_device, 3, "f");
}

static PyMethodDef SpongeCVMethods[] = {
    {"_get_value", (PyCFunction)SpongeCVGetValue, METH_NOARGS, ""},
    {"_set_value", (PyCFunction)SpongeCVSetValue, METH_VARARGS|METH_KEYWORDS, ""},
    {"_get_last_update_step", (PyCFunction)SpongeCVGetLastUpdateStep, METH_VARARGS|METH_KEYWORDS, ""},
    {"_set_last_update_step", (PyCFunction)SpongeCVSetLastUpdateStep, METH_VARARGS|METH_KEYWORDS, ""},
    {"_get_cuda_stream", (PyCFunction)SpongeCVGetStream, METH_NOARGS, ""},
    {"_d_value", (PyCFunction)SpongeCVDeviceValue, METH_NOARGS, ""},
    {"_crd_grads", (PyCFunction)SpongeCVCrdGrads, METH_NOARGS, ""},
    {"_box_grads", (PyCFunction)SpongeCVBoxGrads, METH_NOARGS, ""},
    {NULL,NULL,0,NULL}
};

static PyTypeObject SpongeCVType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "Sponge._COLLECTIVE_VARIABLE_PROTOTYPE",
    sizeof(SpongeCVObject),0,0,0,
    0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,
    0,SpongeCVMethods,0,0,0,0,0,0,0,(initproc)SpongeCVInit,
    0,SpongeCVNew,0,0,0,
};

static PyObject* Atom_Numbers(PyObject* self, PyObject*args)
{
    return Py_BuildValue("i", md_info->atom_numbers);
}

static PyObject* Steps(PyObject* self, PyObject*args)
{
    return Py_BuildValue("i", md_info->sys.steps);
}

static PyObject* Box_Length(PyObject* self, PyObject*args)
{
    return Py_BuildValue("(fff)", md_info->sys.box_length.x, md_info->sys.box_length.y, md_info->sys.box_length.z);
}

static PyObject* Neighbor_List_Atom_Numbers(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)neighbor_list->d_nl, sizeof(ATOM_GROUP) * md_info->atom_numbers, NULL,
        controller->working_device, md_info->atom_numbers, sizeof(ATOM_GROUP) / sizeof(int), "i");
}

static PyObject* Neighbor_List_Atom_Serials(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)neighbor_list->h_nl->atom_serial, sizeof(int) * md_info->atom_numbers * neighbor_list->max_neighbor_numbers, NULL,
        controller->working_device, md_info->atom_numbers, neighbor_list->max_neighbor_numbers, "i");
}

static PyObject* Coordinate(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)md_info->crd, sizeof(float) * 3 * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, 3, "f");
}

static PyObject* Velocity(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)md_info->vel, sizeof(float) * 3 * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, 3, "f");
}

static PyObject* Acceleration(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)md_info->acc, sizeof(float) * 3 * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, 3, "f");
}

static PyObject* Force(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),(ii),s)",(intptr_t)md_info->frc, sizeof(float) * 3 * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, 3, "f");
}

static PyObject* Mass(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),i,s)",(intptr_t)md_info->d_mass, sizeof(float) * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, "f");
}

static PyObject* Charge(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),i,s)",(intptr_t)md_info->d_charge, sizeof(float) * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, "f");
}

static PyObject* Atom_Energy(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),i,s)",(intptr_t)md_info->d_atom_energy, sizeof(float) * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, "f");
}

static PyObject* Atom_Virial(PyObject* self, PyObject*args)
{
    return Py_BuildValue("((Lizi),i,s)",(intptr_t)md_info->d_atom_virial, sizeof(float) * md_info->atom_numbers, NULL, controller->working_device, md_info->atom_numbers, "f");
}

static PyObject* Working_Device(PyObject* self, PyObject*args)
{
    return Py_BuildValue("i", controller->working_device);
}

static PyObject* Control_Printf(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"toprint", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s",kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    controller->printf("%s", buffer);
    return Py_BuildValue("");
}

static PyObject* Control_Warn(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"towarn", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s",kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    controller->Warn(buffer);
    return Py_BuildValue("");
}

static PyObject* Control_Error(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"error", (char*)"error_by", (char*)"error_hint", NULL};
    int error_num;
    char *buffer1;
    char *buffer2;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "iss",kwlist, &error_num, &buffer1, &buffer2))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    controller->Throw_SPONGE_Error(error_num, buffer1, buffer2);
    return Py_BuildValue("");
}

static PyObject* Command_Exist(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"command", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    if (controller->Command_Exist(buffer))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject* Command(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"command", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    return Py_BuildValue("s", controller->Command(buffer));
}

static PyObject* Original_Command(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"command", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    return Py_BuildValue("s", controller->Original_Command(buffer));
}

static PyObject* Step_Print_Initial(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"head", (char*)"format", NULL};
    char *head;
    char *format;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "ss", kwlist, &head, &format))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    controller->Step_Print_Initial(head, format);
    return Py_BuildValue("");
}

static PyObject* Step_Print(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"head", (char*)"content", NULL};
    char *head;
    char *content;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "ss", kwlist, &head, &content))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    controller->Step_Print(head, content);
    return Py_BuildValue("");
}

static PyObject* CV_Command_Exist(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"command", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    if (cv_controller->Command_Exist(buffer))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject* CV_Command(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"command", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    return Py_BuildValue("s", cv_controller->Command(buffer));
}

static PyObject* CV_Original_Command(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"command", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    return Py_BuildValue("s", cv_controller->Original_Command(buffer));
}

static PyObject* Get_CV(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"cv_name", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    return Py_BuildValue("L", (intptr_t)cv_controller->get_CV(buffer));
}

struct CV_PYTHON: public COLLECTIVE_VARIABLE_PROTOTYPE
{
    void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
    void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

void CV_PYTHON::Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name)
{
    Super_Initial(manager, atom_numbers, module_name);
    char buffer[CHAR_LENGTH_MAX];
    sprintf(buffer, "Sponge.COLLECTIVE_VARIABLE_PROTOTYPE.New(%ld, '%s')", (intptr_t)this ,module_name); 
    PyRun_SimpleString(buffer);
}

void CV_PYTHON::Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step)
{
    char buffer[CHAR_LENGTH_MAX + 82];
    sprintf(buffer, "Sponge.COLLECTIVE_VARIABLE_PROTOTYPE.objects['%s'].Compute(%d, %d)", module_name, need, step); 
    PyRun_SimpleString(buffer);
}

static PyObject* Register_CV(PyObject* self, PyObject* args, PyObject* kw)
{
    static char* kwlist[] = {(char*)"type_name", NULL};
    char *buffer;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &buffer))
    {
        PyErr_SetString(PyExc_Exception, "arguments are not right.");
        return NULL;
    }
    auto f = [buffer](COLLECTIVE_VARIABLE_CONTROLLER* manager, const char* name)
    {
        COLLECTIVE_VARIABLE_PROTOTYPE *cv = new CV_PYTHON;
        strcpy(cv->type_name, buffer);
        cv->Initial(manager, manager->atom_numbers, name);
        return cv;
    };
    CV_MAP[0][buffer] = f;
    return Py_BuildValue("");
}


static PyMethodDef SpongeMethod[] =
{
      {"_nl_atom_numbers",(PyCFunction)Neighbor_List_Atom_Numbers, METH_VARARGS, ""},
      {"_nl_atom_serials",(PyCFunction)Neighbor_List_Atom_Serials, METH_VARARGS, ""},
      {"_atom_numbers", (PyCFunction)Atom_Numbers, METH_VARARGS, ""},
      {"_crd", (PyCFunction)Coordinate, METH_VARARGS, ""},
      {"_vel", (PyCFunction)Velocity, METH_VARARGS, ""},
      {"_acc", (PyCFunction)Acceleration, METH_VARARGS, ""},
      {"_frc", (PyCFunction)Force, METH_VARARGS, ""},
      {"_d_mass", (PyCFunction)Mass, METH_VARARGS, ""},
      {"_d_charge", (PyCFunction)Charge, METH_VARARGS, ""},
      {"_d_atom_energy", (PyCFunction)Atom_Energy, METH_VARARGS, ""},
      {"_d_atom_virial", (PyCFunction)Atom_Virial, METH_VARARGS, ""},
      {"_steps", (PyCFunction)Steps, METH_VARARGS, ""},
      {"_box_length", (PyCFunction)Box_Length, METH_VARARGS, ""},
      {"_working_device", (PyCFunction)Working_Device, METH_VARARGS|METH_KEYWORDS, "" },
      {"_printf", (PyCFunction)Control_Printf, METH_VARARGS|METH_KEYWORDS, "" },
      {"_warn", (PyCFunction)Control_Warn, METH_VARARGS|METH_KEYWORDS, "" },
      {"_error", (PyCFunction)Control_Error, METH_VARARGS|METH_KEYWORDS, "" },
      {"_command_exist", (PyCFunction)Command_Exist, METH_VARARGS|METH_KEYWORDS, "" },
      {"_command", (PyCFunction)Command, METH_VARARGS|METH_KEYWORDS, "" },
      {"_original_command", (PyCFunction)Original_Command, METH_VARARGS|METH_KEYWORDS, "" },
      {"_step_print_initial", (PyCFunction)Step_Print_Initial, METH_VARARGS|METH_KEYWORDS, "" },
      {"_step_print", (PyCFunction)Step_Print, METH_VARARGS|METH_KEYWORDS, "" },
      {"_cv_command_exist", (PyCFunction)CV_Command_Exist, METH_VARARGS|METH_KEYWORDS, "" },
      {"_cv_command", (PyCFunction)CV_Command, METH_VARARGS|METH_KEYWORDS, "" },
      {"_cv_original_command", (PyCFunction)CV_Original_Command, METH_VARARGS|METH_KEYWORDS, "" },
      {"_get_cv", (PyCFunction)Get_CV, METH_VARARGS|METH_KEYWORDS, "" },
      {"_register_cv", (PyCFunction)Register_CV, METH_VARARGS|METH_KEYWORDS, "" },
      {NULL,NULL,0,NULL}
};

static PyModuleDef SpongeModule = 
{
  PyModuleDef_HEAD_INIT, "Sponge", NULL, -1, SpongeMethod,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_sponge(void)
{
    PyObject *m;
    if (PyType_Ready(&SpongeCVType) < 0)
        return NULL;
    m = PyModule_Create(&SpongeModule);
    if (m == NULL)
        return NULL;
    Py_INCREF(&SpongeCVType);
    if (PyModule_AddObject(m, "_COLLECTIVE_VARIABLE_PROTOTYPE", (PyObject *) &SpongeCVType) < 0) 
    {
        Py_DECREF(&SpongeCVType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}

PLUGIN_API std::string Name()
{
    return std::string("Python Runtime Interface Plugin");
}

PLUGIN_API std::string Version()
{
    return std::string("1.4b0");
}

PLUGIN_API std::string Version_Check(int i)
{
    if (i < 20231219)
    {
        return std::string("Reason:\n\tPRIPS v1.4b0 can not be used with SPONGE before 20231219. Your SPONGE: " + std::to_string(i));
    }
    return std::string();
}

PLUGIN_API void Initial(MD_INFORMATION* md, CONTROLLER* ctrl, NEIGHBOR_LIST* nl,
                        COLLECTIVE_VARIABLE_CONTROLLER* cv, CV_MAP_TYPE* cv_map, CV_INSTANCE_TYPE* cv_instance_map)
{
    md_info = md;
    controller = ctrl;
    neighbor_list = nl;
    cv_controller = cv;
    CV_MAP = cv_map;
    CV_INSTANCE_MAP = cv_instance_map;
    controller->printf("    initializing pyplugin\n");
    if (!controller->Command_Exist("py"))
    {
        controller->printf("        No 'py' command found. Pyplugin will not be initialized.\n");
        return;
    }
    PyImport_AppendInittab("Sponge",&PyInit_sponge);
    Py_Initialize();
    if (!Py_IsInitialized())
    {
        fprintf(stderr, "        Python Initialize Failed.\n");
        getchar();
        exit(1);
    }
    else
    {
        controller->printf("        Python Initialized\n");
    }
    wchar_t *temp_args[1] = {(wchar_t *)L"SPONGE"};
    PySys_SetArgv(1, temp_args); 
    PyRun_SimpleString(R"XYJ(
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import importlib.util as iu
import cupy as cp
from enum import Enum, Flag
import Sponge

old_excepthook = sys.excepthook
def new_hook(exctype, value, traceback):
    old_excepthook(exctype, value, traceback)
    exit(1)
sys.excepthook = new_hook
del new_hook

def _get_cupy_array(tuple):
    return cp.ndarray(tuple[1], dtype=tuple[2], memptr=cp.cuda.MemoryPointer(cp.cuda.UnownedMemory(*tuple[0]), 0))
Sponge._get_cupy_array = _get_cupy_array

class spongeError(Enum):
    spongeSuccess = 0
    # 未实现的功能
    spongeErrorNotImplemented = 1001
    # 文件格式（编码、换行符）问题 或 数据格式不正确
    spongeErrorBadFileFormat = 1002
    # 冲突的命令
    spongeErrorConflictingCommand = 1003
    # 缺失的命令
    spongeErrorMissingCommand = 1004
    # 类型错误的命令
    spongeErrorTypeErrorCommand = 1005
    # 值错误的命令
    spongeErrorValueErrorCommand = 1006
    # 模拟崩溃
    spongeErrorSimulationBreakDown = 1007
    # 内存分配失败
    spongeErrorMallocFailed = 1008
    # 越界
    spongeErrorOverflow = 1009
    # 打开文件失败
    spongeErrorOpenFileFailed = 1010

Sponge.spongeError = spongeError
del spongeError

class CONTROLLER:
    """
        this **class** is the module to control the input, output and cuda in SPONGE
    """
    def __init__(self):
        self.formats = {}

    @property
    def working_device(self):
        """ The working device id """
        return Sponge._working_device()

    def printf(self, *values, sep=" ", end="\n"):
        """ Print the values to the screen and the mdinfo file """
        return Sponge._printf(sep.join([f"{i}" for i in values]) + end)

    def Warn(self, warning):
        """ Print the warning to the screen and the mdinfo file """ 
        return Sponge._warn(warning)

    def Throw_SPONGE_Error(self, error, error_by, error_hint):
        """ Raise error to the screen and the mdinfo file, then exit """
        error = Sponge.spongeError(error)
        Sponge._error(error.value, error_by, error_hint)

    def Command_Exist(self, arg1, arg2=None):
        """
        Check the command whether exist in SPONGE.
        If Only arg1 is given, the command to check is "arg1".
        If arg1 and arg2 is given, the command to check is "arg1_arg2".

        :param arg1: the command or the command prefix
        :param arg2: the command suffix
        :return: True if the command exist, else False
        """
        if arg2 is None:
            return Sponge._command_exist(arg1)
        else:
            return Sponge._command_exist(f"{arg1}_{arg2}")

    def Command(self, arg1, arg2=None):
        """
        Get the simplified value of the command in SPONGE.
        If Only arg1 is given, the command to get the value is "arg1".
        If arg1 and arg2 is given, the command to get the value is "arg1_arg2".

        :param arg1: the command or the command prefix
        :param arg2: the command suffix
        :return: a string, the simplified value of the command
        """
        if arg2 is None:
            return Sponge._command(arg1)
        else:
            return Sponge._command(f"{arg1}_{arg2}")

    def Original_Command(self, arg1, arg2=None):
        """
        Get the original value of the command in SPONGE.
        If Only arg1 is given, the command to get the value is "arg1".
        If arg1 and arg2 is given, the command to get the value is "arg1_arg2".

        :param arg1: the command or the command prefix
        :param arg2: the command suffix
        :return: a string, the original value of the command
        """
        if arg2 is None:
            return Sponge._original_command(arg1)
        else:
            return Sponge._original_command(f"{arg1}_{arg2}")

    def Step_Print_Initial(self, head, format):
        """
        Initialize a step print item. A step print item is an item to print in the screen and in the mdout file.

        :param head: the name of the item
        :param format: the format of the step print item
        """
        self.formats[head] = format
        Sponge._step_print_initial(head, "%s")

    def Step_Print(self, head, content):
        """
        Print a step print item. A step print item is an item to print in the screen and in the mdout file.

        :param head: the name of the item
        :param content: the content of the step print item
        """
        Sponge._step_print(head, self.formats[head]%content)

    def __repr__(self):
        return "< IO and CUDA controller of SPONGE >"

Sponge.CONTROLLER = CONTROLLER
Sponge.controller = CONTROLLER()
del CONTROLLER

class COLLECTIVE_VARIABLE_NEED(Flag):
    CV_NEED_NONE = 0
    CV_NEED_GPU_VALUE = 1
    CV_NEED_CRD_GRADS = 2
    CV_NEED_CPU_VALUE = 4
    CV_NEED_BOX_GRADS = 8
    CV_NEED_ALL = 15

Sponge.COLLECTIVE_VARIABLE_NEED = COLLECTIVE_VARIABLE_NEED
del COLLECTIVE_VARIABLE_NEED

class COLLECTIVE_VARIABLE_PROTOTYPE:
    types = {}
    objects = {}
    def __init_subclass__(cls, type_name=None):
        if type_name is None:
            type_name = cls.__name__
        Sponge.COLLECTIVE_VARIABLE_PROTOTYPE.types[type_name] = cls
        Sponge._register_cv(type_name)

    def __init__(self, memptr):
        self._cv = Sponge._COLLECTIVE_VARIABLE_PROTOTYPE(memptr)
        self._cuda_stream = cp.cuda.ExternalStream(self._cv._get_cuda_stream(), Sponge.controller.working_device)
        self._d_value = Sponge._get_cupy_array(self._cv._d_value())
        self._crd_grads = Sponge._get_cupy_array(self._cv._crd_grads())
        self._box_grads = Sponge._get_cupy_array(self._cv._box_grads())

    @property
    def d_value(self):
        return self._d_value
    
    @d_value.setter
    def d_value(self, value):
        self._d_value[:] = value

    @property
    def crd_grads(self):
        return self._crd_grads

    @crd_grads.setter
    def crd_grads(self, value):
        self._crd_grads[:] = value

    @property
    def box_grads(self):
        return self._box_grads

    @box_grads.setter
    def box_grads(self, value):
        self._box_grads[:] = value

    @property
    def cuda_stream(self):
        return self._cuda_stream

    def get_last_update_step(self, need):
        return self._cv._get_last_update_step(need)
    
    def set_last_update_step(self, need, step):
        self._cv._set_last_update_step(need, step)

    def Check_Whether_Computed_At_This_Step(self, step, need):
        if (need & Sponge.CV_NEED_CPU_VALUE) and self.get_last_update_step(Sponge.CV_NEED_CPU_VALUE) == step:
            need &= ~Sponge.CV_NEED_CPU_VALUE
        if (need & Sponge.CV_NEED_GPU_VALUE) and self.get_last_update_step(Sponge.CV_NEED_GPU_VALUE) == step:
            need &= ~Sponge.CV_NEED_GPU_VALUE
        if (need & Sponge.CV_NEED_CRD_GRADS) and self.get_last_update_step(Sponge.CV_NEED_CRD_GRADS) == step:
            need &= ~Sponge.CV_NEED_CRD_GRADS
        if (need & Sponge.CV_NEED_BOX_GRADS) and self.get_last_update_step(Sponge.CV_NEED_BOX_GRADS) == step:
            need &= ~Sponge.CV_NEED_BOX_GRADS
        return need

    @classmethod
    def New(cls, memptr, module_name):
        type_name = Sponge.cv_controller.Command(module_name, "type")
        cls.objects[module_name] = cls.types[type_name](memptr, module_name)

    @property
    def value(self):
        return self._cv._get_value()
    
    @value.setter
    def value(self, value):
        return self._cv._set_value(value)


Sponge.COLLECTIVE_VARIABLE_PROTOTYPE = COLLECTIVE_VARIABLE_PROTOTYPE
del COLLECTIVE_VARIABLE_PROTOTYPE

class COLLECTIVE_VARIABLE_CONTROLLER(Sponge.CONTROLLER):
    def Get_CV(self, cv_name):
        return Sponge.COLLECTIVE_VARIABLE_PROTOTYPE(Sponge._get_cv(cv_name))

    def Command_Exist(self, arg1, arg2=None):
        if arg2 is None:
            return Sponge._cv_command_exist(arg1)
        else:
            return Sponge._cv_command_exist(f"{arg1}_{arg2}")

    def Command(self, arg1, arg2=None):
        if arg2 is None:
            return Sponge._cv_command(arg1)
        else:
            return Sponge._cv_command(f"{arg1}_{arg2}")

    def Original_Command(self, arg1, arg2=None):
        if arg2 is None:
            return Sponge._cv_original_command(arg1)
        else:
            return Sponge._cv_original_command(f"{arg1}_{arg2}")

    def Ask_For_CV(self, name, N, verbose_level=0):
        if self.Command_Exist(name, "CV"):
            cvs = self.Original_Command(name, "CV").split()
        if N > 0 and len(cvs) != N:
            self.printf("    Error: %d CV(s) should be given to %s, but %d found\n"%(N, name, len(cvs)))
            input()
            exit(1)
        elif N <= 0 and len(cvs) < -N:
            self.printf("    Error: at least %d CV(s) should be given to %s, but only %d found"%(N, name, len(cvs)))
            input()
            exit(1)
        if verbose_level > -2:
            self.printf("    %d CV(s) found for %s\n"%(len(cvs), name));
        to_ret = []
        for cv_name in cvs:
            if verbose_level > -1:
                self.printf("        CV %d: %s\n"%(i, cv_name))
            to_ret.append(get_CV(cv_name))
            if verbose_level > -1:
                self.printf("        type of '%s' is '%s'\n"%(cv_name, to_ret[-1].type_name));

    def __repr__(self):
        return "< cv controller of SPONGE>"

Sponge.COLLECTIVE_VARIABLE_CONTROLLER = COLLECTIVE_VARIABLE_CONTROLLER
Sponge.cv_controller = COLLECTIVE_VARIABLE_CONTROLLER()
del COLLECTIVE_VARIABLE_CONTROLLER

class MD_INFORMATION:
    """ Contains the information for MD simulations """
    def __init__(self):
        self._crd = _get_cupy_array(Sponge._crd())
        self._vel = _get_cupy_array(Sponge._vel())
        self._frc = _get_cupy_array(Sponge._frc())
        self._d_mass = _get_cupy_array(Sponge._d_mass())
        self._d_charge = _get_cupy_array(Sponge._d_charge())
        self._d_atom_energy = _get_cupy_array(Sponge._d_atom_energy())
        self._d_atom_virial = _get_cupy_array(Sponge._d_atom_virial())

        class system_information:
            """ the system information of MD information """
            @property
            def steps(self):
                """ the current step of the simulation """
                return Sponge._steps()
            @property
            def box_length(self):
                """ the length of the box """
                return Sponge._box_length()

        self._sys = system_information()

    @property
    def atom_numbers(self):
        """ the total number of atoms """
        return Sponge._atom_numbers()

    @property
    def crd(self):
        """ the position coordinates of the atoms """
        return self._crd

    @crd.setter
    def crd(self, value):
        self._crd[:] = value

    @property
    def vel(self):
        """ the velocity of the atoms """
        return self._vel

    @vel.setter
    def vel(self, value):
        self._vel[:] = value

    @property
    def frc(self):
        """ the force of the atoms """
        return self._frc

    @frc.setter
    def frc(self, value):
        self._frc[:] = value

    @property
    def d_mass(self):
        """ the mass of the atoms """
        return self._d_mass

    @property
    def d_charge(self):
        """ the charge of the atoms (In the unit of SPONGE, a unit charge is 18.2223) """
        return self._d_charge

    @d_charge.setter
    def d_charge(self, value):
        self._d_charge[:] = value

    @property
    def d_atom_energy(self):
        """ the energy of the atoms """
        return self._d_atom_energy

    @d_atom_energy.setter
    def d_atom_energy(self, value):
        self._d_atom_energy[:] = value

    @property
    def d_atom_virial(self):
        """ the virial of the atoms """
        return self._d_atom_virial

    @d_atom_virial.setter
    def d_atom_virial(self, value):
        self._d_atom_virial[:] = value

    @property
    def sys(self):
        """ the system information """
        return self._sys

    def __repr__(self):
        return "< MD information container of SPONGE >"

Sponge.MD_INFORMATION = MD_INFORMATION
Sponge.md_info = MD_INFORMATION()
del MD_INFORMATION

class NEIGHBOR_LIST:
    """ 
        Neighbor List of SPONGE.
        This class should be initialized at After_Initial, because neighbor_list is not initialized when initializing prips"""
    def __init__(self):
        self._atom_numbers = Sponge._get_cupy_array(Sponge._nl_atom_numbers())
        self._atom_serials = Sponge._get_cupy_array(Sponge._nl_atom_serials())

    @property
    def atom_numbers(self):
        """ the number of neighbors for every atom """
        return self._atom_numbers[:, 0]

    @property
    def atom_serials(self):
        """ the serial of neighbors for every atom """
        return self._atom_serials

Sponge.NEIGHBOR_LIST = NEIGHBOR_LIST
del NEIGHBOR_LIST

del _get_cupy_array
    )XYJ");
    char buffer[CHAR_LENGTH_MAX];
    sprintf(buffer, "Sponge.fname = r'%s'", controller->Command("py")); 
    PyRun_SimpleString(buffer);
    PyRun_SimpleString(R"XYJ(sponge_pyplugin_path = Path(Sponge.fname)
spec = iu.spec_from_file_location('sponge_pyplugin', sponge_pyplugin_path)
sponge_pyplugin = iu.module_from_spec(spec)
spec.loader.exec_module(sponge_pyplugin)
Sponge.controller.printf("        module '%s' imported."%(sponge_pyplugin_path.stem))
    )XYJ");
    is_initialized = 1;
    controller->printf("    end initializing pyplugin\n");
}

PLUGIN_API void After_Initial()
{
    if (!is_initialized)
        return;
    PyRun_SimpleString(R"XYJ(
if hasattr(sponge_pyplugin, "After_Initial"):
    sponge_pyplugin.After_Initial()
    )XYJ");
}

PLUGIN_API void Calculate_Force()
{
    if (!is_initialized)
        return;
    PyRun_SimpleString(R"XYJ(
if hasattr(sponge_pyplugin, "Calculate_Force"):
    sponge_pyplugin.Calculate_Force()
    )XYJ");
}

PLUGIN_API void Mdout_Print()
{
    if (!is_initialized)
        return;
    PyRun_SimpleString(R"XYJ(
if hasattr(sponge_pyplugin, "Mdout_Print"):
    sponge_pyplugin.Mdout_Print()
    )XYJ");
}
