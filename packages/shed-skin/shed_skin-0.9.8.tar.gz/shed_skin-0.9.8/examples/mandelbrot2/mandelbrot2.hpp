#ifndef __MANDELBROT2_HPP
#define __MANDELBROT2_HPP

using namespace __shedskin__;
namespace __mandelbrot2__ {

extern str *const_0, *const_1, *const_2, *const_3, *const_4, *const_5;

class kohn_bmp;


extern str *__name__;
extern list<tuple<__ss_int> *> *colors;
extern __ss_int res;


extern class_ *cl_kohn_bmp;
class kohn_bmp : public pyobj {
/**
py_kohn_bmp - Copyright 2007 by Michael Kohn
http://www.mikekohn.net/
mike@mikekohn.net
*/
public:
    file_binary *out;
    __ss_int width_bytes;
    __ss_int xpos;
    __ss_int depth;
    __ss_int width;
    __ss_int height;

    kohn_bmp() {}
    kohn_bmp(str *filename, __ss_int width, __ss_int height, __ss_int depth) {
        this->__class__ = cl_kohn_bmp;
        __init__(filename, width, height, depth);
    }
    static void __static__();
    void *__init__(str *filename, __ss_int width, __ss_int height, __ss_int depth);
    void *write_int(__ss_int n);
    void *write_word(__ss_int n);
    void *write_pixel(__ss_int red, __ss_int green, __ss_int blue);
    void *close();
    virtual PyObject *__to_py__();
};

__ss_int mandel(__ss_float real, __ss_float imag, __ss_int max_iterations);
list<tuple<__ss_int> *> *make_colors(__ss_int number_of_colors, __ss_float saturation, __ss_float value);
str *mandel_file(__ss_float cx, __ss_float cy, __ss_float size, __ss_int max_iterations, __ss_int width, __ss_int height);

extern "C" {
PyMODINIT_FUNC PyInit_mandelbrot2(void);

}
} // module namespace
extern "C" PyTypeObject __ss_mandelbrot2_kohn_bmpObjectType;
namespace __shedskin__ { /* XXX */

template<> __mandelbrot2__::kohn_bmp *__to_ss(PyObject *p);
}
#endif
