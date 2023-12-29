#include "builtin.hpp"
#include "time.hpp"
#include "colorsys.hpp"
#include "sys.hpp"
#include "mandelbrot2.hpp"

namespace __mandelbrot2__ {

str *const_0, *const_1, *const_2, *const_3, *const_4, *const_5;


str *__name__;
list<tuple<__ss_int> *> *colors;
__ss_int res;


class list_comp_0 : public __iter<bytes *> {
public:
    __ss_int __3, __4, c;

    int __last_yield;

    list_comp_0();
    bytes * __get_next();
};

static inline list<tuple<__ss_float> *> *list_comp_1(__ss_float saturation, __ss_int number_of_colors, __ss_float value);
static inline list<tuple<__ss_int> *> *list_comp_2(list<tuple<__ss_float> *> *tuples);

list_comp_0::list_comp_0() {
    __last_yield = -1;
}

bytes * list_comp_0::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(c,0,__ss_int(256),1,3,4)
        __result = ((__mod6(new bytes("%c"), 1, c))->__mul__(__ss_int(3)))->__add__(new bytes("\000", 1));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<bytes *>();
}

static inline list<tuple<__ss_float> *> *list_comp_1(__ss_float saturation, __ss_int number_of_colors, __ss_float value) {
    __ss_int __10, __9, x;

    list<tuple<__ss_float> *> *__ss_result = new list<tuple<__ss_float> *>();

    FAST_FOR(x,0,number_of_colors,1,9,10)
        __ss_result->append(__colorsys__::hsv_to_rgb(((x*__ss_float(1.0))/number_of_colors), saturation, value));
    END_FOR

    return __ss_result;
}

static inline list<tuple<__ss_int> *> *list_comp_2(list<tuple<__ss_float> *> *tuples) {
    tuple<__ss_float> *__11;
    __ss_float b, g, r;
    list<tuple<__ss_float> *> *__12;
    __iter<tuple<__ss_float> *> *__13;
    __ss_int __14;
    list<tuple<__ss_float> *>::for_in_loop __15;

    list<tuple<__ss_int> *> *__ss_result = new list<tuple<__ss_int> *>();

    __ss_result->resize(len(tuples));
    FOR_IN(__11,tuples,12,14,15)
        __11 = __11;
        __unpack_check(__11, 3);
        r = __11->__getfast__(0);
        g = __11->__getfast__(1);
        b = __11->__getfast__(2);
        __ss_result->units[__14] = (new tuple<__ss_int>(3,__int((__ss_int(256)*r)),__int((__ss_int(256)*g)),__int((__ss_int(256)*b))));
    END_FOR

    return __ss_result;
}

/**
class kohn_bmp
*/

class_ *cl_kohn_bmp;

void *kohn_bmp::__init__(str *filename, __ss_int width, __ss_int height, __ss_int depth) {
    void *c;

    this->width = width;
    this->height = height;
    this->depth = depth;
    this->xpos = __ss_int(0);
    this->width_bytes = (width*depth);
    if ((__mods(this->width_bytes, __ss_int(4))!=__ss_int(0))) {
        this->width_bytes = (this->width_bytes+(__ss_int(4)-__mods(this->width_bytes, __ss_int(4))));
    }
    this->out = open_binary(filename, const_0);
    (this->out)->write(new bytes("BM"));
    this->write_int((((this->width_bytes*height)+__ss_int(54))+(((depth==__ss_int(1)))?(__ss_int(1024)):(__ss_int(0)))));
    this->write_word(__ss_int(0));
    this->write_word(__ss_int(0));
    this->write_int((__ss_int(54)+(((depth==__ss_int(1)))?(__ss_int(1024)):(__ss_int(0)))));
    this->write_int(__ss_int(40));
    this->write_int(width);
    this->write_int(height);
    this->write_word(__ss_int(1));
    this->write_word((depth*__ss_int(8)));
    this->write_int(__ss_int(0));
    this->write_int(((this->width_bytes*height)*depth));
    this->write_int(__ss_int(0));
    this->write_int(__ss_int(0));
    if ((depth==__ss_int(1))) {
        this->write_int(__ss_int(256));
        this->write_int(__ss_int(256));
        (this->out)->write((new bytes(""))->join(new list_comp_0()));
    }
    else {
        this->write_int(__ss_int(0));
        this->write_int(__ss_int(0));
    }
    return NULL;
}

void *kohn_bmp::write_int(__ss_int n) {
    
    (this->out)->write(__mod6(new bytes("%c%c%c%c"), 4, ((n)&(__ss_int(255))), (((n>>__ss_int(8)))&(__ss_int(255))), (((n>>__ss_int(16)))&(__ss_int(255))), (((n>>__ss_int(24)))&(__ss_int(255)))));
    return NULL;
}

void *kohn_bmp::write_word(__ss_int n) {
    
    (this->out)->write(__mod6(new bytes("%c%c"), 2, ((n)&(__ss_int(255))), (((n>>__ss_int(8)))&(__ss_int(255)))));
    return NULL;
}

void *kohn_bmp::write_pixel(__ss_int red, __ss_int green, __ss_int blue) {
    
    (this->out)->write(__mod6(new bytes("%c%c%c"), 3, __int(((blue)&(__ss_int(255)))), __int(((green)&(__ss_int(255)))), __int(((red)&(__ss_int(255))))));
    this->xpos = (this->xpos+__ss_int(1));
    if ((this->xpos==this->width)) {
        this->xpos = (this->xpos*__ss_int(3));

        while ((this->xpos<this->width_bytes)) {
            (this->out)->write(new bytes("\000", 1));
            this->xpos = (this->xpos+__ss_int(1));
        }
        this->xpos = __ss_int(0);
    }
    return NULL;
}

void *kohn_bmp::close() {
    
    (this->out)->close();
    return NULL;
}

void kohn_bmp::__static__() {
}

__ss_int mandel(__ss_float real, __ss_float imag, __ss_int max_iterations) {
    /**
    determines if a point is in the Mandelbrot set based on deciding if,
    after a maximum allowed number of iterations, the absolute value of
    the resulting number is greater or equal to 2.
    */
    __ss_float __7, __8, z_imag, z_real;
    __ss_int __5, __6, i;

    z_real = __ss_float(0.0);
    z_imag = __ss_float(0.0);

    FAST_FOR(i,__ss_int(0),max_iterations,1,5,6)
        __7 = (((z_real*z_real)-(z_imag*z_imag))+real);
        __8 = (((__ss_int(2)*z_real)*z_imag)+imag);
        z_real = __7;
        z_imag = __8;
        if ((((z_real*z_real)+(z_imag*z_imag))>=((__ss_float)(__ss_int(4))))) {
            return __mods(i, max_iterations);
        }
    END_FOR

    return (-__ss_int(1));
}

list<tuple<__ss_int> *> *make_colors(__ss_int number_of_colors, __ss_float saturation, __ss_float value) {
    list<tuple<__ss_float> *> *tuples;

    number_of_colors = (number_of_colors-__ss_int(1));
    tuples = list_comp_1(saturation, number_of_colors, value);
    return ((new list<tuple<__ss_int> *>(1,(new tuple<__ss_int>(3,__ss_int(0),__ss_int(0),__ss_int(0))))))->__add__(list_comp_2(tuples));
}

str *mandel_file(__ss_float cx, __ss_float cy, __ss_float size, __ss_int max_iterations, __ss_int width, __ss_int height) {
    __ss_float __16, __17, current_x, current_y, increment, proportion, start_imag, start_real, t0;
    str *fname, *mandel_pos;
    kohn_bmp *my_bmp;
    __ss_int __18, __19, __20, __21, c, x, y;

    t0 = __time__::time();
    increment = ___min(2, (__ss_float(__ss_int(0))), (size/width), (size/height));
    proportion = ((__ss_float(1.0)*width)/height);
    __16 = (cx-((increment*width)/__ss_int(2)));
    __17 = (cy-((increment*height)/__ss_int(2)));
    start_real = __16;
    start_imag = __17;
    mandel_pos = __mod6(const_1, 4, cx, cy, size, max_iterations);
    fname = __mod6(const_2, 1, mandel_pos);
    my_bmp = (new kohn_bmp(fname, width, height, __ss_int(3)));
    current_y = start_imag;

    FAST_FOR(y,0,height,1,18,19)
        if (__NOT(__mods(y, __ss_int(10)))) {
            (__sys__::__ss_stdout)->write(__mod6(const_3, 2, (y+__ss_int(1)), height));
        }
        (__sys__::__ss_stdout)->flush();
        current_x = start_real;

        FAST_FOR(x,0,width,1,20,21)
            c = mandel(current_x, current_y, max_iterations);
            c = (((c!=(-__ss_int(1))))?((__mods(c, (len(__mandelbrot2__::colors)-__ss_int(1)))+__ss_int(1))):(__ss_int(0)));
            current_x = (current_x+increment);
            my_bmp->write_pixel((__mandelbrot2__::colors->__getfast__(c))->__getfast__(__ss_int(0)), (__mandelbrot2__::colors->__getfast__(c))->__getfast__(__ss_int(1)), (__mandelbrot2__::colors->__getfast__(c))->__getfast__(__ss_int(2)));
        END_FOR

        current_y = (current_y+increment);
    END_FOR

    print(1, NULL, NULL, NULL, __mod6(const_4, 1, (__time__::time()-t0)));
    my_bmp->close();
    return fname;
}

void __init() {
    const_0 = new str("wb");
    const_1 = new str("%g %gi_%g_%i");
    const_2 = new str("m%s.bmp");
    const_3 = new str("\rrow %i / %i");
    const_4 = new str("\r%.3f s             ");
    const_5 = new str("__main__");

    __name__ = new str("mandelbrot2");

    cl_kohn_bmp = new class_("kohn_bmp");
    kohn_bmp::__static__();
    colors = make_colors(__ss_int(1024), __ss_float(0.8), __ss_float(0.9));
    if (__eq(__mandelbrot2__::__name__, const_5)) {
        res = __ss_int(0);
        res = mandel(__ss_float(1.0), __ss_float(1.0), __ss_int(128));
        mandel_file((-__ss_float(0.7)), __ss_float(0.0), __ss_float(3.2), __ss_int(256), __ss_int(640), __ss_int(480));
    }
}

} // module namespace

/* extension module glue */

extern "C" {
#include <Python.h>
#include "time.hpp"
#include "colorsys.hpp"
#include "sys.hpp"
#include "mandelbrot2.hpp"
#include <structmember.h>
#include "time.hpp"
#include "colorsys.hpp"
#include "sys.hpp"
#include "mandelbrot2.hpp"

PyObject *__ss_mod_mandelbrot2;

namespace __mandelbrot2__ { /* XXX */

/* class kohn_bmp */

typedef struct {
    PyObject_HEAD
    __mandelbrot2__::kohn_bmp *__ss_object;
} __ss_mandelbrot2_kohn_bmpObject;

static PyMemberDef __ss_mandelbrot2_kohn_bmpMembers[] = {
    {NULL}
};

PyObject *__ss_mandelbrot2_kohn_bmp___init__(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        str *arg_0 = __ss_arg<str *>("filename", 0, 0, 0, args, kwargs);
        __ss_int arg_1 = __ss_arg<__ss_int >("width", 1, 0, 0, args, kwargs);
        __ss_int arg_2 = __ss_arg<__ss_int >("height", 2, 0, 0, args, kwargs);
        __ss_int arg_3 = __ss_arg<__ss_int >("depth", 3, 0, 0, args, kwargs);

        return __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->__init__(arg_0, arg_1, arg_2, arg_3));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

PyObject *__ss_mandelbrot2_kohn_bmp_write_int(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        __ss_int arg_0 = __ss_arg<__ss_int >("n", 0, 0, 0, args, kwargs);

        return __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->write_int(arg_0));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

PyObject *__ss_mandelbrot2_kohn_bmp_write_word(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        __ss_int arg_0 = __ss_arg<__ss_int >("n", 0, 0, 0, args, kwargs);

        return __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->write_word(arg_0));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

PyObject *__ss_mandelbrot2_kohn_bmp_write_pixel(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        __ss_int arg_0 = __ss_arg<__ss_int >("red", 0, 0, 0, args, kwargs);
        __ss_int arg_1 = __ss_arg<__ss_int >("green", 1, 0, 0, args, kwargs);
        __ss_int arg_2 = __ss_arg<__ss_int >("blue", 2, 0, 0, args, kwargs);

        return __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->write_pixel(arg_0, arg_1, arg_2));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

PyObject *__ss_mandelbrot2_kohn_bmp_close(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {

        return __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->close());

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

static PyNumberMethods __ss_mandelbrot2_kohn_bmp_as_number = {
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
};

PyObject *__ss_mandelbrot2_kohn_bmp__reduce__(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *__ss_mandelbrot2_kohn_bmp__setstate__(PyObject *self, PyObject *args, PyObject *kwargs);

static PyMethodDef __ss_mandelbrot2_kohn_bmpMethods[] = {
    {(char *)"__reduce__", (PyCFunction)__ss_mandelbrot2_kohn_bmp__reduce__, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"__setstate__", (PyCFunction)__ss_mandelbrot2_kohn_bmp__setstate__, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"__init__", (PyCFunction)__ss_mandelbrot2_kohn_bmp___init__, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"write_int", (PyCFunction)__ss_mandelbrot2_kohn_bmp_write_int, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"write_word", (PyCFunction)__ss_mandelbrot2_kohn_bmp_write_word, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"write_pixel", (PyCFunction)__ss_mandelbrot2_kohn_bmp_write_pixel, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"close", (PyCFunction)__ss_mandelbrot2_kohn_bmp_close, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {NULL, NULL, 0, NULL}
};

int __ss_mandelbrot2_kohn_bmp___tpinit__(PyObject *self, PyObject *args, PyObject *kwargs) {
    if(!__ss_mandelbrot2_kohn_bmp___init__(self, args, kwargs))
        return -1;
    return 0;
}

PyObject *__ss_mandelbrot2_kohn_bmpNew(PyTypeObject *type, PyObject *args, PyObject *kwargs) {
    __ss_mandelbrot2_kohn_bmpObject *self = (__ss_mandelbrot2_kohn_bmpObject *)type->tp_alloc(type, 0);
    self->__ss_object = new __mandelbrot2__::kohn_bmp();
    self->__ss_object->__class__ = __mandelbrot2__::cl_kohn_bmp;
    __ss_proxy->__setitem__(self->__ss_object, self);
    return (PyObject *)self;
}

void __ss_mandelbrot2_kohn_bmpDealloc(__ss_mandelbrot2_kohn_bmpObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
    __ss_proxy->__delitem__(self->__ss_object);
}

PyObject *__ss_get___ss_mandelbrot2_kohn_bmp_width_bytes(__ss_mandelbrot2_kohn_bmpObject *self, void *closure) {
    return __to_py(self->__ss_object->width_bytes);
}

int __ss_set___ss_mandelbrot2_kohn_bmp_width_bytes(__ss_mandelbrot2_kohn_bmpObject *self, PyObject *value, void *closure) {
    try {
        self->__ss_object->width_bytes = __to_ss<__ss_int >(value);
    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return -1;
    }
    return 0;
}

PyObject *__ss_get___ss_mandelbrot2_kohn_bmp_xpos(__ss_mandelbrot2_kohn_bmpObject *self, void *closure) {
    return __to_py(self->__ss_object->xpos);
}

int __ss_set___ss_mandelbrot2_kohn_bmp_xpos(__ss_mandelbrot2_kohn_bmpObject *self, PyObject *value, void *closure) {
    try {
        self->__ss_object->xpos = __to_ss<__ss_int >(value);
    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return -1;
    }
    return 0;
}

PyObject *__ss_get___ss_mandelbrot2_kohn_bmp_depth(__ss_mandelbrot2_kohn_bmpObject *self, void *closure) {
    return __to_py(self->__ss_object->depth);
}

int __ss_set___ss_mandelbrot2_kohn_bmp_depth(__ss_mandelbrot2_kohn_bmpObject *self, PyObject *value, void *closure) {
    try {
        self->__ss_object->depth = __to_ss<__ss_int >(value);
    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return -1;
    }
    return 0;
}

PyObject *__ss_get___ss_mandelbrot2_kohn_bmp_width(__ss_mandelbrot2_kohn_bmpObject *self, void *closure) {
    return __to_py(self->__ss_object->width);
}

int __ss_set___ss_mandelbrot2_kohn_bmp_width(__ss_mandelbrot2_kohn_bmpObject *self, PyObject *value, void *closure) {
    try {
        self->__ss_object->width = __to_ss<__ss_int >(value);
    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return -1;
    }
    return 0;
}

PyObject *__ss_get___ss_mandelbrot2_kohn_bmp_height(__ss_mandelbrot2_kohn_bmpObject *self, void *closure) {
    return __to_py(self->__ss_object->height);
}

int __ss_set___ss_mandelbrot2_kohn_bmp_height(__ss_mandelbrot2_kohn_bmpObject *self, PyObject *value, void *closure) {
    try {
        self->__ss_object->height = __to_ss<__ss_int >(value);
    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return -1;
    }
    return 0;
}

PyGetSetDef __ss_mandelbrot2_kohn_bmpGetSet[] = {
    {(char *)"width_bytes", (getter)__ss_get___ss_mandelbrot2_kohn_bmp_width_bytes, (setter)__ss_set___ss_mandelbrot2_kohn_bmp_width_bytes, (char *)"", NULL},
    {(char *)"xpos", (getter)__ss_get___ss_mandelbrot2_kohn_bmp_xpos, (setter)__ss_set___ss_mandelbrot2_kohn_bmp_xpos, (char *)"", NULL},
    {(char *)"depth", (getter)__ss_get___ss_mandelbrot2_kohn_bmp_depth, (setter)__ss_set___ss_mandelbrot2_kohn_bmp_depth, (char *)"", NULL},
    {(char *)"width", (getter)__ss_get___ss_mandelbrot2_kohn_bmp_width, (setter)__ss_set___ss_mandelbrot2_kohn_bmp_width, (char *)"", NULL},
    {(char *)"height", (getter)__ss_get___ss_mandelbrot2_kohn_bmp_height, (setter)__ss_set___ss_mandelbrot2_kohn_bmp_height, (char *)"", NULL},
    {NULL}
};

PyTypeObject __ss_mandelbrot2_kohn_bmpObjectType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "mandelbrot2.kohn_bmp",
    sizeof( __ss_mandelbrot2_kohn_bmpObject),
    0,
    (destructor) __ss_mandelbrot2_kohn_bmpDealloc,
    0,
    0,
    0,
    0,
    0,
    &__ss_mandelbrot2_kohn_bmp_as_number,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    Py_TPFLAGS_DEFAULT,
    PyDoc_STR("Custom objects"),
    0,
    0,
    0,
    0,
    0,
    0,
    __ss_mandelbrot2_kohn_bmpMethods,
    __ss_mandelbrot2_kohn_bmpMembers,
    __ss_mandelbrot2_kohn_bmpGetSet,
    0, 
    0, 
    0, 
    0, 
    0, 
    (initproc) __ss_mandelbrot2_kohn_bmp___tpinit__,
    0,
    __ss_mandelbrot2_kohn_bmpNew,
};

PyObject *__ss_mandelbrot2_kohn_bmp__reduce__(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *t = PyTuple_New(3);
    PyTuple_SetItem(t, 0, PyObject_GetAttrString(__ss_mod_mandelbrot2, "__newobj__"));
    PyObject *a = PyTuple_New(1);
    Py_INCREF((PyObject *)&__ss_mandelbrot2_kohn_bmpObjectType);
    PyTuple_SetItem(a, 0, (PyObject *)&__ss_mandelbrot2_kohn_bmpObjectType);
    PyTuple_SetItem(t, 1, a);
    PyObject *b = PyTuple_New(5);
    PyTuple_SetItem(b, 0, __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->width_bytes));
    PyTuple_SetItem(b, 1, __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->xpos));
    PyTuple_SetItem(b, 2, __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->depth));
    PyTuple_SetItem(b, 3, __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->width));
    PyTuple_SetItem(b, 4, __to_py(((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->height));
    PyTuple_SetItem(t, 2, b);
    return t;
}

PyObject *__ss_mandelbrot2_kohn_bmp__setstate__(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *state = PyTuple_GetItem(args, 0);
    ((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->width_bytes = __to_ss<__ss_int >(PyTuple_GetItem(state, 0));
    ((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->xpos = __to_ss<__ss_int >(PyTuple_GetItem(state, 1));
    ((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->depth = __to_ss<__ss_int >(PyTuple_GetItem(state, 2));
    ((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->width = __to_ss<__ss_int >(PyTuple_GetItem(state, 3));
    ((__ss_mandelbrot2_kohn_bmpObject *)self)->__ss_object->height = __to_ss<__ss_int >(PyTuple_GetItem(state, 4));
    Py_INCREF(Py_None);
    return Py_None;
}

} // namespace __mandelbrot2__

namespace __mandelbrot2__ { /* XXX */
PyObject *Global_mandelbrot2_mandel(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        __ss_float arg_0 = __ss_arg<__ss_float >("real", 0, 0, 0, args, kwargs);
        __ss_float arg_1 = __ss_arg<__ss_float >("imag", 1, 0, 0, args, kwargs);
        __ss_int arg_2 = __ss_arg<__ss_int >("max_iterations", 2, 1, __ss_int(20), args, kwargs);

        return __to_py(__mandelbrot2__::mandel(arg_0, arg_1, arg_2));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

PyObject *Global_mandelbrot2_make_colors(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        __ss_int arg_0 = __ss_arg<__ss_int >("number_of_colors", 0, 0, 0, args, kwargs);
        __ss_float arg_1 = __ss_arg<__ss_float >("saturation", 1, 1, __ss_float(0.8), args, kwargs);
        __ss_float arg_2 = __ss_arg<__ss_float >("value", 2, 1, __ss_float(0.9), args, kwargs);

        return __to_py(__mandelbrot2__::make_colors(arg_0, arg_1, arg_2));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

PyObject *Global_mandelbrot2_mandel_file(PyObject *self, PyObject *args, PyObject *kwargs) {
    try {
        __ss_float arg_0 = __ss_arg<__ss_float >("cx", 0, 1, (-__ss_float(0.7)), args, kwargs);
        __ss_float arg_1 = __ss_arg<__ss_float >("cy", 1, 1, __ss_float(0.0), args, kwargs);
        __ss_float arg_2 = __ss_arg<__ss_float >("size", 2, 1, __ss_float(3.2), args, kwargs);
        __ss_int arg_3 = __ss_arg<__ss_int >("max_iterations", 3, 1, __ss_int(512), args, kwargs);
        __ss_int arg_4 = __ss_arg<__ss_int >("width", 4, 1, __ss_int(640), args, kwargs);
        __ss_int arg_5 = __ss_arg<__ss_int >("height", 5, 1, __ss_int(480), args, kwargs);

        return __to_py(__mandelbrot2__::mandel_file(arg_0, arg_1, arg_2, arg_3, arg_4, arg_5));

    } catch (Exception *e) {
        PyErr_SetString(__to_py(e), ((e->message)?(e->message->c_str()):""));
        return 0;
    }
}

static PyNumberMethods Global_mandelbrot2_as_number = {
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
};

static PyMethodDef Global_mandelbrot2Methods[] = {
    {(char *)"__newobj__", (PyCFunction)__ss__newobj__, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"mandel", (PyCFunction)Global_mandelbrot2_mandel, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"make_colors", (PyCFunction)Global_mandelbrot2_make_colors, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {(char *)"mandel_file", (PyCFunction)Global_mandelbrot2_mandel_file, METH_VARARGS | METH_KEYWORDS, (char *)""},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module_mandelbrot2 = {
    PyModuleDef_HEAD_INIT,
    "mandelbrot2",   /* name of module */
    NULL,   /* module documentation, may be NULL */
    -1,     /* size of per-interpreter state of the module or -1 if the module keeps state in global variables. */
    Global_mandelbrot2Methods
};

PyMODINIT_FUNC PyInit_mandelbrot2(void) {

    __shedskin__::__init();
    __sys__::__init(0, 0);
    __time__::__init();
    __colorsys__::__init();
    __mandelbrot2__::__init();

    PyObject *m;

    if (PyType_Ready(&__ss_mandelbrot2_kohn_bmpObjectType) < 0)
        return NULL;

    // create extension module
    __ss_mod_mandelbrot2 = m = PyModule_Create(&Module_mandelbrot2);
    if (m == NULL)
        return NULL;

    // add global variables
    PyModule_AddObject(m, (char *)"colors", __to_py(__mandelbrot2__::colors));
    PyModule_AddObject(m, (char *)"res", __to_py(__mandelbrot2__::res));

    // add type objects
    Py_INCREF(&__ss_mandelbrot2_kohn_bmpObjectType);
    if (PyModule_AddObject(m, "kohn_bmp", (PyObject *) &__ss_mandelbrot2_kohn_bmpObjectType) < 0) {
        Py_DECREF(&__ss_mandelbrot2_kohn_bmpObjectType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}


} // namespace __mandelbrot2__

} // extern "C"
namespace __mandelbrot2__ { /* XXX */

PyObject *kohn_bmp::__to_py__() {
    PyObject *p;
    if(__ss_proxy->has_key(this))
        p = (PyObject *)(__ss_proxy->__getitem__(this));
    else {
        __ss_mandelbrot2_kohn_bmpObject *self = (__ss_mandelbrot2_kohn_bmpObject *)(__ss_mandelbrot2_kohn_bmpObjectType.tp_alloc(&__ss_mandelbrot2_kohn_bmpObjectType, 0));
        self->__ss_object = this;
        __ss_proxy->__setitem__(self->__ss_object, self);
        p = (PyObject *)self;
    }
    Py_INCREF(p);
    return p;
}

} // module namespace

namespace __shedskin__ { /* XXX */

template<> __mandelbrot2__::kohn_bmp *__to_ss(PyObject *p) {
    if(p == Py_None) return NULL;
    if(PyObject_IsInstance(p, (PyObject *)&__mandelbrot2__::__ss_mandelbrot2_kohn_bmpObjectType)!=1)
        throw new TypeError(new str("error in conversion to Shed Skin (kohn_bmp expected)"));
    return ((__mandelbrot2__::__ss_mandelbrot2_kohn_bmpObject *)p)->__ss_object;
}
}
int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __sys__::__init(0, 0);
    __time__::__init();
    __colorsys__::__init();
    __shedskin__::__start(__mandelbrot2__::__init);
}
