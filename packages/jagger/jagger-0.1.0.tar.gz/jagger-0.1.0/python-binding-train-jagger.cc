#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;


int bora(int i, int j) {
  return i * 2 + j * 3;
}

PYBIND11_MODULE(jagger, m) {
    m.doc() = "Python binding for Jagger.";

    m.def("bora", &bora, "test");

}

